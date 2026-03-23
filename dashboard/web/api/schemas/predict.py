"""FastAPI 요청/응답 스키마 정의"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


# ── 예측 요청 스키마 ──────────────────────────────────────────────────────────
class PredictRequest(BaseModel):
    # 위치
    district: str = Field(..., description="자치구 영문명 (예: Gangnam)")

    # 숙소 기본
    room_type: Literal["entire_home", "private_room", "hotel_room", "shared_room"] = "entire_home"
    accommodates: int = Field(2, ge=1, le=16)
    bedrooms: int = Field(1, ge=0, le=10)
    bathrooms: float = Field(1.0, ge=0.5, le=8.0)

    # 호스트 속성
    review_scores_rating: float = Field(4.5, ge=1.0, le=5.0)
    review_count: int = Field(0, ge=0)
    photos: int = Field(10, ge=1, le=100)
    response_rate: float = Field(0.9, ge=0.0, le=1.0)
    instant_bookable: bool = True
    min_nights: int = Field(1, ge=1, le=365)

    # 호스트 유형
    host_type: Literal["new", "existing"] = "new"
    booked_days_count: Optional[int] = Field(None, ge=0, le=31)

    # 운영비 (월, 원)
    opex_monthly: float = Field(0.0, ge=0.0)
    cleaning_fee_per_stay: float = Field(30000.0, ge=0.0)
    platform_fee_rate: float = Field(0.03, ge=0.0, le=0.5)

    # POI (선택: 없으면 자치구 평균 적용)
    nearest_poi_dist_km: Optional[float] = Field(None, ge=0.0)
    nearest_poi_type_name: Optional[str] = None

    # 추가 게스트 요금 정책
    extra_guest_fee: bool = Field(False, description="추가 게스트 요금 부과 여부")

    # 슈퍼호스트 여부
    superhost: bool = False

    # 호스트 목표/현재 일평균 요금 (선택: 없으면 ML 예측값 기반 최적화)
    target_adr: Optional[float] = Field(None, ge=0.0, description="호스트의 목표/현재 일평균 요금")


# ── 예측 응답 스키마 ──────────────────────────────────────────────────────────
class PredictResponse(BaseModel):
    adr_pred: float
    occ_pred: float
    revpar_pred: float
    monthly_revenue: float
    monthly_net_profit: float
    bep_rate: float
    weekday_occ: float
    weekend_occ: float
    cluster_id: int
    cluster_label: str
    percentile_rank: float
    revpar_trend: Optional[float] = None
    trend_label: Optional[str] = None


# ── 헬스 스코어 스키마 ────────────────────────────────────────────────────────
class HealthScoreComponent(BaseModel):
    name: str
    score: float
    max_score: float
    weight: float
    actions: list[str]


class HealthScoreResponse(BaseModel):
    composite: float
    grade: str
    components: list[HealthScoreComponent]
    top_actions: list[str]


# ── 벤치마크 스키마 ───────────────────────────────────────────────────────────
class BenchmarkRequest(BaseModel):
    district: str
    room_type: str = "entire_home"


class BenchmarkResponse(BaseModel):
    adr_p25: float
    adr_median: float
    adr_p75: float
    occ_p25: float
    occ_median: float
    occ_p75: float
    revpar_median: float
    sample_size: int


# ── 지오코드 응답 ─────────────────────────────────────────────────────────────
class GeocodeResponse(BaseModel):
    lat: float
    lng: float
    display_name: str
