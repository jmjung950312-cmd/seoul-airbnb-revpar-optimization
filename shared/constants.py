"""
shared/constants.py
===================
프로젝트 전역 단일 진실 원천 (Single Source of Truth)

자치구 매핑, 숙소 유형 매핑 등 프로젝트 전반에서 사용되는 상수를 정의합니다.
host_preview, risk_detection, dashboard 등 모든 모듈은 이 파일에서 import합니다.
"""

# ──────────────────────────────────────────────
# 25개 자치구 영문(전체형) → 한글 매핑
# ──────────────────────────────────────────────
DISTRICT_KO: dict[str, str] = {
    'Gangnam-gu':      '강남구',
    'Gangdong-gu':     '강동구',
    'Gangbuk-gu':      '강북구',
    'Gangseo-gu':      '강서구',
    'Gwanak-gu':       '관악구',
    'Gwangjin-gu':     '광진구',
    'Guro-gu':         '구로구',
    'Geumcheon-gu':    '금천구',
    'Nowon-gu':        '노원구',
    'Dobong-gu':       '도봉구',
    'Dongdaemun-gu':   '동대문구',
    'Dongjak-gu':      '동작구',
    'Mapo-gu':         '마포구',
    'Seodaemun-gu':    '서대문구',
    'Seocho-gu':       '서초구',
    'Seongdong-gu':    '성동구',
    'Seongbuk-gu':     '성북구',
    'Songpa-gu':       '송파구',
    'Yangcheon-gu':    '양천구',
    'Yeongdeungpo-gu': '영등포구',
    'Yongsan-gu':      '용산구',
    'Eunpyeong-gu':    '은평구',
    'Jongno-gu':       '종로구',
    'Jung-gu':         '중구',
    'Jungnang-gu':     '중랑구',
}

# ──────────────────────────────────────────────
# 자치구 단축형 → 전체형 (Web API용: Next.js 형식 → CSV 형식)
# ──────────────────────────────────────────────
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

# ──────────────────────────────────────────────
# 숙소 유형 정규화 (UI 표시값 → 모델 입력값)
# ──────────────────────────────────────────────
ROOM_TYPE_MAP: dict[str, str] = {
    "Entire home/apt": "entire_home",
    "Private room":    "private_room",
    "Shared room":     "shared_room",
    "Hotel room":      "hotel_room",
    # 이미 정규화된 값은 통과
    "entire_home":     "entire_home",
    "private_room":    "private_room",
    "shared_room":     "shared_room",
    "hotel_room":      "hotel_room",
}

# ──────────────────────────────────────────────
# 허용 자치구 목록 (Pydantic Literal 검증용)
# ──────────────────────────────────────────────
VALID_DISTRICTS = list(DISTRICT_NAME_MAP.keys())

# ──────────────────────────────────────────────
# 모델링 상수
# ──────────────────────────────────────────────
RANDOM_SEED = 42
REVPAR_MAX = 2_000_000
AIRBNB_FEE_RATE = 0.03
DAYS_PER_MONTH = 30
AVG_MONTHLY_CLEANINGS = 8  # 월 평균 청소 횟수 가정 (occ ~65% 기준)
