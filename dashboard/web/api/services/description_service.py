"""숙소 설명 생성 서비스 — 템플릿 기반"""

from services.model_service import DISTRICT_NAME_MAP

# 자치구 한글명
DISTRICT_KO: dict[str, str] = {
    "Gangnam": "강남구", "Gangdong": "강동구", "Gangbuk": "강북구", "Gangseo": "강서구",
    "Gwanak": "관악구", "Gwangjin": "광진구", "Guro": "구로구", "Geumcheon": "금천구",
    "Nowon": "노원구", "Dobong": "도봉구", "Dongdaemun": "동대문구", "Dongjak": "동작구",
    "Mapo": "마포구", "Seodaemun": "서대문구", "Seocho": "서초구", "Seongdong": "성동구",
    "Seongbuk": "성북구", "Songpa": "송파구", "Yangcheon": "양천구",
    "Yeongdeungpo": "영등포구", "Yongsan": "용산구", "Eunpyeong": "은평구",
    "Jongno": "종로구", "Jung": "중구", "Jungnang": "중랑구",
}

ROOM_TYPE_KO = {
    "entire_home": "집 전체", "private_room": "개인실",
    "shared_room": "공유실", "hotel_room": "호텔 객실",
}

CLUSTER_VIBE = {
    0: "활기찬 핫플레이스 속 감각적인",
    1: "서울 로컬의 따뜻한 분위기가 살아있는",
    2: "합리적인 가격에 접근성 좋은",
    3: "비즈니스와 여가 모두 완벽한 프리미엄",
}


def generate_listing_description(req, predict_result: dict) -> str:
    """숙소 정보 기반 한국어 숙소 설명 생성"""
    district_ko = DISTRICT_KO.get(req.district, req.district)
    cluster_id = predict_result.get("cluster_id", 2)
    vibe = CLUSTER_VIBE.get(cluster_id, "편리한 위치의")

    room_type_ko = ROOM_TYPE_KO.get(req.room_type, "숙소")
    bedrooms_str = f"침실 {req.bedrooms}개" if req.bedrooms > 0 else "스튜디오"
    guests_str = f"최대 {req.accommodates}명"

    amenity_lines = []
    if req.instant_bookable:
        amenity_lines.append("✓ 즉시 예약 가능")
    if req.min_nights <= 1:
        amenity_lines.append("✓ 1박 단기 숙박 가능")
    amenity_lines.append("✓ 고속 Wi-Fi")
    amenity_lines.append("✓ 에어컨 및 난방 완비")
    if req.bedrooms > 0:
        amenity_lines.append(f"✓ {bedrooms_str}")

    rating_str = ""
    if req.review_count >= 10:
        rating_str = f"⭐ {req.review_scores_rating:.1f} ({req.review_count}개 후기)"

    score_str = f" · 헬스 스코어 {predict_result.get('cluster_label', '')}" if predict_result.get("cluster_label") else ""

    desc = f"""{vibe} {district_ko} {room_type_ko}에 오신 것을 환영합니다.

서울 {district_ko}의 중심에 위치한 {guests_str} 수용 가능한 쾌적한 숙소입니다{score_str}.
도심의 주요 관광지, 맛집, 쇼핑 거리까지 편리하게 이동할 수 있습니다.

{chr(10).join(amenity_lines)}
{"✓ " + rating_str if rating_str else ""}

【공간 소개】
깔끔하게 정돈된 인테리어와 필수 생활용품이 완비되어 있어 마치 집처럼 편안하게 지낼 수 있습니다.
자연 채광이 풍부하고 환기가 잘 되는 쾌적한 환경입니다.

【위치 안내】
{district_ko}은 서울의 대표적인 지역으로, 대중교통 이용이 매우 편리합니다.
지하철역이 도보 거리 내에 있어 서울 전 지역 접근이 수월합니다.

【호스트 안내】
궁금한 점이 있으시면 언제든지 메시지 주세요. 빠르게 답변 드리겠습니다.
즐거운 서울 여행이 되시길 바랍니다! 🙏"""

    return desc
