"""ML 모델 서비스: 예측 로직 + 헬스 스코어 계산"""

from pathlib import Path
from functools import lru_cache
import numpy as np
import pandas as pd

# predict_utils는 상위 디렉토리에서 import
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from predict_utils import load_models, predict_revpar, compute_health_score  # noqa: E402

DATA_DIR = Path(__file__).parent.parent / "data"

# ── 자치구 이름 매핑 (Next.js 형식 → district_lookup.csv 형식) ─────────────────
DISTRICT_NAME_MAP: dict[str, str] = {
    "Gangnam":      "Gangnam-gu",
    "Gangdong":     "Gangdong-gu",
    "Gangbuk":      "Gangbuk-gu",
    "Gangseo":      "Gangseo-gu",
    "Gwanak":       "Gwanak-gu",
    "Gwangjin":     "Gwangjin-gu",
    "Guro":         "Guro-gu",
    "Geumcheon":    "Geumcheon-gu",
    "Nowon":        "Nowon-gu",
    "Dobong":       "Dobong-gu",
    "Dongdaemun":   "Dongdaemun-gu",
    "Dongjak":      "Dongjak-gu",
    "Mapo":         "Mapo-gu",
    "Seodaemun":    "Seodaemun-gu",
    "Seocho":       "Seocho-gu",
    "Seongdong":    "Seongdong-gu",
    "Seongbuk":     "Seongbuk-gu",
    "Songpa":       "Songpa-gu",
    "Yangcheon":    "Yangcheon-gu",
    "Yeongdeungpo": "Yeongdeungpo-gu",
    "Yongsan":      "Yongsan-gu",
    "Eunpyeong":    "Eunpyeong-gu",
    "Jongno":       "Jongno-gu",
    "Jung":         "Jung-gu",
    "Jungnang":     "Jungnang-gu",
}

# ── room_type 매핑 (Next.js UI 값 → predict_utils 값) ─────────────────────────
ROOM_TYPE_MAP: dict[str, str] = {
    "Entire home/apt": "entire_home",
    "Private room":    "private_room",
    "Shared room":     "shared_room",
    "Hotel room":      "hotel_room",
    "entire_home":     "entire_home",
    "private_room":    "private_room",
    "shared_room":     "shared_room",
    "hotel_room":      "hotel_room",
}

# ── 사진 티어 헬퍼 ────────────────────────────────────────────────────────────
def get_photos_tier(photos_count: int) -> str:
    if photos_count < 14:    return "하"
    elif photos_count < 23:  return "중하"
    elif photos_count <= 35: return "중상"
    else:                    return "상"

# ── POI 거리 카테고리 ─────────────────────────────────────────────────────────
def get_poi_dist_category(dist_km: float) -> str:
    if dist_km < 0.2:   return "초근접"
    elif dist_km < 0.5: return "근접"
    elif dist_km < 1.0: return "보통"
    else:               return "원거리"


# ── 싱글턴: 모델 & 데이터 캐싱 ───────────────────────────────────────────────
@lru_cache(maxsize=1)
def get_artifacts():
    return load_models(DATA_DIR / "models")

@lru_cache(maxsize=1)
def get_district_lookup() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "district_lookup.csv").set_index("district")

@lru_cache(maxsize=1)
def get_cluster_listings() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "cluster_listings_ao.csv")


# ── 자치구 → lookup row ───────────────────────────────────────────────────────
def get_district_row(district_short: str) -> pd.Series:
    """'Gangnam' → district_lookup['Gangnam-gu'] 행 반환"""
    district_full = DISTRICT_NAME_MAP.get(district_short, district_short)
    lookup = get_district_lookup()
    if district_full not in lookup.index:
        # 가장 유사한 키로 폴백
        district_full = next(
            (k for k in lookup.index if district_short.lower() in k.lower()),
            lookup.index[0],
        )
    return lookup.loc[district_full]


# ── 메인 예측 서비스 ──────────────────────────────────────────────────────────
def run_predict(req) -> dict:
    """PredictRequest → predict_revpar 결과"""
    artifacts = get_artifacts()
    row = get_district_row(req.district)

    # 자치구 통계
    cluster_id = int(row["cluster"])
    cluster_label = str(row.get("cluster_name", f"클러스터 {cluster_id}"))

    # POI 거리 기본값: 자치구 평균에서 추정 (없으면 0.5km)
    poi_dist = req.nearest_poi_dist_km if req.nearest_poi_dist_km is not None else 0.5
    poi_category = get_poi_dist_category(poi_dist)
    poi_type = req.nearest_poi_type_name or "관광지"

    # room_type 정규화
    room_type_norm = ROOM_TYPE_MAP.get(req.room_type, "entire_home")

    # 월 운영비 합산
    opex_total = req.opex_monthly + req.cleaning_fee_per_stay * 8  # 월 8회 청소 가정

    listing = {
        # 자치구 통계
        "cluster":                   cluster_id,
        "district_median_revpar":    float(row["district_median_revpar"]),
        "district_listing_count":    int(row["district_listing_count"]),
        "district_superhost_rate":   float(row["district_superhost_rate"]),
        "district_entire_home_rate": float(row["district_entire_home_rate"]),
        "ttm_pop":                   int(row["ttm_pop"]),

        # 호스트 입력
        "room_type":               room_type_norm,
        "bedrooms":                req.bedrooms,
        "baths":                   req.bathrooms,
        "guests":                  req.accommodates,
        "min_nights":              req.min_nights,
        "instant_book":            int(req.instant_bookable),
        "superhost":               int(req.superhost),
        "rating_overall":          req.review_scores_rating,
        "photos_count":            req.photos,
        "num_reviews":             req.review_count,
        "extra_guest_fee_policy":  "0",
        "is_active_operating":     1,

        # POI
        "nearest_poi_dist_km":    poi_dist,
        "poi_dist_category":      poi_category,
        "nearest_poi_type_name":  poi_type,
        "photos_tier":            get_photos_tier(req.photos),
    }

    result = predict_revpar(listing, opex_per_month=opex_total, **artifacts)

    # 예약률 기반 평일/주말 분리
    # RevPAR 역산으로 실질 예약률 추정 (occ_pred가 0이면 revpar 기반 보정)
    occ = result["Occ_pred"]
    if occ < 0.01 and result["RevPAR_pred"] > 0:
        # iso_reg 보정 후 revpar로 역산
        occ = result["RevPAR_pred"] / max(result["ADR_pred"], 1)
    weekend_occ = min(1.0, occ * 1.3)
    weekday_occ = max(0.0, (occ * 7 - weekend_occ * 2) / 5)

    # 손익분기 요금: opex / (occ × 30)
    bep_rate = opex_total / max(occ * 30, 1)

    # 클러스터 내 퍼센타일 (adr_pred 기준)
    ao_df = get_cluster_listings()
    cluster_df = ao_df[ao_df["cluster"] == cluster_id]
    if "ttm_revpar" in cluster_df.columns and len(cluster_df) > 0:
        percentile = float(
            np.mean(cluster_df["ttm_revpar"] <= result["RevPAR_pred"]) * 100
        )
    else:
        percentile = 50.0

    return {
        "adr_pred":          result["ADR_pred"],
        "occ_pred":          result["Occ_pred"],
        "revpar_pred":       result["RevPAR_pred"],
        "monthly_revenue":   result["monthly_revenue"],
        "monthly_net_profit": result["net_profit"],
        "bep_rate":          bep_rate,
        "weekday_occ":       weekday_occ,
        "weekend_occ":       weekend_occ,
        "cluster_id":        cluster_id,
        "cluster_label":     cluster_label,
        "percentile_rank":   percentile,
        "revpar_trend":      result.get("revpar_trend"),
        "trend_label":       result.get("trend_label"),
    }


# ── 헬스 스코어 서비스 ────────────────────────────────────────────────────────
def run_health_score(req) -> dict:
    """PredictRequest → compute_health_score 결과 + 포맷 변환"""
    row = get_district_row(req.district)
    cluster_id = int(row["cluster"])

    ao_df = get_cluster_listings()
    cluster_listings = ao_df[ao_df["cluster"] == cluster_id]

    poi_dist = req.nearest_poi_dist_km if req.nearest_poi_dist_km is not None else 0.5

    user_vals = {
        "my_reviews":    req.review_count,
        "my_rating":     req.review_scores_rating,
        "my_photos":     req.photos,
        "my_instant":    req.instant_bookable,
        "my_min_nights": req.min_nights,
        "my_extra_fee":  False,
        "my_poi_dist":   poi_dist,
        "my_bedrooms":   req.bedrooms,
        "my_baths":      req.bathrooms,
    }

    hs = compute_health_score(user_vals, cluster_listings)

    # 컴포넌트 이름 한→영
    comp_name_map = {
        "review_signal":   "리뷰 신호",
        "listing_quality": "사진 품질",
        "booking_policy":  "예약 정책",
        "location":        "위치",
        "listing_config":  "숙소 구성",
    }

    components = [
        {
            "name":      comp_name_map.get(k, k),
            "score":     round(v, 1),
            "max_score": 100.0,
            "weight":    0.2,
            "actions":   [],
        }
        for k, v in hs["components"].items()
    ]

    return {
        "composite":   round(hs["composite"], 1),
        "grade":       hs["grade"],
        "components":  components,
        "top_actions": hs["actions"][:5],
    }


# ── 벤치마크 서비스 ───────────────────────────────────────────────────────────
def run_benchmark(district: str, room_type: str) -> dict:
    """자치구 + 룸타입 기준 벤치마크 통계"""
    room_type_norm = ROOM_TYPE_MAP.get(room_type, room_type)
    row = get_district_row(district)
    cluster_id = int(row["cluster"])

    ao_df = get_cluster_listings()
    cluster_df = ao_df[ao_df["cluster"] == cluster_id].copy()

    # ADR 추정값 (ttm_revpar 활용)
    if "ttm_revpar" in cluster_df.columns and len(cluster_df) > 10:
        revpars = cluster_df["ttm_revpar"].dropna()
        # 예약률 중앙값 추정 (~0.65)
        occ_est = 0.65
        adrs = revpars / occ_est

        return {
            "adr_p25":     float(np.percentile(adrs, 25)),
            "adr_median":  float(np.median(adrs)),
            "adr_p75":     float(np.percentile(adrs, 75)),
            "occ_p25":     0.52,
            "occ_median":  occ_est,
            "occ_p75":     0.78,
            "revpar_median": float(np.median(revpars)),
            "sample_size": len(cluster_df),
        }
    else:
        # 폴백: 자치구 통계 기반 추정
        med_revpar = float(row["district_median_revpar"])
        return {
            "adr_p25":     med_revpar * 0.75,
            "adr_median":  med_revpar / 0.65,
            "adr_p75":     med_revpar * 1.35,
            "occ_p25":     0.50,
            "occ_median":  0.65,
            "occ_p75":     0.78,
            "revpar_median": med_revpar,
            "sample_size": int(row["district_listing_count"]),
        }
