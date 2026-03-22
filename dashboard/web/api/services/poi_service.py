"""주변 POI 서비스 — 자치구별 대표 관광지 데이터"""

import math

# 자치구별 대표 POI (실제 위경도 포함)
DISTRICT_POIS: dict[str, list[dict]] = {
    "Gangnam": [
        {"name": "코엑스몰", "category": "쇼핑", "lat": 37.5115, "lng": 127.0595},
        {"name": "강남역", "category": "교통", "lat": 37.4979, "lng": 127.0276},
        {"name": "선릉·정릉", "category": "문화", "lat": 37.5098, "lng": 127.0476},
        {"name": "청담동 패션거리", "category": "쇼핑", "lat": 37.5244, "lng": 127.0538},
        {"name": "압구정로데오", "category": "음식", "lat": 37.5273, "lng": 127.0378},
    ],
    "Jongno": [
        {"name": "경복궁", "category": "관광", "lat": 37.5796, "lng": 126.9770},
        {"name": "북촌한옥마을", "category": "문화", "lat": 37.5822, "lng": 126.9850},
        {"name": "인사동", "category": "쇼핑", "lat": 37.5744, "lng": 126.9852},
        {"name": "창덕궁", "category": "관광", "lat": 37.5824, "lng": 126.9910},
        {"name": "익선동", "category": "음식", "lat": 37.5758, "lng": 126.9986},
    ],
    "Mapo": [
        {"name": "홍대 클럽거리", "category": "문화", "lat": 37.5563, "lng": 126.9230},
        {"name": "합정역", "category": "교통", "lat": 37.5493, "lng": 126.9146},
        {"name": "망원시장", "category": "음식", "lat": 37.5561, "lng": 126.9027},
        {"name": "월드컵공원", "category": "자연", "lat": 37.5700, "lng": 126.8980},
        {"name": "연남동 카페거리", "category": "음식", "lat": 37.5641, "lng": 126.9234},
    ],
    "Yongsan": [
        {"name": "이태원", "category": "음식", "lat": 37.5340, "lng": 126.9943},
        {"name": "국립중앙박물관", "category": "문화", "lat": 37.5240, "lng": 126.9808},
        {"name": "용산역", "category": "교통", "lat": 37.5298, "lng": 126.9645},
        {"name": "해방촌", "category": "음식", "lat": 37.5449, "lng": 126.9850},
        {"name": "한강공원 이촌지구", "category": "자연", "lat": 37.5193, "lng": 126.9634},
    ],
    "Jung": [
        {"name": "명동", "category": "쇼핑", "lat": 37.5636, "lng": 126.9850},
        {"name": "남대문시장", "category": "쇼핑", "lat": 37.5592, "lng": 126.9753},
        {"name": "덕수궁", "category": "관광", "lat": 37.5659, "lng": 126.9749},
        {"name": "동대문디자인플라자", "category": "문화", "lat": 37.5670, "lng": 127.0095},
        {"name": "청계천", "category": "자연", "lat": 37.5691, "lng": 126.9779},
    ],
    "Seocho": [
        {"name": "서울예술의전당", "category": "문화", "lat": 37.4836, "lng": 127.0147},
        {"name": "교대역", "category": "교통", "lat": 37.4934, "lng": 127.0141},
        {"name": "반포한강공원", "category": "자연", "lat": 37.5109, "lng": 126.9979},
        {"name": "몽마르뜨공원", "category": "자연", "lat": 37.4931, "lng": 127.0062},
        {"name": "강남고속버스터미널", "category": "교통", "lat": 37.5048, "lng": 126.9997},
    ],
    "Songpa": [
        {"name": "잠실 롯데월드타워", "category": "관광", "lat": 37.5126, "lng": 127.1025},
        {"name": "석촌호수", "category": "자연", "lat": 37.5082, "lng": 127.0997},
        {"name": "잠실야구장", "category": "문화", "lat": 37.5121, "lng": 127.0719},
        {"name": "올림픽공원", "category": "자연", "lat": 37.5211, "lng": 127.1219},
        {"name": "송파 가락시장", "category": "음식", "lat": 37.4929, "lng": 127.1149},
    ],
    "Seongdong": [
        {"name": "성수 카페거리", "category": "음식", "lat": 37.5441, "lng": 127.0572},
        {"name": "서울숲", "category": "자연", "lat": 37.5445, "lng": 127.0374},
        {"name": "뚝섬한강공원", "category": "자연", "lat": 37.5309, "lng": 127.0640},
        {"name": "왕십리역", "category": "교통", "lat": 37.5614, "lng": 127.0369},
        {"name": "뚝도시장", "category": "음식", "lat": 37.5458, "lng": 127.0538},
    ],
}

# 기본 POI (자치구별 데이터 없을 때)
DEFAULT_POIS = [
    {"name": "지하철역", "category": "교통", "lat": 37.5665, "lng": 126.9780},
    {"name": "편의점", "category": "쇼핑", "lat": 37.5660, "lng": 126.9785},
    {"name": "한강공원", "category": "자연", "lat": 37.5280, "lng": 126.9940},
    {"name": "전통시장", "category": "음식", "lat": 37.5670, "lng": 126.9790},
    {"name": "공원", "category": "자연", "lat": 37.5660, "lng": 126.9770},
]


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (math.sin(d_lat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(d_lng / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_nearby_pois(district: str, lat: float | None, lng: float | None) -> list[dict]:
    """자치구 POI 목록 반환 (위경도 있으면 거리 계산, 없으면 기본값)"""
    pois = DISTRICT_POIS.get(district, DEFAULT_POIS)

    # 자치구 중심 좌표 (근사값)
    center_lat = lat or 37.5665
    center_lng = lng or 126.9780

    result = []
    for poi in pois:
        dist = haversine_km(center_lat, center_lng, poi["lat"], poi["lng"])
        result.append({
            "name": poi["name"],
            "category": poi["category"],
            "distance_km": round(dist, 1),
            "lat": poi["lat"],
            "lng": poi["lng"],
        })

    return sorted(result, key=lambda x: x["distance_km"])
