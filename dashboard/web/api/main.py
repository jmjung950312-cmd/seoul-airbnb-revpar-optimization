"""서울 에어비앤비 RevPAR 예측 FastAPI 백엔드"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers import predict, geocode, analyze
from services.model_service import get_artifacts, get_district_lookup, get_cluster_listings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """서버 시작 시 ML 모델 + 데이터 프리로드"""
    print("모델 및 데이터 로딩 중...")
    get_artifacts()           # LightGBM 모델 캐싱
    get_district_lookup()     # 자치구 룩업 캐싱
    get_cluster_listings()    # 클러스터 리스팅 캐싱
    print("준비 완료 — 모든 모델 로드됨")
    yield


app = FastAPI(
    title="서울 에어비앤비 RevPAR 예측 API",
    version="1.0.0",
    description="LightGBM 기반 서울 에어비앤비 수익 예측 API",
    lifespan=lifespan,
)

# CORS: Next.js 개발 서버 + Vercel 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(analyze.router, tags=["통합 분석"])
app.include_router(predict.router, tags=["개별 예측"])
app.include_router(geocode.router, tags=["지오코드"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "서울 에어비앤비 RevPAR API"}
