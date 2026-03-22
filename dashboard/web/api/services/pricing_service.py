"""요금 전략 추천 서비스"""

import math
from services.model_service import get_district_row


# 계절 조정 계수 (서울 기준)
SEASONAL_ADJUSTMENTS = {
    "spring": 1.08,   # 3~5월: 벚꽃 시즌
    "summer": 1.18,   # 6~8월: 여름 성수기
    "fall":   1.12,   # 9~11월: 단풍 시즌
    "winter": 0.85,   # 12~2월: 비수기
}


def build_pricing_recommendation(req, adr_pred: float, occ_pred: float) -> dict:
    """ADR 예측값 기반 요금 전략 권고안 생성"""
    row = get_district_row(req.district)
    cluster_id = int(row["cluster"])

    # 평일/주말 요금 분리
    # 주말 프리미엄: 클러스터별 차등 (핫플=1.35, 비즈니스=1.25, 기타=1.20)
    weekend_premium = {0: 1.35, 1: 1.20, 2: 1.22, 3: 1.25}.get(cluster_id, 1.20)

    # 최적 평일 요금: 사용자 목표 요금과 ML 예측값을 블렌딩하여 도출
    user_price = req.target_adr if req.target_adr else adr_pred
    price_ratio = user_price / adr_pred if adr_pred > 0 else 1.0

    if price_ratio > 1.0:
        # 목표 > 시장 예측: 점유율 가중 블렌딩 (occ 높을수록 목표에 더 근접)
        alpha = min(0.55, occ_pred * 0.85)
        optimal = adr_pred * (1 - alpha) + user_price * alpha
        weekday_price = round(min(adr_pred * 1.25, optimal) / 1000) * 1000
    else:
        # 목표 <= 시장 예측: 점유율 기반 소폭 조정
        occ_adj = max(0.90, 1.0 + (occ_pred - 0.65) * 0.25)
        weekday_price = round(adr_pred * occ_adj / 1000) * 1000

    weekend_price = round(adr_pred * weekend_premium / 1000) * 1000  # 1000원 단위 반올림

    # 성수기 배율: occ가 높을수록 성수기 탄력성 크게
    peak_multiplier = round(1.0 + min(0.6, occ_pred * 0.8), 2)

    # 할인 적용 임박 기준 (최소박 대비)
    discount_threshold = max(7, req.min_nights * 3)

    return {
        "weekday_price": weekday_price,
        "weekend_price": weekend_price,
        "peak_multiplier": peak_multiplier,
        "discount_threshold_days": discount_threshold,
        "seasonal_adjustments": SEASONAL_ADJUSTMENTS,
    }
