"""예측 라우터: POST /predict, POST /health-score, POST /benchmark"""

from fastapi import APIRouter, HTTPException
from schemas.predict import (
    PredictRequest, PredictResponse,
    HealthScoreResponse,
    BenchmarkRequest, BenchmarkResponse,
)
from services.model_service import run_predict, run_health_score, run_benchmark

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    """RevPAR 예측 + 수익 계산"""
    try:
        result = run_predict(req)
        return PredictResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/health-score", response_model=HealthScoreResponse)
async def health_score(req: PredictRequest):
    """숙소 헬스 스코어 계산"""
    try:
        result = run_health_score(req)
        return HealthScoreResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/benchmark", response_model=BenchmarkResponse)
async def benchmark(req: BenchmarkRequest):
    """자치구 + 룸타입 기준 벤치마크 통계"""
    try:
        result = run_benchmark(req.district, req.room_type)
        return BenchmarkResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
