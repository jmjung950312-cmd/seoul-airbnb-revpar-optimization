"""통합 분석 라우터: POST /analyze — 모든 결과를 한 번에 반환"""

import asyncio
from fastapi import APIRouter, HTTPException
from schemas.predict import PredictRequest
from schemas.analyze import AnalyzeResponse
from services.model_service import run_predict, run_health_score, run_benchmark
from services.pricing_service import build_pricing_recommendation
from services.poi_service import get_nearby_pois
from services.description_service import generate_listing_description

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: PredictRequest):
    """RevPAR 예측 + 헬스 스코어 + 벤치마크 + 요금 전략 + POI 통합 반환"""
    try:
        # 예측 / 헬스스코어 / 벤치마크를 병렬 실행
        predict_result, hs_result, bm_result = await asyncio.gather(
            asyncio.to_thread(run_predict, req),
            asyncio.to_thread(run_health_score, req),
            asyncio.to_thread(run_benchmark, req.district, req.room_type),
        )

        # 요금 전략 (예측 결과 기반)
        pricing = build_pricing_recommendation(
            req,
            predict_result["adr_pred"],
            predict_result["occ_pred"],
        )

        # 주변 POI (위경도 없으면 자치구 기본값)
        pois = get_nearby_pois(req.district, None, None)

        # 숙소 설명
        description = generate_listing_description(req, predict_result)

        return AnalyzeResponse(
            predict=predict_result,
            health_score=hs_result,
            benchmark=bm_result,
            pricing_rec=pricing,
            nearby_pois=pois,
            listing_description=description,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
