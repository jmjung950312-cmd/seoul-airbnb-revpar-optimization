"""지오코드 라우터: GET /geocode (Nominatim 프록시)"""

import httpx
from fastapi import APIRouter, Query, HTTPException
from schemas.predict import GeocodeResponse

router = APIRouter()

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "SeoulAirbnbDashboard/1.0"}


@router.get("/geocode", response_model=GeocodeResponse)
async def geocode(q: str = Query(..., description="검색할 주소")):
    """주소 → 위경도 변환 (Nominatim 프록시)"""
    params = {"q": q, "format": "json", "limit": 1, "accept-language": "ko"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(NOMINATIM_URL, params=params, headers=HEADERS)
            data = resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"지오코딩 서비스 오류: {e}") from e

    if not data:
        raise HTTPException(status_code=404, detail="주소를 찾을 수 없습니다")

    item = data[0]
    return GeocodeResponse(
        lat=float(item["lat"]),
        lng=float(item["lon"]),
        display_name=item["display_name"],
    )
