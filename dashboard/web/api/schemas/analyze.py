"""통합 분석 응답 스키마"""

from pydantic import BaseModel
from typing import Optional
from schemas.predict import PredictResponse, HealthScoreResponse, BenchmarkResponse


class PricingRecommendation(BaseModel):
    weekday_price: float
    weekend_price: float
    peak_multiplier: float
    discount_threshold_days: int
    seasonal_adjustments: dict[str, float]


class NearbyPOI(BaseModel):
    name: str
    category: str
    distance_km: float
    lat: float
    lng: float


class AnalyzeResponse(BaseModel):
    predict: PredictResponse
    health_score: HealthScoreResponse
    benchmark: BenchmarkResponse
    pricing_rec: PricingRecommendation
    nearby_pois: list[NearbyPOI]
    listing_description: str
