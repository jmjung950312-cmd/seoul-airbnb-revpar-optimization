import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import calendar as cal_mod
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
from pathlib import Path
import sys
import requests
from streamlit_js_eval import get_geolocation

# ── 페이지 설정 ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="에어비앤비 수익 최적화",
    page_icon=":material/analytics:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── 한글 폰트 ─────────────────────────────────────────────────────────────────
def set_korean_font():
    import os
    system = platform.system()
    if system == "Darwin":
        candidates = ["AppleGothic", "Apple SD Gothic Neo"]
    elif system == "Windows":
        candidates = ["Malgun Gothic", "NanumGothic"]
    else:
        # Linux (Streamlit Cloud) — fonts-nanum 패키지에서 직접 등록
        nanum_paths = [
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "/usr/share/fonts/nanum/NanumGothic.ttf",
        ]
        for p in nanum_paths:
            if os.path.exists(p):
                fm.fontManager.addfont(p)
                font_prop = fm.FontProperties(fname=p)
                font_name = font_prop.get_name()
                plt.rcParams["font.family"] = font_name
                plt.rcParams["axes.unicode_minus"] = False
                return font_name
        candidates = ["NanumGothic", "NanumBarunGothic", "UnDotum", "DejaVu Sans"]
    available = [f.name for f in fm.fontManager.ttflist]
    for font in candidates:
        if font in available:
            plt.rcParams["font.family"] = font
            plt.rcParams["axes.unicode_minus"] = False
            return font
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False
    return "default"

set_korean_font()

# ── 테마 CSS 변수 ────────────────────────────────────────────────────────────
_is_dark = st.session_state.get("dark_mode", False)

_THEME_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

  /* ── CSS 변수: 라이트 테마 (기본) ── */
  :root {
    --bg-app: #FAFAFA;
    --bg-card: #FFFFFF;
    --bg-card-hover: #F8F8F8;
    --bg-secondary: #F2F2F2;
    --bg-coral-light: #FFF0EE;
    --text-primary: #222222;
    --text-secondary: #717171;
    --text-muted: #888888;
    --text-faint: #AAAAAA;
    --border-color: #DDDDDD;
    --border-light: #EBEBEB;
    --border-card: #E8E8E8;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.06);
    --shadow-md: 0 4px 16px rgba(0,0,0,0.08);
    --shadow-lg: 0 8px 30px rgba(0,0,0,0.12);
    --shadow-color: rgba(0,0,0,0.07);
    --shadow-light: rgba(0,0,0,0.04);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --coral: #FF5A5F;
    --coral-hover: #E8484D;
    --coral-dark: #C62828;
    --green: #2E7D32;
    --cal-weekday: #1C1C1E;
    --cal-weekday-hover-bg: #F2F2F7;
    --cal-sun-hover-bg: #FFF0EE;
    --cal-sat-hover-bg: #EEF4FF;
    --tab-bg: #F5F5F5;
    --tab-active-bg: #FFFFFF;
    --input-bg: #FFFFFF;
  }

  /* ── 웹폰트 전역 적용 ── */
  html, body, .stApp, .stMarkdown, .stButton > button,
  .stSelectbox, .stNumberInput, .stTextInput, .stCheckbox,
  h1, h2, h3, h4, h5, h6, p, div, label, input, textarea, select {
    font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif !important;
  }
""" + ("""
  /* ── CSS 변수: 다크 테마 오버라이드 ── */
  :root {
    --bg-app: #0E1117;
    --bg-card: #1A1A2E;
    --bg-card-hover: #252540;
    --bg-secondary: #1E1E32;
    --bg-coral-light: #2A1520;
    --text-primary: #FAFAFA;
    --text-secondary: #B0B0B0;
    --text-muted: #888888;
    --text-faint: #666666;
    --border-color: #333355;
    --border-light: #252540;
    --border-card: #2A2A45;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.2);
    --shadow-md: 0 4px 16px rgba(0,0,0,0.25);
    --shadow-lg: 0 8px 30px rgba(0,0,0,0.3);
    --shadow-color: rgba(0,0,0,0.3);
    --shadow-light: rgba(0,0,0,0.2);
    --coral: #FF6B6F;
    --coral-hover: #FF5A5F;
    --coral-dark: #E8484D;
    --green: #4CAF50;
    --cal-weekday: #E0E0E0;
    --cal-weekday-hover-bg: #252540;
    --cal-sun-hover-bg: #2A1520;
    --cal-sat-hover-bg: #152030;
    --tab-bg: #1A1A2E;
    --tab-active-bg: #252540;
    --input-bg: #1A1A2E;
  }
  /* 다크 모드: Streamlit 기본 요소 오버라이드 */
  .stApp { background-color: #0E1117 !important; }
  .stSelectbox > div > div,
  .stNumberInput > div > div > input {
    background-color: #1A1A2E !important; color: #FAFAFA !important;
    border-color: #333355 !important;
  }
  .stSelectbox label, .stNumberInput label, .stCheckbox label {
    color: #FAFAFA !important;
  }
  .stExpander { border-color: #333355 !important; }
  .stExpander header { color: #FAFAFA !important; }
  /* 다크 모드: 탭 텍스트 색상 */
  .stTabs [data-baseweb="tab"] { color: #B0B0B0 !important; }
  .stTabs [aria-selected="true"] { color: var(--coral) !important; }
""" if _is_dark else "") + """

  /* ── 레이아웃 ── */
  .stApp { background-color: var(--bg-app); }
  .block-container { max-width: 880px !important; padding: 1.5rem 2rem 3rem !important; }
  [data-testid="stSidebar"] { display: none !important; }
  [data-testid="collapsedControl"] { display: none !important; }

  /* 기본 버튼 */
  .stButton > button {
    background-color: var(--bg-card) !important; color: var(--text-primary) !important;
    border: 1.5px solid var(--border-color) !important; border-radius: var(--radius-sm) !important;
    padding: 12px 28px !important; font-size: 15px !important;
    font-weight: 500 !important; width: 100% !important; min-height: 48px !important;
    cursor: pointer !important; transition: all 0.2s ease !important;
  }
  .stButton > button:hover { background-color: var(--bg-card-hover) !important; }
  /* 클릭(포커스) 시 핑크 아웃라인 — 모든 버튼 공통 */
  .stButton > button:focus:not(.host-card-selected .stButton > button) {
    background: #FFF8F7 !important; color: #FF5A5F !important;
    border: 2px solid #FF5A5F !important;
    outline: none !important; box-shadow: none !important;
  }

  /* 주요 액션 버튼 — 코랄 */
  .nav-primary .stButton > button {
    background-color: var(--coral) !important; color: white !important;
    border: none !important;
  }
  .nav-primary .stButton > button:hover { background-color: var(--coral-hover) !important; }

  /* 예약된 날짜 버튼 (type="primary") — 코랄 */
  .stButton > button[data-testid="stBaseButton-primary"],
  button[kind="primary"] {
    background-color: var(--coral) !important; color: white !important;
    border: none !important;
  }
  .stButton > button[data-testid="stBaseButton-primary"]:hover,
  button[kind="primary"]:hover { background-color: var(--coral-hover) !important; }

  /* 뒤로가기 버튼 */
  .back-btn .stButton > button {
    background-color: var(--bg-card) !important; color: var(--text-primary) !important;
    border: 1.5px solid var(--border-color) !important;
  }
  .back-btn .stButton > button:hover { background-color: var(--bg-card-hover) !important; }

  /* 숙소 종류 카드 (에어비앤비 스타일) — 비선택 */
  .rt-card .stButton > button {
    background: white !important; color: #222222 !important;
    border: 1.5px solid #DDDDDD !important; border-radius: 12px !important;
    min-height: 80px !important; padding: 16px 20px !important;
    text-align: left !important; font-size: 15px !important; font-weight: 700 !important;
    transition: border-color 0.15s ease !important;
    white-space: normal !important; line-height: 1.5 !important;
  }
  .rt-card .stButton > button:hover {
    border-color: #222222 !important; background: white !important;
    color: #222222 !important;
  }
  /* 숙소 종류 카드 — 선택됨 */
  .rt-card-active .stButton > button {
    background: #FFF8F7 !important; color: #FF5A5F !important;
    border: 2px solid #FF5A5F !important; border-radius: 12px !important;
    min-height: 80px !important; padding: 16px 20px !important;
    text-align: left !important; font-size: 15px !important; font-weight: 700 !important;
    white-space: normal !important; line-height: 1.5 !important;
  }
  .rt-card-active .stButton > button:hover {
    background: #FFF0EE !important; color: #FF5A5F !important;
    border-color: #FF5A5F !important;
  }

  /* 카드 */
  .card { background: var(--bg-card); border-radius: 14px; padding: 22px 24px;
    box-shadow: 0 2px 12px var(--shadow-color); margin-bottom: 14px; }

  /* 구분선 */
  .section-divider { border: none; border-top: 1.5px solid var(--border-light); margin: 28px 0; }

  /* 숫자 강조 */
  .big-num { font-size: 30px; font-weight: 700; color: var(--coral); }

  /* 감춤 */
  #MainMenu { visibility: hidden; } footer { visibility: hidden; }

  /* 입력 요소 */
  .stSelectbox > div > div,
  .stNumberInput > div > div > input { border-radius: 8px !important; }
  .stCheckbox { margin-bottom: 4px; }

  /* 달력 탐색 버튼 — 작게 */
  .cal-nav .stButton > button {
    padding: 6px 12px !important; font-size: 14px !important;
    min-height: 36px !important; border-radius: 8px !important;
  }

  /* ── iOS 스타일 달력 날짜 버튼 공통 ── */
  .st-key-cal_grid .stButton > button {
    min-height: 44px !important; max-height: 44px !important;
    height: 44px !important;
    font-size: 14px !important; font-weight: 400 !important;
    padding: 0 !important; border: none !important;
    background: transparent !important;
    width: 100% !important; line-height: 44px !important;
    border-radius: 22px !important;
    white-space: nowrap !important; overflow: hidden !important;
  }
  /* 예약된 날짜 (primary 버튼) — 코랄 배경 유지 */
  .st-key-cal_grid .stButton > button[data-testid="stBaseButton-primary"] {
    background: var(--coral) !important; color: white !important;
    font-weight: 700 !important;
  }
  .st-key-cal_grid .stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: var(--coral-hover) !important;
  }
  .st-key-cal_grid .stButton > button p {
    margin: 0 !important; padding: 0 !important;
    line-height: 44px !important; white-space: nowrap !important;
  }
  /* 평일 */
  .cal-weekday .stButton > button { color: var(--cal-weekday) !important; }
  .cal-weekday .stButton > button:hover {
    background: var(--cal-weekday-hover-bg) !important; color: var(--coral) !important;
  }
  /* 일요일 */
  .cal-sun .stButton > button { color: #FF3B30 !important; }
  .cal-sun .stButton > button:hover { background: var(--cal-sun-hover-bg) !important; }
  /* 토요일 */
  .cal-sat .stButton > button { color: #007AFF !important; }
  .cal-sat .stButton > button:hover { background: var(--cal-sat-hover-bg) !important; }
  /* 평일 공휴일 */
  .cal-holiday .stButton > button { color: #FF3B30 !important; font-weight: 500 !important; }
  .cal-holiday .stButton > button:hover { background: var(--cal-sun-hover-bg) !important; }
  /* 예약됨 (평일) */
  .cal-booked .stButton > button {
    background: var(--coral) !important; color: white !important;
    font-weight: 700 !important;
  }
  .cal-booked .stButton > button:hover { background: var(--coral-hover) !important; }
  /* 예약됨 (일요일) */
  .cal-booked-red .stButton > button {
    background: #FF3B30 !important; color: white !important; font-weight: 700 !important;
  }
  .cal-booked-red .stButton > button:hover { background: #D62D20 !important; }
  /* 예약됨 (토요일) */
  .cal-booked-blue .stButton > button {
    background: #007AFF !important; color: white !important; font-weight: 700 !important;
  }
  .cal-booked-blue .stButton > button:hover { background: #0062CC !important; }
  /* 오늘 날짜 — 코랄 테두리 링 */
  .cal-today .stButton > button {
    box-shadow: inset 0 0 0 2px var(--coral) !important;
  }
  /* 달력 빠른 선택 버튼 — 소형 */
  .cal-quick-btn .stButton > button {
    min-height: 32px !important; max-height: 32px !important;
    padding: 2px 6px !important; font-size: 11px !important;
    font-weight: 600 !important; border-radius: 8px !important;
  }

  /* POI 뱃지 */
  .poi-badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 12px; font-weight: 600; margin-right: 4px;
  }

  /* 네비게이션 버튼 정렬 */
  div[data-testid="stMarkdownContainer"]:has(.back-btn),
  div[data-testid="stMarkdownContainer"]:has(.nav-primary) {
    height: 0 !important; min-height: 0 !important;
    overflow: hidden !important; margin: 0 !important; padding: 0 !important;
  }

  /* 탭 스타일 */
  .stTabs [data-baseweb="tab-list"] {
    gap: 6px; background: var(--tab-bg); border-radius: 12px;
    padding: 4px; border-bottom: none !important;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px !important; padding: 8px 14px !important;
    font-size: 13px !important; font-weight: 600 !important;
    color: var(--text-secondary) !important; background: transparent !important;
    border: none !important; white-space: nowrap;
  }
  .stTabs [aria-selected="true"] {
    background: var(--tab-active-bg) !important; color: var(--coral) !important;
    box-shadow: 0 2px 8px var(--shadow-color) !important;
  }
  .stTabs [data-baseweb="tab-panel"] { padding: 20px 0 0 !important; }

  /* 모든 버튼 높이 통일 (달력 버튼 제외) */
  .stButton > button { min-height: 48px !important; }
  .st-key-cal_grid .stButton > button {
    min-height: 44px !important; max-height: 44px !important; height: 44px !important;
    padding: 0 !important;
  }

  /* 숙소 종류 카드 설명 텍스트 */
  .rt-card .stButton > button p, .rt-card-active .stButton > button p {
    margin: 0 !important;
  }

  /* 인테리어 스타일 선택 버튼 — 소형 */
  [data-testid="stColumn"]:has(.style-sel-btn) .stButton > button {
    min-height: 26px !important; max-height: 26px !important;
    padding: 1px 4px !important; font-size: 11px !important;
    font-weight: 500 !important;
  }

  /* 호스트 타입 선택 — 글로벌 min-height 이후 선언 */
  .host-card-selected .stButton > button {
    background-color: var(--coral) !important;
    color: white !important;
    border: none !important;
    font-size: 17px !important;
    min-height: 100px !important; font-weight: 700 !important;
    border-radius: 14px !important;
  }
  .host-card-selected .stButton > button:hover,
  .host-card-selected .stButton > button:focus {
    background-color: var(--coral-hover) !important;
    color: white !important;
    border: none !important;
  }
  .host-card-unselected .stButton > button {
    background-color: var(--bg-card) !important; color: var(--text-primary) !important;
    border: 2px solid var(--border-color) !important; font-size: 17px !important;
    min-height: 100px !important; font-weight: 700 !important;
    border-radius: 14px !important;
  }
  .host-card-unselected .stButton > button:hover {
    border-color: var(--coral) !important; color: var(--coral) !important;
    background-color: var(--bg-coral-light) !important;
  }

  /* "현재 위치 사용" 버튼 — 코랄 아웃라인 */
  .geo-btn .stButton > button {
    background: transparent !important;
    color: var(--coral) !important;
    border: 2px solid var(--coral) !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
  }
  .geo-btn .stButton > button:hover {
    background: var(--bg-coral-light) !important;
    color: var(--coral) !important;
    border-color: var(--coral-hover) !important;
  }

  /* Step5 KPI 카드 폰트 축소 + 균형 */
  [data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 22px !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
  }
  [data-testid="stMetric"] [data-testid="stMetricLabel"] {
    font-size: 12px !important;
    font-weight: 600 !important;
  }
  [data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-size: 11px !important;
  }

  /* 히어로 섹션 */
  .hero-section {
    background: linear-gradient(135deg, #FF5A5F 0%, #E8484D 60%, #C62828 100%);
    border-radius: 20px; padding: 40px 28px 36px; text-align: center;
    margin-bottom: 28px; position: relative; overflow: hidden;
  }

  /* 테마 토글 버튼 */
  .theme-toggle .stButton > button {
    min-height: 36px !important; max-height: 36px !important;
    padding: 4px 12px !important; font-size: 13px !important;
    border-radius: 20px !important; width: auto !important;
  }
</style>
"""
st.markdown(_THEME_CSS, unsafe_allow_html=True)

# ── 상수 ─────────────────────────────────────────────────────────────────────
DISTRICT_KR = {
    "Gangnam-gu": "강남구", "Gangdong-gu": "강동구", "Gangbuk-gu": "강북구",
    "Gangseo-gu": "강서구", "Gwanak-gu": "관악구", "Gwangjin-gu": "광진구",
    "Guro-gu": "구로구", "Geumcheon-gu": "금천구", "Nowon-gu": "노원구",
    "Dobong-gu": "도봉구", "Dongdaemun-gu": "동대문구", "Dongjak-gu": "동작구",
    "Mapo-gu": "마포구", "Seodaemun-gu": "서대문구", "Seocho-gu": "서초구",
    "Seongdong-gu": "성동구", "Seongbuk-gu": "성북구", "Songpa-gu": "송파구",
    "Yangcheon-gu": "양천구", "Yeongdeungpo-gu": "영등포구", "Yongsan-gu": "용산구",
    "Eunpyeong-gu": "은평구", "Jongno-gu": "종로구", "Jung-gu": "중구",
    "Jungnang-gu": "중랑구",
}

ROOM_TYPE_KR = {
    "entire_home": "집 전체", "private_room": "개인실",
    "hotel_room": "호텔 객실", "shared_room": "다인실",
}
ROOM_TYPE_DESC = {
    "entire_home": "숙소 전체를 단독으로 사용하는 형태",
    "private_room": "침실은 개인 공간, 거실·주방은 공용",
    "hotel_room": "호텔 스타일 객실",
    "shared_room": "다른 게스트와 공간을 함께 사용",
}
ROOM_TYPE_ICONS = {
    "entire_home": ":material/home:",
    "private_room": ":material/bedroom_parent:",
    "hotel_room": ":material/hotel:",
    "shared_room": ":material/group:",
}

ROOM_STYLES = ["모던/미니멀", "빈티지/레트로", "한옥/전통", "아늑/가정적", "럭셔리/프리미엄"]

POI_TYPE_ICON = {
    "관광지": ":material/place:",
    "문화시설": ":material/museum:",
    "쇼핑": ":material/shopping_bag:",
    "음식점": ":material/restaurant:",
    "숙박": ":material/hotel:",
    "레포츠": ":material/fitness_center:",
    "여행코스": ":material/directions_walk:",
    "축제공연행사": ":material/theater_comedy:",
}

# 2026년 대한민국 공휴일 (월, 일) 기준
HOLIDAYS = {
    2026: {
        (1, 1): "신정",
        (2, 16): "설날 전날",
        (2, 17): "설날",
        (2, 18): "설날 다음날",
        (3, 1): "삼일절",
        (3, 2): "삼일절 대체",
        (5, 5): "어린이날",
        (5, 24): "부처님오신날",
        (5, 25): "부처님오신날 대체",
        (6, 3): "지방선거일",
        (6, 6): "현충일",
        (8, 15): "광복절",
        (8, 17): "광복절 대체",
        (9, 24): "추석 전날",
        (9, 25): "추석",
        (9, 26): "추석 다음날",
        (10, 3): "개천절",
        (10, 5): "개천절 대체",
        (10, 9): "한글날",
        (12, 25): "크리스마스",
    }
}

# 자치구 중심 좌표
DISTRICT_CENTERS = {
    "Dobong-gu":        (37.6576, 127.0405),
    "Dongdaemun-gu":    (37.5829, 127.0474),
    "Dongjak-gu":       (37.5005, 126.9510),
    "Eunpyeong-gu":     (37.6077, 126.9217),
    "Gangbuk-gu":       (37.6339, 127.0234),
    "Gangdong-gu":      (37.5397, 127.1347),
    "Gangnam-gu":       (37.5051, 127.0414),
    "Gangseo-gu":       (37.5551, 126.8359),
    "Geumcheon-gu":     (37.4721, 126.8964),
    "Guro-gu":          (37.4959, 126.8660),
    "Gwanak-gu":        (37.4784, 126.9403),
    "Gwangjin-gu":      (37.5434, 127.0748),
    "Jongno-gu":        (37.5767, 126.9932),
    "Jung-gu":          (37.5621, 126.9916),
    "Jungnang-gu":      (37.5948, 127.0846),
    "Mapo-gu":          (37.5555, 126.9249),
    "Nowon-gu":         (37.6477, 127.0665),
    "Seocho-gu":        (37.4948, 127.0175),
    "Seodaemun-gu":     (37.5632, 126.9356),
    "Seongbuk-gu":      (37.5943, 127.0216),
    "Seongdong-gu":     (37.5519, 127.0434),
    "Songpa-gu":        (37.5065, 127.1065),
    "Yangcheon-gu":     (37.5309, 126.8587),
    "Yeongdeungpo-gu":  (37.5178, 126.9070),
    "Yongsan-gu":       (37.5419, 126.9791),
}

CLUSTER_INFO = {
    "핫플 수익형": {
        "emoji": ":material/emoji_events:", "color": "#FF5A5F", "elasticity": -0.7,
        "desc": "외국인 관광객 수요가 높아 요금을 올려도 예약이 잘 줄지 않는 지역입니다.",
        "strategy": [
            "1박 요금 10~20% 인상 테스트 — 수요가 탄탄합니다",
            "즉시예약 반드시 켜기 — 예약 기회를 놓치지 마세요",
            "사진 20~35장 + 주변 관광지 포함 촬영",
            "영문 설명 최적화 — 외국인 게스트 유입",
            "슈퍼호스트 달성 후 요금 프리미엄 적용",
        ],
    },
    "프리미엄 비즈니스": {
        "emoji": ":material/trending_up:", "color": "#00A699", "elasticity": -0.8,
        "desc": "안정적인 수요와 높은 수익을 보이는 프리미엄 주거·상업 복합 지역입니다.",
        "strategy": [
            "현재 요금 수준 방어 — 불필요한 가격 인하 자제",
            "슈퍼호스트 + 게스트 선호 배지 달성 목표",
            "평점 4.8 이상 유지 — 리뷰 관리에 집중",
            "집 전체 형태 전환 검토 — 개인실 대비 수익 2.7배",
            "관광지·문화시설 근접성을 제목에 명시",
        ],
    },
    "로컬 주거형": {
        "emoji": ":material/balance:", "color": "#FFB400", "elasticity": -1.1,
        "desc": "공급과 수요가 균형을 이루는 안정적인 시장입니다. 운영 최적화가 핵심입니다.",
        "strategy": [
            "사진 20~35장 등록 — 클릭률 높이기가 1순위",
            "최소 숙박 2~3박 — 리뷰를 빠르게 쌓는 전략",
            "즉시예약 켜기 — 비용 없이 예약률 높이기",
            "추가 게스트 요금 없애고 1박 요금에 통합",
            "슈퍼호스트 달성 후 요금 소폭 인상",
        ],
    },
    "가성비 신흥형": {
        "emoji": ":material/shield:", "color": "#9C27B0", "elasticity": -1.5,
        "desc": "가격 경쟁이 치열한 지역입니다. 예약률 유지가 최우선 전략입니다.",
        "strategy": [
            "요금 인상 자제 — 예약률 방어가 수익 보호",
            "사진 수 늘려 클릭률 개선",
            "슈퍼호스트 배지로 가격 외 차별화",
            "최소 숙박일 줄이기 — 예약 가능한 날 늘리기",
            "추가 요금 없애 선택 유인 강화",
        ],
    },
}

# ── 데이터 로드 ───────────────────────────────────────────────────────────────
_APP_DIR = Path(__file__).parent

@st.cache_data
def load_data():
    df = pd.read_csv(_APP_DIR / "data/raw/seoul_airbnb_cleaned.csv")
    cluster_df = pd.read_csv(_APP_DIR / "data/processed/district_clustered.csv")
    df = df.merge(
        cluster_df[["district", "cluster", "cluster_name"]],
        on="district", how="left",
    )
    # active_df도 캐시에 포함 — rerun마다 재계산 방지
    active_df = df[
        (df["refined_status"] == "Active") & (df["operation_status"] == "Operating")
    ].copy()
    # POI DB도 동일 CSV에서 추출 — CSV 이중 로딩 제거
    poi_cols = ["nearest_poi_name", "nearest_poi_addr", "nearest_poi_type_name",
                "nearest_poi_lat", "nearest_poi_lng"]
    poi_df = df[poi_cols].dropna(subset=["nearest_poi_name", "nearest_poi_lat", "nearest_poi_lng"])
    poi_df = poi_df.drop_duplicates(subset=["nearest_poi_name"]).reset_index(drop=True)
    return df, cluster_df, active_df, poi_df

df, cluster_df, active_df, poi_db = load_data()

# ── 브라우저 GPS 위치 수집 (비동기 — 스크립트 레벨에서 호출해야 결과 수신 가능) ──
_browser_loc = get_geolocation()
if _browser_loc:
    st.session_state["_browser_geo"] = _browser_loc

# ── ML 모델 로드 (INTEGRATION_GUIDE.md 캐싱 패턴) ─────────────────────────────
_PKG_DIR = Path(__file__).parent / "revpar_model_package"
if str(_PKG_DIR) not in sys.path:
    sys.path.insert(0, str(_PKG_DIR))

from predict_utils import load_models, predict_revpar, compute_health_score  # noqa: E402

@st.cache_resource
def load_ml_models():
    return load_models(_PKG_DIR / "models")

@st.cache_data
def load_district_lookup():
    return pd.read_csv(str(_PKG_DIR / "district_lookup.csv")).set_index("district")

@st.cache_data
def load_cluster_listings():
    return pd.read_csv(str(_PKG_DIR / "cluster_listings_ao.csv"))

ml_artifacts       = load_ml_models()
ml_district_lookup = load_district_lookup()
ml_ao_df           = load_cluster_listings()

# ── 헬퍼 함수 ────────────────────────────────────────────────────────────────
def get_bench(district, room_type):
    return active_df[
        (active_df["district"] == district) &
        (active_df["room_type"] == room_type)
    ]

def bench_val(bench, col, default, pct=50):
    if len(bench) > 0 and col in bench.columns:
        vals = bench[col].dropna()
        if len(vals) > 0:
            return float(np.percentile(vals, pct))
    return default

def dn(district):
    return DISTRICT_KR.get(district, district)

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

KR_TO_DISTRICT = {v: k for k, v in DISTRICT_KR.items()}

def extract_district_from_text(text: str) -> str | None:
    """텍스트(주소 또는 display_name)에서 자치구 영문 키를 추출. 못 찾으면 None."""
    for kr_name, en_name in KR_TO_DISTRICT.items():
        if kr_name in text:
            return en_name
    return None

def geocode_address(address: str):
    """Nominatim 지오코딩 — (lat, lng, display_name) 반환, 실패 시 (None, None, None)"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": f"{address} 서울 대한민국", "format": "json", "limit": 1}
        headers = {"User-Agent": "SeoulAirbnbDashboard/1.0"}
        resp = requests.get(url, params=params, headers=headers, timeout=6)
        data = resp.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]
    except Exception:
        pass
    return None, None, None

def reverse_geocode(lat: float, lng: float):
    """Nominatim 역지오코딩 — 좌표 → 한국어 주소 반환"""
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {"lat": lat, "lon": lng, "format": "json", "accept-language": "ko", "zoom": 18}
        headers = {"User-Agent": "SeoulAirbnbDashboard/1.0"}
        resp = requests.get(url, params=params, headers=headers, timeout=6)
        data = resp.json()
        if "display_name" in data:
            return data["display_name"]
    except Exception:
        pass
    return None

def handle_geocode_result(address: str):
    """지오코딩 + 세션 업데이트 공통 로직"""
    detected = extract_district_from_text(address)
    if detected:
        st.session_state.district = detected
    lat, lng, disp = geocode_address(address)
    if lat:
        st.session_state.my_lat = lat
        st.session_state.my_lng = lng
        st.session_state.my_location_name = disp
        st.session_state.location_confirmed = True
        if not detected:
            detected2 = extract_district_from_text(disp)
            if detected2:
                st.session_state.district = detected2
        return True
    else:
        dc = DISTRICT_CENTERS.get(st.session_state.district)
        if dc:
            st.session_state.my_lat, st.session_state.my_lng = dc
            st.session_state.my_location_name = dn(st.session_state.district) + " (자치구 평균)"
            st.session_state.location_confirmed = True
        return False

def get_ip_geolocation():
    """IP 기반 위치 추정 — (lat, lng, display) 반환, 실패 시 (None, None, None)"""
    apis = [
        {
            "url": "http://ip-api.com/json/?fields=status,lat,lon,city,regionName&lang=ko",
            "parse": lambda d: (d["lat"], d["lon"], f"{d.get('regionName', '')} {d.get('city', '')}")
            if d.get("status") == "success" else None,
        },
        {
            "url": "https://ipapi.co/json/",
            "parse": lambda d: (float(d["latitude"]), float(d["longitude"]), f"{d.get('region', '')} {d.get('city', '')}")
            if "latitude" in d else None,
        },
    ]
    headers = {"User-Agent": "SeoulAirbnbDashboard/1.0"}
    for api in apis:
        try:
            resp = requests.get(api["url"], headers=headers, timeout=5)
            data = resp.json()
            result = api["parse"](data)
            if result:
                return result
        except Exception:
            continue
    return None, None, None

def handle_current_location():
    """현재 위치 사용 — 세션에 저장된 브라우저 GPS 우선, IP 폴백"""
    ip_display = None
    # 1순위: 브라우저 GPS (스크립트 레벨에서 수집된 결과)
    loc = st.session_state.get("_browser_geo")
    if loc and loc.get("coords"):
        lat = loc["coords"]["latitude"]
        lng = loc["coords"]["longitude"]
    else:
        # 2순위: IP 기반 (로컬에서만 유효)
        lat, lng, ip_display = get_ip_geolocation()
    if lat is None:
        return False, "위치 정보를 가져올 수 없습니다. 브라우저 위치 권한을 허용해주세요."
    # 역지오코딩으로 정확한 한국어 주소 얻기
    rev_addr = reverse_geocode(lat, lng)
    if rev_addr:
        st.session_state.my_address = rev_addr
        st.session_state.my_lat = lat
        st.session_state.my_lng = lng
        st.session_state.my_location_name = rev_addr
        st.session_state.location_confirmed = True
        det = extract_district_from_text(rev_addr)
        if det:
            st.session_state.district = det
        return True, rev_addr
    else:
        # 역지오코딩 실패 — 좌표 문자열이라도 사용
        fallback = ip_display.strip() if ip_display else f"{lat:.4f}, {lng:.4f}"
        st.session_state.my_address = fallback
        st.session_state.my_lat = lat
        st.session_state.my_lng = lng
        st.session_state.my_location_name = fallback
        st.session_state.location_confirmed = True
        det = extract_district_from_text(fallback)
        if det:
            st.session_state.district = det
        return True, fallback

def find_nearby_pois(lat, lng, max_km=2.0):
    """반경 max_km 내 POI 목록 반환 (거리 순 정렬) — NumPy 벡터화 버전"""
    R = 6371.0
    lat1 = np.radians(lat)
    lon1 = np.radians(lng)
    lat2 = np.radians(poi_db["nearest_poi_lat"].values)
    lon2 = np.radians(poi_db["nearest_poi_lng"].values)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    dists = R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    mask = dists <= max_km
    if not mask.any():
        return []

    subset = poi_db[mask].copy()
    subset_dists = dists[mask]
    subset["_dist_km"] = subset_dists
    subset = subset.sort_values("_dist_km")

    results = []
    for _, row in subset.iterrows():
        results.append({
            "name": row["nearest_poi_name"],
            "type": row["nearest_poi_type_name"] if pd.notna(row["nearest_poi_type_name"]) else "기타",
            "dist_km": row["_dist_km"],
            "dist_m": int(row["_dist_km"] * 1000),
            "addr": row["nearest_poi_addr"] if pd.notna(row.get("nearest_poi_addr")) else "",
        })
    return results

# ── session_state 초기화 ──────────────────────────────────────────────────────
def init_state():
    now = datetime.now()
    defaults = {
        # 공통
        "step": 1,
        "host_type": None,          # "new" | "existing"
        "district": "Mapo-gu",
        "room_type": None,
        # 요금
        "my_adr": None,
        "my_occ_pct": None,
        "weekday_occ_pct": 0,
        "weekend_occ_pct": 0,
        "weekdays_booked": 0,
        "weekends_booked": 0,
        "weekdays_total": 22,
        "weekends_total": 9,
        # 운영비
        "opex_elec": 80000, "opex_water": 30000, "opex_mgmt": 150000,
        "opex_net": 30000, "opex_clean": 200000, "opex_loan": 0, "opex_etc": 50000,
        # 운영 체크 (기존 호스트)
        "my_photos": None, "my_superhost": False, "my_instant": False,
        "my_extra_fee": False, "my_min_nights": None,
        "my_rating": None, "my_reviews": None,
        # 신규 호스트 숙소 정보
        "my_guests": None, "my_bedrooms": None, "my_baths_count": None,
        "my_beds": None, "my_room_style": "모던/미니멀",
        # 달력 (기존 호스트)
        "calendar_year": now.year, "calendar_month": now.month,
        "booked_days": set(),        # 현재 월 선택된 날
        # 평일/주말 요금 & 할인
        "weekday_adr": None,      # 평일 1박 요금
        "weekend_adr": None,      # 주말 1박 요금
        "weekly_discount": 0,     # 주간 할인율 (%)
        "monthly_discount": 0,    # 월간 할인율 (%)
        # 추가 요금
        "fee_cleaning": 0,        # 청소비 (1회)
        "fee_pet": 0,             # 반려동물 수수료 (1회)
        "fee_extra_guest": 0,     # 추가 게스트 수수료 (1인/1박)
        "fee_other": 0,           # 기타 수수료 (1회)
        # 달력 범위 선택
        "range_select_start": None,  # 범위 선택 시작일
        "range_select_mode": False,  # 범위 선택 모드 활성화
        # 위치
        "my_address": "",
        "my_lat": None, "my_lng": None, "my_location_name": "",
        "location_confirmed": False,
        # 테마
        "dark_mode": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── 공통 UI 컴포넌트 ─────────────────────────────────────────────────────────
def render_theme_toggle():
    """우측 상단 다크/라이트 테마 토글 버튼"""
    _dark = st.session_state.get("dark_mode", False)
    _label = "라이트" if _dark else "다크"
    _icon = ":material/light_mode:" if _dark else ":material/dark_mode:"
    tc1, tc2 = st.columns([8, 2])
    with tc2:
        pass  # theme toggle wrapper removed
        if st.button(_label, key="theme_toggle", icon=_icon):
            st.session_state.dark_mode = not _dark
            st.rerun()

def render_logo():
    render_theme_toggle()
    _tc = "var(--coral)" if not st.session_state.get("dark_mode") else "#FF6B6F"
    _sc = "var(--text-muted)"
    st.markdown(f"""
    <div style="text-align:center;padding:20px 0 4px;">
      <h2 style="color:{_tc};margin:6px 0 2px;font-weight:800;letter-spacing:-0.5px;">
        에어비앤비 수익 최적화
      </h2>
      <p style="color:{_sc};font-size:13px;margin:0;">
        서울 실운영 숙소 14,399개 데이터 기반 · 내 숙소 맞춤 분석
      </p>
    </div>
    """, unsafe_allow_html=True)

def render_hero():
    render_theme_toggle()
    st.markdown("""
    <div style="
      background: linear-gradient(135deg, #FF5A5F 0%, #E8484D 100%);
      border-radius: var(--radius-lg); padding: 48px 28px 44px; text-align: center;
      margin-bottom: 28px;
    ">
      <h1 style="color:white;font-size:30px;font-weight:800;margin:0 0 12px;
        line-height:1.3;letter-spacing:-0.5px;">
        에어비앤비 최적화 플래너
      </h1>
      <p style="color:rgba(255,255,255,0.88);font-size:14px;margin:0;letter-spacing:0.2px;">
        내 숙소에 딱 맞는 수익 전략을 3분 만에 찾아드립니다
      </p>
    </div>
    """, unsafe_allow_html=True)

def render_progress(current_step):
    host_type = st.session_state.get("host_type", "existing")
    if host_type == "new":
        labels = ["숙소 정보", "숙소 설정", "월 운영비", "분석 결과"]
        step_to_pos = {1: 1, 2: 2, 3: 3, 5: 4}
    else:
        labels = ["숙소 정보", "요금 현황", "월 운영비", "운영 체크"]
        step_to_pos = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}

    current = step_to_pos.get(current_step, current_step)
    total = len(labels)

    # 슬림한 프로그레스 바
    pct = ((current - 1) / (total - 1)) * 100 if total > 1 else 100
    html = f'<div style="margin:16px 0 8px;">'
    html += f'<div style="background:var(--border-light);border-radius:4px;height:4px;overflow:hidden;">'
    html += f'<div style="background:var(--coral);width:{pct:.0f}%;height:4px;border-radius:4px;transition:width 0.3s;"></div>'
    html += f'</div>'
    # 단계 라벨
    html += f'<div style="display:flex;justify-content:space-between;margin-top:8px;">'
    for i, label in enumerate(labels, 1):
        if i < current:
            label_color = "var(--text-secondary)"
            fw = "500"
        elif i == current:
            label_color = "var(--coral)"
            fw = "700"
        else:
            label_color = "var(--text-faint)"
            fw = "400"
        html += f'<span style="font-size:12px;color:{label_color};font-weight:{fw};">{label}</span>'
    html += '</div></div>'
    st.markdown(html, unsafe_allow_html=True)

def coral_box(content):
    st.markdown(
        f'<div style="background:var(--bg-coral-light);border-radius:10px;padding:16px 20px;margin-top:8px;">{content}</div>',
        unsafe_allow_html=True,
    )

def info_row(label, value, value_color="var(--text-primary)"):
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border-light);">'
        f'<span style="color:var(--text-secondary);font-size:14px;">{label}</span>'
        f'<span style="font-weight:600;color:{value_color};font-size:14px;">{value}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

def fmt_krw(amount):
    """금액 포맷: 음수면 -₩xxx,xxx / 양수면 ₩xxx,xxx"""
    v = int(amount)
    if v < 0:
        return f"-₩{abs(v):,}"
    return f"₩{v:,}"

def status_bar(message, level="success"):
    """level: 'success' | 'warning' | 'error'"""
    styles = {
        "success": ("#F0FAF0", "#C8E6C9", "#2E7D32"),
        "warning": ("#FFFDE7", "#FFF9C4", "#F9A825"),
        "error":   ("#FFF5F5", "#FFCDD2", "#C62828"),
    }
    bg, border, color = styles.get(level, styles["success"])
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;'
        f'background:{bg};border:1px solid {border};border-radius:10px;'
        f'padding:12px 18px;margin-top:12px;">'
        f'<div style="width:8px;height:8px;border-radius:50%;background:{color};'
        f'flex-shrink:0;"></div>'
        f'<span style="font-size:13px;font-weight:600;color:{color};">'
        f'{message}</span></div>',
        unsafe_allow_html=True,
    )

def section_title(title, subtitle=""):
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)

# ── 달력 컴포넌트 ─────────────────────────────────────────────────────────────
def render_calendar():
    """인터랙티브 달력: 예약된 날짜 클릭 선택 → 예약률 반환 (범위 선택 지원)"""
    year = st.session_state.calendar_year
    month = st.session_state.calendar_month
    days_in_month = cal_mod.monthrange(year, month)[1]
    booked = st.session_state.booked_days  # set of ints
    today = datetime.now()
    today_day = today.day if today.year == year and today.month == month else None

    # 평일/주말 일수 미리 계산 (빠른 선택에 필요)
    _weekdays_set = set()
    _weekends_set = set()
    for d in range(1, days_in_month + 1):
        dow = datetime(year, month, d).weekday()
        if dow >= 5:
            _weekends_set.add(d)
        else:
            _weekdays_set.add(d)

    # ── 카드형 컨테이너 시작 ────────────────────────────────────────────────
    st.markdown(
        '<div style="background:var(--card-bg, white);border-radius:16px;padding:20px;'
        'box-shadow:0 2px 12px var(--shadow-color, rgba(0,0,0,0.06));border:1px solid var(--border-color, #F0EEEC);">',
        unsafe_allow_html=True,
    )

    # ── 월 탐색 ──────────────────────────────────────────────────────────────
    cn1, cn2, cn3 = st.columns([1, 4, 1])
    with cn1:
        st.markdown('<div class="cal-nav">', unsafe_allow_html=True)
        if st.button("◀", key="cal_prev"):
            if month == 1:
                st.session_state.calendar_month = 12
                st.session_state.calendar_year = year - 1
            else:
                st.session_state.calendar_month -= 1
            st.session_state.booked_days = set()
            st.session_state.range_select_start = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with cn2:
        st.markdown(
            f'<div style="text-align:center;font-size:18px;font-weight:800;padding:6px 0;'
            f'color:var(--text-primary, #484848);">'
            f'{year}년 {month}월</div>',
            unsafe_allow_html=True,
        )
    with cn3:
        st.markdown('<div class="cal-nav">', unsafe_allow_html=True)
        if st.button("▶", key="cal_next"):
            if month == 12:
                st.session_state.calendar_month = 1
                st.session_state.calendar_year = year + 1
            else:
                st.session_state.calendar_month += 1
            st.session_state.booked_days = set()
            st.session_state.range_select_start = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 빠른 선택 버튼 ─────────────────────────────────────────────────────
    st.markdown(
        '<div style="display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap;">',
        unsafe_allow_html=True,
    )
    qs_cols = st.columns(5)
    with qs_cols[0]:
        st.markdown('<div class="cal-quick-btn">', unsafe_allow_html=True)
        if st.button("전체 선택", key="qs_all"):
            all_days = set(range(1, days_in_month + 1))
            if st.session_state.booked_days == all_days:
                st.session_state.booked_days = set()
            else:
                st.session_state.booked_days = all_days
            st.session_state.range_select_start = None
            st.rerun()
    with qs_cols[1]:
        st.markdown('<div class="cal-quick-btn">', unsafe_allow_html=True)
        if st.button("전체 해제", key="qs_none"):
            st.session_state.booked_days = set()
            st.session_state.range_select_start = None
            st.rerun()
    with qs_cols[2]:
        st.markdown('<div class="cal-quick-btn">', unsafe_allow_html=True)
        if st.button("평일만", key="qs_wd"):
            st.session_state.booked_days = _weekdays_set.copy()
            st.session_state.range_select_start = None
            st.rerun()
    with qs_cols[3]:
        st.markdown('<div class="cal-quick-btn">', unsafe_allow_html=True)
        if st.button("주말만", key="qs_we"):
            st.session_state.booked_days = _weekends_set.copy()
            st.session_state.range_select_start = None
            st.rerun()
    with qs_cols[4]:
        st.markdown('<div class="cal-quick-btn">', unsafe_allow_html=True)
        _range_mode = st.session_state.get("range_select_mode", False)
        _range_start = st.session_state.get("range_select_start")
        if _range_start:
            _range_label = f"범위: {_range_start}일~"
        elif _range_mode:
            _range_label = "시작일 클릭..."
        else:
            _range_label = "범위 선택"
        _is_active = _range_mode or _range_start is not None
        if st.button(_range_label, key="qs_range", type="primary" if _is_active else "secondary"):
            if _is_active:
                st.session_state.range_select_mode = False
                st.session_state.range_select_start = None
            else:
                st.session_state.range_select_mode = True
                st.session_state.range_select_start = None
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 범위 선택 안내
    _range_mode = st.session_state.get("range_select_mode", False)
    _range_start = st.session_state.get("range_select_start")
    if _range_start:
        st.info(f"{_range_start}일부터 시작 — 끝 날짜를 클릭하면 범위가 선택됩니다 (취소: 범위 선택 버튼 재클릭)", icon=":material/push_pin:")
    elif _range_mode:
        st.info("범위 시작 날짜를 클릭하세요", icon=":material/push_pin:")

    # ── 요일 헤더 — 일요일 먼저 (iOS 스타일) ────────────────────────────────
    DAY_NAMES   = ["일", "월", "화", "수", "목", "금", "토"]
    DAY_FULL    = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"]
    DAY_COLORS  = ["#FF3B30", "#555", "#555", "#555", "#555", "#555", "#007AFF"]
    header_html = '<div style="display:grid;grid-template-columns:repeat(7,1fr);margin-bottom:2px;">'
    for d, full, c in zip(DAY_NAMES, DAY_FULL, DAY_COLORS):
        header_html += (
            f'<div title="{full}" style="text-align:center;font-size:12px;font-weight:700;'
            f'color:{c};padding:8px 0 6px;letter-spacing:0.5px;">{d}</div>'
        )
    header_html += "</div>"
    header_html += '<div style="border-top:1.5px solid var(--border-color, #E8E6E3);margin-bottom:6px;"></div>'
    st.markdown(header_html, unsafe_allow_html=True)

    # ── 달력 그리드 — 일요일 시작 ────────────────────────────────────────────
    cal_mod.setfirstweekday(6)   # 6 = Sunday first
    month_cal = cal_mod.monthcalendar(year, month)
    cal_mod.setfirstweekday(0)   # 원상복구 (Monday)
    year_holidays = HOLIDAYS.get(year, {})

    with st.container(key="cal_grid"):
      for w_idx, week in enumerate(month_cal):
        cols = st.columns(7)
        for i, day in enumerate(week):
            is_sunday   = (i == 0)
            is_saturday = (i == 6)

            with cols[i]:
                if day == 0:
                    st.markdown('<div style="height:48px;"></div>', unsafe_allow_html=True)
                else:
                    is_booked  = day in booked
                    is_today   = (day == today_day)
                    hname      = year_holidays.get((month, day), "")
                    is_holiday = bool(hname)

                    # ── CSS 클래스 결정 ────────────────────────────────────
                    if is_booked:
                        css_class = "cal-booked-red" if is_sunday else (
                                    "cal-booked-blue" if is_saturday else "cal-booked")
                    elif is_sunday or (is_holiday and is_sunday):
                        css_class = "cal-sun"
                    elif is_saturday:
                        css_class = "cal-sat"
                    elif is_holiday:
                        css_class = "cal-holiday"
                    else:
                        css_class = "cal-weekday"

                    today_cls = " cal-today" if is_today else ""

                    st.markdown(f'<div class="{css_class}{today_cls}">', unsafe_allow_html=True)
                    btn_type = "primary" if is_booked else "secondary"
                    if st.button(str(day), key=f"cal_{year}_{month}_{day}",
                                 use_container_width=True, type=btn_type):
                        _rm = st.session_state.get("range_select_mode", False)
                        _rs = st.session_state.get("range_select_start")
                        if _rm and _rs is None:
                            # 범위 모드: 시작점 설정
                            st.session_state.range_select_start = day
                        elif _rs is not None:
                            # 범위 모드: 끝점 → 범위 선택/해제
                            lo, hi = min(_rs, day), max(_rs, day)
                            range_days = set(range(lo, hi + 1))
                            if range_days.issubset(booked):
                                st.session_state.booked_days -= range_days
                            else:
                                st.session_state.booked_days |= range_days
                            st.session_state.range_select_start = None
                            st.session_state.range_select_mode = False
                        else:
                            # 일반 클릭 토글
                            if day in booked:
                                st.session_state.booked_days.discard(day)
                            else:
                                st.session_state.booked_days.add(day)
                        st.rerun()

                    # ── 공휴일 이름 (버튼 아래, 15px 고정 행) ────────────────
                    if hname:
                        hcolor = "#FF3B30"
                        short  = hname if len(hname) <= 5 else hname[:4] + "…"
                        st.markdown(
                            f'<div style="text-align:center;font-size:9px;font-weight:600;'
                            f'color:{hcolor};height:15px;line-height:15px;'
                            f'overflow:hidden;white-space:nowrap;">{short}</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown('<div style="height:15px;"></div>', unsafe_allow_html=True)

        # 주 구분선 (마지막 주 제외)
        if w_idx < len(month_cal) - 1:
            st.markdown(
                '<div style="border-top:1px solid var(--border-light, #F5F3F0);margin:2px 0 4px;"></div>',
                unsafe_allow_html=True,
            )

    # ── 카드형 컨테이너 종료 ────────────────────────────────────────────────
    st.markdown('</div>', unsafe_allow_html=True)

    booked_count = len(booked)
    occ_rate = booked_count / days_in_month if days_in_month > 0 else 0

    # 평일 / 주말 분리
    weekdays_booked = len(booked & _weekdays_set)
    weekends_booked = len(booked & _weekends_set)
    weekdays_total = len(_weekdays_set)
    weekends_total = len(_weekends_set)

    weekday_occ = weekdays_booked / weekdays_total if weekdays_total > 0 else 0
    weekend_occ = weekends_booked / weekends_total if weekends_total > 0 else 0

    return (occ_rate, booked_count, days_in_month,
            weekday_occ, weekend_occ,
            weekdays_booked, weekdays_total,
            weekends_booked, weekends_total)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — 숙소 기본 정보 + 호스트 유형 선택
# ─────────────────────────────────────────────────────────────────────────────
def step1():
    render_hero()
    render_progress(1)
    section_title("1단계: 내 숙소 기본 정보", "숙소 종류와 호스팅 경험을 선택해주세요.")

    # ── 호스트 유형 선택 ──────────────────────────────────────────────────────
    st.markdown("**나는 어떤 호스트인가요?**")
    st.caption("호스팅 경험에 따라 최적화된 분석 과정이 제공됩니다.")

    ht = st.session_state.host_type
    hc1, hc2 = st.columns(2)

    with hc1:
        sel_new = ht == "new"
        if st.button("신규 호스트", key="ht_new", use_container_width=True, icon=":material/person_add:", type="primary" if sel_new else "secondary"):
            st.session_state.host_type = "new"
            st.rerun()
        st.caption("처음으로 숙소를 등록하거나 아직 예약 이력이 없어요")

    with hc2:
        sel_ex = ht == "existing"
        if st.button("기존 호스트", key="ht_existing", use_container_width=True, icon=":material/workspace_premium:", type="primary" if sel_ex else "secondary"):
            st.session_state.host_type = "existing"
            st.rerun()
        st.caption("이미 에어비앤비를 운영 중이고 예약 이력이 있어요")

    # ── 숙소 종류 (에어비앤비 스타일 카드) ──────────────────────────────────────
    st.markdown("---")
    st.markdown("**:material/home: 숙소 종류**")
    room_types = ["entire_home", "private_room", "hotel_room", "shared_room"]
    rt_c1, rt_c2 = st.columns(2)
    for idx, rt in enumerate(room_types):
        selected = st.session_state.room_type == rt
        name = ROOM_TYPE_KR.get(rt, rt)
        desc = ROOM_TYPE_DESC.get(rt, "")
        with (rt_c1 if idx % 2 == 0 else rt_c2):
            if st.button(f"{name}\n{desc}", key=f"rt_{rt}", use_container_width=True, type="primary" if selected else "secondary"):
                st.session_state.room_type = rt
                st.rerun()

    # ── 숙소 구성 (인원/침실/욕실/침대) ──────────────────────────────────────
    if st.session_state.room_type is not None:
        st.markdown("---")
        st.markdown(
            '<div style="font-weight:700;font-size:14px;color:var(--text-primary);margin:16px 0 10px;">숙소 구성</div>',
            unsafe_allow_html=True,
        )
        _s1_bench = get_bench(st.session_state.district, st.session_state.room_type)
        s1c1, s1c2, s1c3, s1c4 = st.columns(4)
        with s1c1:
            _raw_g = st.session_state.my_guests
            _def_g = max(1, int(_raw_g) if _raw_g is not None else int(bench_val(_s1_bench, "guests", 2)))
            st.session_state.my_guests = st.number_input(":material/group: 최대 숙박 인원", 1, 20, _def_g, key="s1_guests")
        with s1c2:
            _raw_br = st.session_state.my_bedrooms
            _def_br = max(1, int(_raw_br) if _raw_br is not None else int(bench_val(_s1_bench, "bedrooms", 1)))
            st.session_state.my_bedrooms = st.number_input(":material/bed: 침실 수", 0, 20, _def_br, key="s1_bedrooms")
        with s1c3:
            _raw_bt = st.session_state.my_baths_count
            _def_bt = max(1, int(_raw_bt) if _raw_bt is not None else int(bench_val(_s1_bench, "baths", 1)))
            st.session_state.my_baths_count = st.number_input(":material/shower: 욕실 수", 0, 10, _def_bt, key="s1_baths")
        with s1c4:
            _def_beds = int(st.session_state.my_beds) if st.session_state.my_beds else max(1, int(bench_val(_s1_bench, "beds", 1)))
            st.session_state.my_beds = st.number_input(":material/single_bed: 침대 수", 0, 20, _def_beds, key="s1_beds")

    if ht is None or st.session_state.room_type is None:
        missing = []
        if ht is None: missing.append("호스트 유형")
        if st.session_state.room_type is None: missing.append("숙소 종류")
        st.info(f"{'과 '.join(missing)}을 선택해주세요.", icon=":material/info:")
    else:
        if st.button("다음 단계", key="next1", use_container_width=True, type="primary", icon=":material/arrow_forward:"):
            st.session_state.step = 2
            st.rerun()

    st.caption(":material/lock: 입력하신 정보는 저장되지 않습니다 · :material/calendar_today: 데이터 기간: 2024-10 ~ 2025-09 · 32,061개 리스팅 기반")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2-NEW — 신규 호스트: 숙소 상세 설정
# ─────────────────────────────────────────────────────────────────────────────
def step2_new():
    render_logo()
    render_progress(2)
    section_title(
        "2단계: 내 숙소 설정",
        "요금·사진·수용 인원·주소를 입력해주세요. 지역 평균과 비교하여 추천 요금을 안내합니다.",
    )

    bench = get_bench(st.session_state.district, st.session_state.room_type)
    b_adr_p25 = bench_val(bench, "ttm_avg_rate", 70000, 25)

    # ── 요금 & 사진 수 ────────────────────────────────────────────────────────
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        default_adr = int(st.session_state.my_adr) if st.session_state.my_adr else int(b_adr_p25)
        my_adr = st.number_input(
            "예정 1박 요금 (원)",
            min_value=0, max_value=2_000_000,
            value=default_adr, step=5_000,
            help="처음에는 지역 하위 25% 요금으로 리뷰를 빠르게 쌓는 걸 권장합니다",
        )
        st.session_state.my_adr = my_adr

    with r1c2:
        default_ph = int(st.session_state.my_photos) if st.session_state.my_photos else 0
        my_photos = st.number_input(
            ":material/photo_camera: 등록 예정 사진 수 (장)",
            min_value=0, max_value=300, value=default_ph,
            help="최적 구간은 20~35장입니다",
        )
        st.session_state.my_photos = my_photos

    # ── 방 스타일 ─────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="font-weight:700;font-size:14px;color:var(--text-primary);margin:16px 0 8px;">인테리어 스타일</div>',
        unsafe_allow_html=True,
    )
    style_cols = st.columns(len(ROOM_STYLES))
    for i, style in enumerate(ROOM_STYLES):
        is_sel = st.session_state.my_room_style == style
        style_cols[i].markdown(
            f'<div style="text-align:center;padding:18px 8px 16px;border-radius:10px;cursor:pointer;'
            f'background:{"#FFF0EE" if is_sel else "#F7F7F7"};'
            f'border:2px solid {"#FF5A5F" if is_sel else "transparent"};">'
            f'<div style="font-size:15px;font-weight:{"700" if is_sel else "500"};'
            f'color:{"#FF5A5F" if is_sel else "#484848"};line-height:1.3;">{style}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        # 선택 버튼 — 소형
        style_cols[i].markdown(
            '<div class="style-sel-btn" style="margin-top:-6px;">',
            unsafe_allow_html=True,
        )
        if style_cols[i].button("선택" if not is_sel else ":material/check:", key=f"style_{i}", use_container_width=True):
            st.session_state.my_room_style = style
            st.rerun()
        style_cols[i].markdown("</div>", unsafe_allow_html=True)

    # ── 숙소 주소 입력 ────────────────────────────────────────────────────────
    st.markdown(
        '<hr style="border:none;border-top:1px solid var(--border-light);margin:20px 0 16px;">', unsafe_allow_html=True
    )
    st.markdown(
        '<div style="font-weight:700;font-size:14px;color:var(--text-primary);margin-bottom:4px;">숙소 주소</div>'
        '<div style="font-size:12px;color:var(--text-muted);margin-bottom:10px;">'
        '주소는 게스트에게 공개되지 않으며, 데이터 분석에만 활용됩니다.</div>',
        unsafe_allow_html=True,
    )
    addr_col, btn_col, geo_col = st.columns([4, 2, 2])
    with addr_col:
        my_address = st.text_input(
            "주소 입력",
            value=st.session_state.my_address,
            placeholder="예) 마포구 서교동, 홍대입구역, 연남동 245-3",
            label_visibility="collapsed",
        )
        st.session_state.my_address = my_address
    with btn_col:
        if st.button("위치 확인", key="geocode_btn_new", icon=":material/search:"):
            if my_address.strip():
                with st.spinner("위치 확인 중..."):
                    ok = handle_geocode_result(my_address)
                if not ok:
                    st.warning("정확한 주소를 찾지 못했습니다. 자치구 중심으로 분석합니다.")
                st.rerun()
            else:
                st.warning("주소를 입력해주세요.")
    with geo_col:
        st.markdown('<div class="geo-btn">', unsafe_allow_html=True)
        if st.button("현재 위치 사용", key="geo_btn_new", icon=":material/my_location:"):
            with st.spinner("현재 위치를 확인하는 중..."):
                ok, msg = handle_current_location()
            if ok:
                st.rerun()
            else:
                st.warning(msg)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.location_confirmed:
        district_kr = DISTRICT_KR.get(st.session_state.district, st.session_state.district)
        st.success(f"위치 확인됨: {st.session_state.my_location_name} ({district_kr})", icon=":material/check_circle:")
    else:
        st.info("주소를 입력하고 [위치 확인]을 누르거나, [현재 위치 사용]을 눌러주세요.", icon=":material/location_on:")

    # ── 네비게이션 ───────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    nc1, nc2 = st.columns(2)
    with nc1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("이전", key="back2n", use_container_width=True, icon=":material/arrow_back:"):
            st.session_state.step = 1
            st.rerun()
    with nc2:
        st.markdown('<div class="nav-primary">', unsafe_allow_html=True)
        if st.button("다음 단계", key="next2n", use_container_width=True, type="primary", icon=":material/arrow_forward:"):
            st.session_state.step = 3
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2-EXISTING — 기존 호스트: 요금 + 달력 예약률
# ─────────────────────────────────────────────────────────────────────────────
def step2_existing():
    render_logo()
    render_progress(2)
    section_title(
        "2단계: 요금 & 예약 현황",
        "평일/주말 요금을 입력하고, 지난 달 예약된 날짜를 달력에서 클릭해 선택하세요.",
    )

    bench = get_bench(st.session_state.district, st.session_state.room_type)
    b_adr = bench_val(bench, "ttm_avg_rate", 100000)

    # ── 평일/주말 요금 입력 ─────────────────────────────────────────────────
    st.markdown(
        '<div style="font-weight:700;font-size:14px;color:var(--text-primary);margin:8px 0 6px;">1박 요금 설정</div>',
        unsafe_allow_html=True,
    )
    default_adr = int(st.session_state.my_adr) if st.session_state.my_adr else int(b_adr)
    default_weekday = int(st.session_state.weekday_adr) if st.session_state.weekday_adr else default_adr
    default_weekend = int(st.session_state.weekend_adr) if st.session_state.weekend_adr else int(default_adr * 1.2)

    fc1, fc2 = st.columns(2)
    with fc1:
        weekday_adr = st.number_input(
            "평일 1박 요금 (월~목)",
            min_value=0, max_value=2_000_000,
            value=default_weekday, step=5_000,
            help="월~목요일에 적용되는 1박 요금",
        )
    with fc2:
        weekend_adr = st.number_input(
            "주말 1박 요금 (금~일)",
            min_value=0, max_value=2_000_000,
            value=default_weekend, step=5_000,
            help="금~일요일에 적용되는 1박 요금",
        )
    st.session_state.weekday_adr = weekday_adr
    st.session_state.weekend_adr = weekend_adr

    dc1, dc2 = st.columns(2)
    with dc1:
        weekly_discount = st.number_input(
            "주간 할인 % (7박 이상)",
            min_value=0, max_value=50,
            value=int(st.session_state.weekly_discount), step=1,
            help="7박 이상 연박 시 적용되는 할인율",
        )
    with dc2:
        monthly_discount = st.number_input(
            "월간 할인 % (28박 이상)",
            min_value=0, max_value=70,
            value=int(st.session_state.monthly_discount), step=1,
            help="28박 이상 장기 숙박 시 적용되는 할인율",
        )
    st.session_state.weekly_discount = weekly_discount
    st.session_state.monthly_discount = monthly_discount

    # ── 달력 예약률 + 통계 패널 (좌 70% / 우 30%) ──────────────────────────
    st.markdown(
        '<div style="font-weight:700;font-size:14px;color:var(--text-primary);margin:20px 0 6px;">예약된 날짜 선택</div>'
        '<div style="font-size:12px;color:var(--text-muted);margin-bottom:12px;">'
        '예약이 완료된 날짜를 클릭하세요. 빨간 날짜 = 예약됨 / 회색 = 비어있음</div>',
        unsafe_allow_html=True,
    )

    cal_col, stat_col = st.columns([7, 3])
    with cal_col:
        (occ_rate, booked_count, days_in_month,
         weekday_occ, weekend_occ,
         wd_booked, wd_total,
         we_booked, we_total) = render_calendar()

    st.session_state.my_occ_pct = int(occ_rate * 100)
    st.session_state.weekday_occ_pct = int(weekday_occ * 100)
    st.session_state.weekend_occ_pct = int(weekend_occ * 100)
    st.session_state.weekdays_booked = wd_booked
    st.session_state.weekends_booked = we_booked
    st.session_state.weekdays_total = wd_total
    st.session_state.weekends_total = we_total

    # effective ADR (가중평균)
    effective_adr = (weekday_adr * wd_total + weekend_adr * we_total) / days_in_month if days_in_month > 0 else weekday_adr
    st.session_state.my_adr = int(effective_adr)
    my_revpar = effective_adr * occ_rate

    # ── 우측 통계 패널 ──────────────────────────────────────────────────────
    with stat_col:
        _stat_card = (
            'background:var(--bg-card);border-radius:12px;padding:14px 12px;text-align:center;'
            'box-shadow:0 1px 4px rgba(0,0,0,0.05);border:1px solid var(--border-card);margin-bottom:10px;'
        )
        _stat_label = 'font-size:11px;color:var(--text-muted);margin-bottom:4px;'
        _stat_value = 'font-size:22px;font-weight:700;'
        _stat_sub = 'font-size:10px;color:var(--text-faint);margin-top:2px;'

        st.markdown(
            f'<div style="font-weight:700;font-size:13px;color:var(--text-primary);margin-bottom:10px;'
            f'padding-bottom:8px;border-bottom:2px solid #FF5A5F;">예약 현황</div>',
            unsafe_allow_html=True,
        )
        # 예약일 / 총 일수
        st.markdown(
            f'<div style="{_stat_card}">'
            f'<div style="{_stat_label}">예약일 / 총 일수</div>'
            f'<div style="{_stat_value}color:var(--coral);">{booked_count}일 / {days_in_month}일</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        # 평일 예약률
        wd_color = "#484848" if weekday_occ <= weekend_occ else "#FF5A5F"
        st.markdown(
            f'<div style="{_stat_card}">'
            f'<div style="{_stat_label}">평일 예약률</div>'
            f'<div style="{_stat_value}color:{wd_color};">{weekday_occ:.0%}</div>'
            f'<div style="{_stat_sub}">{wd_booked}/{wd_total}일</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        # 주말 예약률
        we_color = "#FF5A5F" if weekend_occ >= weekday_occ else "#484848"
        st.markdown(
            f'<div style="{_stat_card}">'
            f'<div style="{_stat_label}">주말 예약률</div>'
            f'<div style="{_stat_value}color:{we_color};">{weekend_occ:.0%}</div>'
            f'<div style="{_stat_sub}">{we_booked}/{we_total}일</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        # 하루 실수익
        st.markdown(
            f'<div style="{_stat_card}">'
            f'<div style="{_stat_label}">하루 실수익</div>'
            f'<div style="{_stat_value}color:var(--coral);">₩{int(my_revpar):,}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        # 유효 1박 요금
        st.markdown(
            f'<div style="{_stat_card}">'
            f'<div style="{_stat_label}">유효 1박 요금</div>'
            f'<div style="{_stat_value}color:var(--text-primary);">₩{int(effective_adr):,}</div>'
            f'<div style="{_stat_sub}">평일·주말 가중평균</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── 추가 요금 설정 (선택, expander) ─────────────────────────────────────
    with st.expander("추가 요금 설정 (선택)"):
        ef1, ef2 = st.columns(2)
        with ef1:
            fee_cleaning = st.number_input(
                "청소비 (1회)", min_value=0, max_value=500_000,
                value=int(st.session_state.fee_cleaning), step=5_000,
                help="예약 1건당 부과하는 청소비",
            )
            fee_extra_guest = st.number_input(
                "추가 게스트 (1인/1박)", min_value=0, max_value=200_000,
                value=int(st.session_state.fee_extra_guest), step=1_000,
                help="기준 인원 초과 시 1인/1박 추가 요금",
            )
        with ef2:
            fee_pet = st.number_input(
                "반려동물 (1회)", min_value=0, max_value=300_000,
                value=int(st.session_state.fee_pet), step=5_000,
                help="반려동물 동반 시 부과하는 1회 요금",
            )
            fee_other = st.number_input(
                "기타 수수료 (1회)", min_value=0, max_value=300_000,
                value=int(st.session_state.fee_other), step=5_000,
                help="체크인 수수료 등 기타 1회 비용",
            )
        st.session_state.fee_cleaning = fee_cleaning
        st.session_state.fee_pet = fee_pet
        st.session_state.fee_extra_guest = fee_extra_guest
        st.session_state.fee_other = fee_other

        # 월 추가 수입 추정
        avg_stay = max(int(st.session_state.get("my_min_nights") or 2), 2)
        est_bookings = booked_count / avg_stay if booked_count > 0 else 0
        extra_monthly = int((fee_cleaning + fee_pet + fee_other) * est_bookings + fee_extra_guest * booked_count)
        if extra_monthly > 0:
            st.markdown(
                f'<div style="font-size:12px;color:var(--coral);font-weight:600;margin-top:8px;">'
                f'※ 예상 월 추가 수입: ₩{extra_monthly:,} (예약 약 {est_bookings:.0f}회 기준)</div>',
                unsafe_allow_html=True,
            )

    # ── 네비게이션 ───────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    nc1, nc2 = st.columns(2)
    with nc1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("이전", key="back2e", use_container_width=True, icon=":material/arrow_back:"):
            st.session_state.step = 1
            st.rerun()
    with nc2:
        st.markdown('<div class="nav-primary">', unsafe_allow_html=True)
        if st.button("다음 단계", key="next2e", use_container_width=True, type="primary", icon=":material/arrow_forward:"):
            st.session_state.step = 3
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — 월 운영비 (공통)
# ─────────────────────────────────────────────────────────────────────────────
def step3():
    render_logo()
    render_progress(3)
    section_title(
        "3단계: 월 운영비 입력",
        "숙소를 운영하는 데 매달 고정으로 나가는 비용을 입력해주세요.",
    )

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**:material/bolt: 공과금 · 관리비**")
            opex_elec  = st.number_input("전기세 (원/월)",  0, 500_000,   st.session_state.opex_elec,  5_000)
            opex_water = st.number_input("수도세 (원/월)",  0, 200_000,   st.session_state.opex_water, 5_000)
            opex_mgmt  = st.number_input("관리비 (원/월)",  0, 1_000_000, st.session_state.opex_mgmt,  10_000)
            opex_net   = st.number_input("인터넷 (원/월)",  0, 100_000,   st.session_state.opex_net,   5_000)
            st.session_state.opex_elec  = opex_elec
            st.session_state.opex_water = opex_water
            st.session_state.opex_mgmt  = opex_mgmt
            st.session_state.opex_net   = opex_net

    with col2:
        with st.container(border=True):
            st.markdown("**:material/cleaning_services: 청소 · 대출 · 기타**")
            opex_clean = st.number_input("청소 비용 (원/월)",  0, 1_000_000, st.session_state.opex_clean, 10_000)
            opex_loan  = st.number_input("대출 이자 (원/월)", 0, 5_000_000, st.session_state.opex_loan,  50_000)
            opex_etc   = st.number_input("기타 비용 (원/월)", 0, 500_000,   st.session_state.opex_etc,   10_000)
            st.session_state.opex_clean = opex_clean
            st.session_state.opex_loan  = opex_loan
            st.session_state.opex_etc   = opex_etc

    total_opex = (opex_elec + opex_water + opex_mgmt + opex_net
                  + opex_clean + opex_loan + opex_etc)
    st.markdown(
        f'<div style="border:2px solid var(--coral);border-radius:12px;'
        f'padding:20px 24px;text-align:center;margin:16px 0;">'
        f'<div style="color:var(--text-muted);font-size:13px;font-weight:600;">월 총 운영비</div>'
        f'<div style="color:var(--coral);font-size:28px;font-weight:800;letter-spacing:-0.5px;margin:4px 0;">'
        f'₩{total_opex:,}</div>'
        f'<div style="color:var(--text-faint);font-size:11px;">에어비앤비 수수료 3%는 별도입니다</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    nc1, nc2 = st.columns(2)
    with nc1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("이전", key="back3", use_container_width=True, icon=":material/arrow_back:"):
            st.session_state.step = 2
            st.rerun()
    with nc2:
        st.markdown('<div class="nav-primary">', unsafe_allow_html=True)
        next_step = 5 if st.session_state.host_type == "new" else 4
        label = "분석 결과 보기" if next_step == 5 else "다음 단계"
        btn_icon = ":material/search:" if next_step == 5 else ":material/arrow_forward:"
        if st.button(label, key="next3", use_container_width=True, type="primary", icon=btn_icon):
            st.session_state.step = next_step
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — 운영 현황 체크 + 위치 입력 (기존 호스트 전용)
# ─────────────────────────────────────────────────────────────────────────────
def step4_existing():
    render_logo()
    render_progress(4)
    section_title(
        "4단계: 운영 현황 체크",
        "현재 숙소 운영 상태를 체크해주세요. 개선 포인트를 찾는 데 사용됩니다.",
    )

    bench = get_bench(st.session_state.district, st.session_state.room_type)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**:material/star: 리뷰 & 평점**")
        default_rv = int(st.session_state.my_reviews) if st.session_state.my_reviews is not None else int(bench_val(bench, "num_reviews", 20))
        my_reviews = st.number_input("현재 리뷰 수 (건)", 0, 5000, default_rv)
        st.session_state.my_reviews = my_reviews

        default_rt = float(st.session_state.my_rating) if st.session_state.my_rating is not None else round(bench_val(bench, "rating_overall", 4.70), 1)
        my_rating = st.slider("현재 평점", 0.0, 5.0, default_rt, 0.1)
        st.session_state.my_rating = my_rating

        st.markdown("**:material/workspace_premium: 배지 & 예약 설정**")
        my_superhost = st.checkbox("슈퍼호스트 배지 있음", value=bool(st.session_state.my_superhost))
        st.session_state.my_superhost = my_superhost
        my_instant = st.checkbox("즉시예약 켜져 있음", value=bool(st.session_state.my_instant))
        st.session_state.my_instant = my_instant
        my_extra_fee = st.checkbox("추가 게스트 요금 받고 있음", value=bool(st.session_state.my_extra_fee))
        st.session_state.my_extra_fee = my_extra_fee

    with col2:
        st.markdown("**:material/photo_camera: 사진 & 숙박 설정**")
        default_ph = int(st.session_state.my_photos) if st.session_state.my_photos is not None else int(bench_val(bench, "photos_count", 22))
        my_photos = st.number_input("등록된 사진 수 (장)", 0, 300, default_ph)
        st.session_state.my_photos = my_photos

        default_mn = int(st.session_state.my_min_nights) if st.session_state.my_min_nights is not None else int(bench_val(bench, "min_nights", 2))
        my_min_nights = st.number_input("최소 숙박일 (박)", 1, 365, default_mn)
        st.session_state.my_min_nights = my_min_nights

    # ── 위치 정보 (전체 너비) ────────────────────────────────────────────────
    st.markdown(
        '<hr style="border:none;border-top:1px solid var(--border-light);margin:20px 0 16px;">', unsafe_allow_html=True
    )
    st.markdown("**숙소 주소**")
    st.markdown(
        '<div style="font-size:12px;color:var(--text-muted);margin-bottom:8px;">'
        '주소는 게스트에게 공개되지 않으며, 데이터 분석에만 활용됩니다.</div>',
        unsafe_allow_html=True,
    )
    my_address = st.text_input(
        "주소",
        value=st.session_state.my_address,
        placeholder="예) 마포구 서교동, 홍대입구역, 연남동 245-3",
        label_visibility="collapsed",
        key="addr_ex",
    )
    st.session_state.my_address = my_address

    loc_btn1, loc_btn2 = st.columns(2)
    with loc_btn1:
        if st.button("위치 확인", key="geocode_btn_ex", use_container_width=True, icon=":material/search:"):
            if my_address.strip():
                with st.spinner("위치 확인 중..."):
                    ok = handle_geocode_result(my_address)
                if not ok:
                    st.warning("정확한 주소를 찾지 못했습니다. 자치구 중심으로 분석합니다.")
                st.rerun()
            else:
                st.warning("주소를 입력해주세요.")
    with loc_btn2:
        if st.button("현재 위치 사용", key="geo_btn_ex", use_container_width=True, icon=":material/my_location:"):
            with st.spinner("현재 위치를 확인하는 중..."):
                ok, msg = handle_current_location()
            if ok:
                st.rerun()
            else:
                st.warning(msg)

    if st.session_state.location_confirmed:
        district_kr = DISTRICT_KR.get(st.session_state.district, st.session_state.district)
        st.success(f"위치 확인됨: {st.session_state.my_location_name} ({district_kr})", icon=":material/check_circle:")
    else:
        st.info("주소를 입력하고 [위치 확인]을 누르거나, [현재 위치 사용]을 눌러주세요.", icon=":material/location_on:")

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    nc1, nc2 = st.columns(2)
    with nc1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("이전", key="back4", use_container_width=True, icon=":material/arrow_back:"):
            st.session_state.step = 3
            st.rerun()
    with nc2:
        st.markdown('<div class="nav-primary">', unsafe_allow_html=True)
        if st.button("분석 결과 보기", key="next4", use_container_width=True, type="primary", icon=":material/search:"):
            st.session_state.step = 5
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — 분석 결과 대시보드
# ─────────────────────────────────────────────────────────────────────────────
def step5():
    district      = st.session_state.district
    room_type     = st.session_state.room_type or "entire_home"
    host_type     = st.session_state.get("host_type", "existing")
    my_adr        = float(st.session_state.my_adr or 100000)
    my_photos     = int(st.session_state.my_photos or 0)
    my_superhost  = bool(st.session_state.my_superhost)
    my_instant    = bool(st.session_state.my_instant)
    my_extra_fee  = bool(st.session_state.my_extra_fee)
    my_min_nights = int(st.session_state.my_min_nights or 2)
    my_rating     = float(st.session_state.my_rating or 4.5)
    my_reviews    = int(st.session_state.my_reviews or 0)
    my_lat        = st.session_state.my_lat
    my_lng        = st.session_state.my_lng
    if not my_lat:
        dc = DISTRICT_CENTERS.get(district)
        if dc:
            my_lat, my_lng = dc
    my_loc_name   = st.session_state.my_location_name

    bench     = get_bench(district, room_type)
    b_adr     = bench_val(bench, "ttm_avg_rate", 100000)
    b_adr_p25 = bench_val(bench, "ttm_avg_rate", 70000, 25)
    b_adr_p75 = bench_val(bench, "ttm_avg_rate", 140000, 75)
    b_revpar  = bench_val(bench, "ttm_revpar", 40000)
    b_occ     = bench_val(bench, "ttm_occupancy", 0.40)

    # 신규 호스트 → 지역 평균 예약률 사용
    if host_type == "new":
        my_occ = b_occ
    else:
        my_occ = (st.session_state.my_occ_pct or int(b_occ * 100)) / 100

    opex_items = {
        "전기세": st.session_state.opex_elec,
        "수도세": st.session_state.opex_water,
        "관리비": st.session_state.opex_mgmt,
        "인터넷": st.session_state.opex_net,
        "청소비": st.session_state.opex_clean,
        "대출이자": st.session_state.opex_loan,
        "기타": st.session_state.opex_etc,
    }
    total_opex      = sum(opex_items.values())
    my_revpar       = my_adr * my_occ
    monthly_revenue = my_revpar * 30

    # 추가 요금 수익 계산
    _fee_cleaning     = int(st.session_state.get("fee_cleaning", 0))
    _fee_pet          = int(st.session_state.get("fee_pet", 0))
    _fee_extra_guest  = int(st.session_state.get("fee_extra_guest", 0))
    _fee_other        = int(st.session_state.get("fee_other", 0))
    _avg_stay         = max(int(st.session_state.get("my_min_nights") or 2), 2)
    _booked_days      = my_occ * 30
    _est_bookings     = _booked_days / _avg_stay if _booked_days > 0 else 0
    extra_fee_revenue = (_fee_cleaning + _fee_pet + _fee_other) * _est_bookings + _fee_extra_guest * _booked_days
    monthly_revenue   = monthly_revenue + extra_fee_revenue

    airbnb_fee      = monthly_revenue * 0.03
    net_profit      = monthly_revenue - airbnb_fee - total_opex
    # BEP(손익분기) ADR: 예약률이 0이면 계산 불가
    bep_adr         = (total_opex / 0.97) / (30 * my_occ) if my_occ > 0 else None

    d_row        = cluster_df[cluster_df["district"] == district]
    cluster_name = d_row["cluster_name"].values[0] if len(d_row) > 0 else "로컬 주거형"
    c_info       = CLUSTER_INFO.get(cluster_name, CLUSTER_INFO["로컬 주거형"])
    elasticity   = c_info["elasticity"]
    d_name       = dn(district)
    rt_name      = ROOM_TYPE_KR.get(room_type, room_type)

    # ── 헤더 ────────────────────────────────────────────────────────────────
    host_badge = "신규 호스트" if host_type == "new" else "기존 호스트"

    # ── ML 예측 계산 ─────────────────────────────────────────────────────────
    def _poi_dist_cat(d):
        if d < 0.2:  return "초근접"
        if d < 0.5:  return "근접"
        if d < 1.0:  return "보통"
        return "원거리"

    def _photos_tier(n):
        if n < 14:   return "하"
        if n < 23:   return "중하"
        if n <= 35:  return "중상"
        return "상"

    # POI 거리 계산 (위치 확인 시 실거리, 없으면 벤치마크 중위값)
    if my_lat and my_lng:
        _nearby_pois = find_nearby_pois(my_lat, my_lng, max_km=5.0)
        _poi_dist = _nearby_pois[0]["dist_km"] if _nearby_pois else 0.5
        _poi_type = _nearby_pois[0]["type"]    if _nearby_pois else "관광지"
    else:
        _poi_dist = float(bench_val(bench, "nearest_poi_dist_km", 0.5))
        _poi_type = "관광지"

    # district_lookup 조회
    _dl = ml_district_lookup.loc[district] if district in ml_district_lookup.index \
        else ml_district_lookup.iloc[0]

    _listing = {
        "cluster":                   int(_dl["cluster"]),
        "district_median_revpar":    float(_dl["district_median_revpar"]),
        "district_listing_count":    int(_dl["district_listing_count"]),
        "district_superhost_rate":   float(_dl["district_superhost_rate"]),
        "district_entire_home_rate": float(_dl["district_entire_home_rate"]),
        "ttm_pop":                   int(_dl["ttm_pop"]),
        "room_type":                 room_type,
        "bedrooms":    int(st.session_state.my_bedrooms  or bench_val(bench, "bedrooms", 1)),
        "baths":     float(st.session_state.my_baths_count or bench_val(bench, "baths", 1)),
        "guests":      int(st.session_state.my_guests    or bench_val(bench, "guests",   2)),
        "min_nights":              my_min_nights,
        "instant_book":            1 if my_instant  else 0,
        "superhost":               1 if my_superhost else 0,
        "rating_overall":          my_rating  or 4.5,
        "photos_count":            my_photos  or 0,
        "num_reviews":             my_reviews or 0,
        "extra_guest_fee_policy":  "1" if my_extra_fee else "0",
        "is_active_operating":     1,
        "nearest_poi_dist_km":     _poi_dist,
        "poi_dist_category":       _poi_dist_cat(_poi_dist),
        "nearest_poi_type_name":   _poi_type,
        "photos_tier":             _photos_tier(my_photos or 0),
        "ttm_avg_rate":            my_adr,
    }

    try:
        _ml    = predict_revpar(_listing, opex_per_month=total_opex, **ml_artifacts)
        _ml_ok = True
    except Exception:
        _ml_ok = False
        _ml    = {}

    # 헬스스코어 (기존 호스트 전용)
    if host_type == "existing":
        _cluster_id       = int(_dl["cluster"])
        _cluster_listings = ml_ao_df[ml_ao_df["cluster"] == _cluster_id]
        _user_vals = {
            "my_reviews":    my_reviews or 0,
            "my_rating":     my_rating  or 4.5,
            "my_photos":     my_photos  or 0,
            "my_instant":    my_instant,
            "my_min_nights": my_min_nights,
            "my_extra_fee":  my_extra_fee,
            "my_poi_dist":   _poi_dist,
            "my_bedrooms":   int(st.session_state.my_bedrooms   or bench_val(bench, "bedrooms", 1)),
            "my_baths":    float(st.session_state.my_baths_count or bench_val(bench, "baths",    1)),
        }
        try:
            _hs    = compute_health_score(_user_vals, _cluster_listings)
            _hs_ok = True
        except Exception:
            _hs_ok = False
            _hs    = {}
    else:
        _hs_ok = False
        _hs    = {}

    st.header(":material/analytics: 분석 결과", text_alignment="center")

    # ── 분석 요약 카드 (탭 상단) — 네이티브 컴포넌트 ─────────────────────────
    _revpar_diff_s = my_revpar - b_revpar
    _profit_val_s  = fmt_krw(net_profit)

    # 배지 행
    st.markdown(
        f":red-badge[{d_name}] :gray-badge[{rt_name}] :gray-badge[실운영 {len(bench):,}개 기준] :red-badge[{host_badge}]"
    )

    # KPI 행 — st.metric with border
    with st.container(horizontal=True):
        st.metric("현재 1박 요금", f"₩{int(my_adr):,}", border=True)
        st.metric("하루 실수익", f"₩{int(my_revpar):,}",
                  delta=f"지역 평균 대비 ₩{int(abs(_revpar_diff_s)):,}",
                  delta_color="normal" if _revpar_diff_s >= 0 else "inverse",
                  border=True)
        st.metric("월 예상 순이익", _profit_val_s,
                  delta="흑자" if net_profit >= 0 else "적자",
                  delta_color="normal" if net_profit >= 0 else "inverse",
                  border=True)
        st.metric("시장 유형", cluster_name,
                  delta=f"탄력성 {abs(elasticity):.1f}",
                  delta_color="off",
                  border=True)

    st.divider()

    # ── 탭 구성 ─────────────────────────────────────────────────────────────
    if host_type == "existing":
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            ":material/bar_chart: 수익 요약",
            ":material/lightbulb: 요금 전략",
            ":material/place: 주변 관광지",
            ":material/checklist: 운영 개선",
            ":material/location_city: 지역 진단",
            ":material/health_and_safety: 헬스 스코어",
            ":material/edit_note: 숙소 설명",
        ])
    else:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            ":material/bar_chart: 수익 요약",
            ":material/lightbulb: 요금 추천",
            ":material/place: 주변 관광지",
            ":material/location_city: 지역 진단",
            ":material/edit_note: 숙소 설명",
        ])
        tab6 = None

    # ── TAB 1: 수익 요약 (KPI + 손익계산서) ─────────────────────────────────
    with tab1:
        revpar_diff  = my_revpar - b_revpar
        bep_ok       = my_adr >= bep_adr if bep_adr is not None else False

        with st.container(horizontal=True):
            st.metric("하루 평균 실수익", f"₩{int(my_revpar):,}",
                      delta=f"지역 평균 대비 ₩{int(abs(revpar_diff)):,}",
                      delta_color="normal" if revpar_diff >= 0 else "inverse",
                      border=True)
            _pv = fmt_krw(net_profit)
            st.metric("월 예상 순이익", _pv,
                      delta="흑자" if net_profit > 0 else "적자",
                      delta_color="normal" if net_profit > 0 else "inverse",
                      border=True)
            if bep_adr is not None:
                st.metric("적자 예방 최소 요금", f"₩{int(bep_adr):,}",
                          delta=f"현재 요금 {'이상 — 흑자' if bep_ok else '이하 — 손실 위험'}",
                          delta_color="normal" if bep_ok else "inverse",
                          border=True)
            else:
                st.metric("적자 예방 최소 요금", "계산 불가",
                          delta="BEP 계산 불가 — 예약이 없으면 손익분기를 달성할 수 없습니다",
                          delta_color="off",
                          border=True)
        st.caption("※ 적자 예방 최소 요금 = 운영비 + 수수료를 모두 커버하려면 1박에 최소 이 금액이 필요합니다")

        if host_type == "new":
            st.info(f"신규 호스트는 실제 예약 데이터가 없어 지역 평균 예약률({b_occ:.0%})로 계산했습니다.")

        # ── 평일 / 주말 예약률 + 수익 비교 (기존 호스트) ────────────────────
        if host_type == "existing":
            wd_occ_pct = st.session_state.get("weekday_occ_pct", 0)
            we_occ_pct = st.session_state.get("weekend_occ_pct", 0)
            wd_booked_n = st.session_state.get("weekdays_booked", 0)
            we_booked_n = st.session_state.get("weekends_booked", 0)
            wd_total_n  = st.session_state.get("weekdays_total", 22)
            we_total_n  = st.session_state.get("weekends_total", 9)
            overall_pct = int(my_occ * 100)

            # 평일/주말 개별 요금 반영
            _wd_adr = float(st.session_state.get("weekday_adr") or my_adr)
            _we_adr = float(st.session_state.get("weekend_adr") or my_adr)
            # 월 매출 분리
            wd_revenue_n = _wd_adr * wd_booked_n
            we_revenue_n = _we_adr * we_booked_n
            # 하루 기대 수익 (RevPAR) = 요금 × 예약률
            wd_revpar_n = _wd_adr * (wd_occ_pct / 100)
            we_revpar_n = _we_adr * (we_occ_pct / 100)
            # 색상 — 전체 대비 높으면 강조
            wd_col = "#2E7D32" if wd_occ_pct >= overall_pct else "#767676"
            we_col = "#FF5A5F" if we_occ_pct >= overall_pct else "#767676"

            # 예약률 3분할 카드
            with st.container(horizontal=True):
                st.metric("전체 예약률", f"{overall_pct}%",
                          delta=f"지역 평균 {b_occ:.0%}", delta_color="off", border=True)
                st.metric("평일 예약률", f"{wd_occ_pct}%",
                          delta=f"{wd_total_n}일 중 {wd_booked_n}일 예약", delta_color="off", border=True)
                st.metric("주말 예약률", f"{we_occ_pct}%",
                          delta=f"{we_total_n}일 중 {we_booked_n}일 예약", delta_color="off", border=True)

            # 평일 / 주말 수익 비교 카드
            _wd_c, _we_c = st.columns(2)
            with _wd_c:
                with st.container(border=True):
                    st.markdown("**평일 수익**")
                    st.metric("하루 기대 수익", f"₩{int(wd_revpar_n):,}")
                    st.metric("이달 평일 매출", f"₩{int(wd_revenue_n):,}")
            with _we_c:
                with st.container(border=True):
                    st.markdown("**주말 수익**")
                    st.metric("하루 기대 수익", f"₩{int(we_revpar_n):,}")
                    st.metric("이달 주말 매출", f"₩{int(we_revenue_n):,}")
            # 한 줄 인사이트
            if we_booked_n > 0 and wd_booked_n > 0:
                diff_pct = abs(we_revpar_n - wd_revpar_n) / max(wd_revpar_n, 1) * 100
                if we_revpar_n > wd_revpar_n:
                    insight = f"주말 하루 수익이 평일보다 {diff_pct:.0f}% 높습니다. 주말 요금 인상을 검토해보세요."
                    st.info(insight, icon=":material/lightbulb:")
                else:
                    insight = f"평일 하루 수익이 주말보다 {diff_pct:.0f}% 높습니다. 평일 예약 확보 전략이 효과적입니다."
                    st.success(insight, icon=":material/lightbulb:")

        st.subheader("월 손익 계산서")
        st.caption("이번 달 예상 수익 구조입니다.")

        col_pnl, col_pie = st.columns(2)
        with col_pnl:
            with st.container(border=True):
                st.markdown("**손익 내역**")
                rows = [
                    ("월 매출", f"₩{int(monthly_revenue):,}"),
                    ("에어비앤비 수수료 (3%)", f"- ₩{int(airbnb_fee):,}"),
                    ("월 운영비", f"- ₩{int(total_opex):,}"),
                ]
                for label, value in rows:
                    _l, _v = st.columns([2, 1])
                    _l.markdown(f":small[{label}]")
                    _v.markdown(f"**{value}**")
                st.markdown("---")
                _nl, _nv = st.columns([2, 1])
                _nl.markdown("**월 순이익**")
                _nv.markdown(f"**{fmt_krw(net_profit)}**")

            if net_profit > 0:
                st.success(f"월 {fmt_krw(net_profit)} 흑자", icon=":material/check_circle:")
            elif net_profit == 0:
                st.warning("정확히 본전 상태", icon=":material/info:")
            else:
                st.error(f"월 ₩{int(abs(net_profit)):,} 적자 — 요금 인상 또는 운영비 절감 필요", icon=":material/error:")

        with col_pie:
            nonzero = {k: v for k, v in opex_items.items() if v > 0}
            if nonzero and total_opex > 0:
                fig, ax = plt.subplots(figsize=(4.5, 4))
                colors = ["#4A6CF7","#6C5CE7","#00B894","#FDCB6E","#E17055","#74B9FF","#A29BFE"]
                wedges, texts, autotexts = ax.pie(
                    nonzero.values(), autopct="%1.0f%%",
                    startangle=90, colors=colors[:len(nonzero)],
                    textprops={"fontsize": 10},
                    wedgeprops={"width": 0.45, "linewidth": 1, "edgecolor": "white"},
                    pctdistance=0.76,
                )
                for t in autotexts:
                    t.set_color("white")
                    t.set_fontweight("bold")
                ax.text(0, 0.06, f"₩{total_opex:,}", ha="center", va="center",
                        fontsize=14, fontweight="bold", color="#484848")
                ax.text(0, -0.12, "월 운영비", ha="center", va="center",
                        fontsize=10, color="#888")
                ax.legend(nonzero.keys(), loc="upper center",
                          bbox_to_anchor=(0.5, -0.02), ncol=min(len(nonzero), 3),
                          fontsize=9, frameon=False)
                fig.patch.set_facecolor("none")
                fig.tight_layout()
                st.pyplot(fig)
                plt.close()
            else:
                st.info("운영비를 입력하면 구성 차트가 표시됩니다.")

    # ── TAB 2: 요금 전략 ─────────────────────────────────────────────────────
    with tab2:
        section_title(":material/lightbulb: 내 숙소에 맞는 적정 요금")

        if my_superhost and my_rating >= 4.8 and my_reviews >= 50:
            s_color = "#FF5A5F"
            rec_min, rec_max = int(b_adr), int(b_adr_p75)
            s_tip = "현재 요금이 지역 평균보다 낮다면 10~20% 인상을 테스트해보세요."
            s_tier = "프리미엄 호스트"
            s_tier_reason = "슈퍼호스트 + 평점 4.8 이상 + 리뷰 50건 이상"
            s_tier_range = "지역 평균 ~ 상위 25%"
        elif my_reviews >= 10 and my_rating >= 4.5:
            s_color = "#00A699"
            rec_min, rec_max = int(b_adr_p25), int(b_adr)
            s_tip = "슈퍼호스트 달성 후 요금을 지역 평균 이상으로 올릴 수 있습니다."
            s_tier = "성장 호스트"
            s_tier_reason = "평점 4.5 이상 + 리뷰 10건 이상"
            s_tier_range = "하위 25% ~ 지역 평균"
        else:
            s_color = "#2196F3"
            rec_min = max(int(bep_adr) if bep_adr is not None else 0, int(b_adr_p25 * 0.85))
            rec_max = int(b_adr_p25)
            s_tip = "하위 25% 요금으로 첫 10건의 리뷰를 빠르게 쌓은 후 요금을 올리세요."
            s_tier = "신규 진입"
            s_tier_reason = "리뷰 10건 미만 또는 평점 4.5 미만"
            s_tier_range = "본전 요금 ~ 하위 25%"

        # ── 단일 적정 요금 카드 ──────────────────────────────────────────────
        _bep_label = f'₩{int(bep_adr):,}' if bep_adr is not None else '계산 불가'
        _bep_span = f'<span style="font-size:11px;color:var(--text-faint);">본전 {_bep_label}</span>'
        st.markdown(
            f'<div style="background:var(--bg-card);border:2px solid {s_color};border-radius:16px;'
            f'padding:28px 24px;text-align:center;margin-bottom:16px;'
            f'box-shadow:0 3px 16px rgba(0,0,0,0.07);">'
            f'<div style="font-size:12px;color:var(--text-muted);margin-bottom:4px;">'
            f'{d_name} {rt_name} · 실운영 {len(bench):,}개 데이터 기반</div>'
            f'<div style="display:inline-block;background:{s_color}15;color:{s_color};'
            f'font-size:12px;font-weight:700;padding:3px 12px;border-radius:20px;margin-bottom:10px;">'
            f'{s_tier}</div>'
            f'<div style="font-size:14px;font-weight:700;color:var(--text-primary);margin-bottom:10px;">내 숙소 적정 1박 요금</div>'
            f'<div style="font-size:40px;font-weight:800;color:{s_color};letter-spacing:-1px;">'
            f'₩{rec_min:,} ~ ₩{rec_max:,}</div>'
            f'<div style="display:flex;justify-content:center;gap:18px;margin-top:14px;flex-wrap:wrap;">'
            f'{_bep_span}'
            f'<span style="font-size:11px;color:var(--text-faint);">하위25% ₩{int(b_adr_p25):,}</span>'
            f'<span style="font-size:11px;color:var(--text-faint);">지역 평균 ₩{int(b_adr):,}</span>'
            f'<span style="font-size:11px;color:var(--text-faint);">상위25% ₩{int(b_adr_p75):,}</span>'
            f'</div>'
            f'<div style="font-size:11px;color:var(--text-faint);margin-top:12px;border-top:1px solid var(--border-light);padding-top:10px;">'
            f'내 조건({s_tier_reason})에 따라 <b style="color:var(--text-secondary);">{s_tier_range}</b> 구간을 추천합니다</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if my_adr < rec_min:
            st.info(f"현재 요금 ₩{int(my_adr):,}이 적정 구간보다 ₩{rec_min - int(my_adr):,} 낮습니다. {s_tip}", icon=":material/arrow_upward:")
        elif my_adr > rec_max:
            st.warning(f"현재 요금 ₩{int(my_adr):,}이 적정 구간보다 ₩{int(my_adr) - rec_max:,} 높습니다. {s_tip}", icon=":material/warning:")
        else:
            st.success(f"현재 요금이 적정 구간 안에 있습니다. 잘 하고 계세요! {s_tip}", icon=":material/check_circle:")

        # ── 예상 수익 최적화 가이드 (ML) ──────────────────────────────────────────
        if _ml_ok:
            st.subheader("예상 수익 최적화 가이드")
            st.caption("서울 실운영 14,399개 리스팅 데이터 기반 시장 적정값입니다.")

            adr_diff   = _ml["ADR_pred"]   - my_adr
            occ_diff   = _ml["Occ_pred"]   - my_occ
            revp_diff  = _ml["RevPAR_pred"] - my_revpar

            with st.container(horizontal=True):
                st.metric("시장 적정 1박 요금", f"₩{int(_ml['ADR_pred']):,}",
                          delta=f"내 요금 대비 ₩{int(abs(adr_diff)):,}",
                          delta_color="normal" if adr_diff >= 0 else "inverse",
                          border=True)
                st.metric("시장 적정 예약률", f"{_ml['Occ_pred']:.1%}",
                          delta=f"내 예약률 대비 {abs(occ_diff)*100:.1f}%p",
                          delta_color="normal" if occ_diff >= 0 else "inverse",
                          border=True)
                st.metric("시장 적정 하루 실수익", f"₩{int(_ml['RevPAR_pred']):,}",
                          delta=f"현재 대비 ₩{int(abs(revp_diff)):,}",
                          delta_color="normal" if revp_diff >= 0 else "inverse",
                          border=True)

            ml_net = _ml["net_profit"]
            with st.container(border=True):
                _mc1, _mc2, _mc3 = st.columns(3)
                _mc1.metric("시장 적정 월 수익", f"₩{int(_ml['monthly_revenue']):,}")
                _mc2.metric("시장 적정 월 순이익", fmt_krw(ml_net))
                _mc3.caption(f"운영비 ₩{int(total_opex):,} 반영")

        # ── 요금 시뮬레이션 ─────────────────────────────────────────────────────
        if _ml_ok:
            sim_label = "예상 수익 시뮬레이션" if host_type == "new" else "요금 변경 시뮬레이션"
            st.subheader(f":material/bar_chart: {sim_label}")
            st.caption("1박 요금을 조정하면 ML 모델이 예약률과 수익을 재예측합니다.")

            adr_pred = _ml["ADR_pred"]
            delta_pct = st.slider("요금 변화율 (%)", -50, 100, 0, 1)
            sim_adr = int(my_adr * (1 + delta_pct / 100))

            gap_ratio = abs(sim_adr - adr_pred) / adr_pred if adr_pred > 0 else 0
            if gap_ratio > 0.5:
                st.warning("시장 적정가 대비 50% 이상 차이 나는 구간입니다. 예측 정확도가 낮을 수 있습니다.", icon=":material/warning:")

            sim_result = predict_revpar(
                {**_listing, "ttm_avg_rate": sim_adr},
                opex_per_month=total_opex, **ml_artifacts
            )
            sim_net  = sim_result["net_profit"]
            sim_occ  = sim_result["Occ_pred"]
            sim_revp = sim_result["RevPAR_pred"]

            pct_range = np.linspace(-50, 100, 40)
            price_range = my_adr * (1 + pct_range / 100)

            # 시뮬레이션 커브를 session_state에 캐싱 — 슬라이더 변경 시 재계산 방지
            _sim_cache_key = f"{hash(frozenset(_listing.items()))}_{my_adr}_{total_opex}"
            if st.session_state.get("_sim_cache_key") != _sim_cache_key:
                _sim_profits_cache = []
                for _p in price_range:
                    _r = predict_revpar({**_listing, "ttm_avg_rate": _p}, opex_per_month=total_opex, **ml_artifacts)
                    _sim_profits_cache.append(_r["net_profit"])
                st.session_state["_sim_cache_key"] = _sim_cache_key
                st.session_state["_sim_profits_cache"] = _sim_profits_cache
            sim_profits = st.session_state["_sim_profits_cache"]

            cs1, cs2 = st.columns(2)
            with cs1:
                if host_type == "existing":
                    cur_label = "현재"
                    sim_rows = [
                        ("1박 요금",    f"₩{int(my_adr):,}",   f"₩{int(sim_adr):,}",  f"{(sim_adr/my_adr-1)*100:+.1f}%"),
                        ("예약률",      f"{my_occ:.0%}",        f"{sim_occ:.0%}",       f"{(sim_occ-my_occ)*100:+.1f}%p"),
                        ("하루 실수익", f"₩{int(my_revpar):,}", f"₩{int(sim_revp):,}", f"{(sim_revp/my_revpar-1)*100:+.1f}%" if my_revpar > 0 else "-"),
                        ("월 순이익",   fmt_krw(net_profit),    fmt_krw(sim_net),       f"₩{sim_net - net_profit:+,.0f}"),
                    ]
                else:
                    cur_label = "ML 기본 예측"
                    ml_occ_base  = _ml["Occ_pred"]
                    ml_revp_base = _ml["RevPAR_pred"]
                    ml_net_base  = _ml["net_profit"]
                    sim_rows = [
                        ("1박 요금",    f"₩{int(my_adr):,}",       f"₩{int(sim_adr):,}",  f"{(sim_adr/my_adr-1)*100:+.1f}%"),
                        ("예약률",      f"{ml_occ_base:.0%}",       f"{sim_occ:.0%}",       f"{(sim_occ-ml_occ_base)*100:+.1f}%p"),
                        ("하루 실수익", f"₩{int(ml_revp_base):,}", f"₩{int(sim_revp):,}", f"{(sim_revp/ml_revp_base-1)*100:+.1f}%" if ml_revp_base > 0 else "-"),
                        ("월 순이익",   fmt_krw(ml_net_base),       fmt_krw(sim_net),       f"₩{sim_net - ml_net_base:+,.0f}"),
                    ]

                html = ('<div style="background:var(--bg-card);border-radius:12px;padding:20px;'
                        'box-shadow:0 2px 10px rgba(0,0,0,0.06);">'
                        '<div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;'
                        'color:var(--text-muted);font-size:12px;font-weight:600;padding-bottom:8px;'
                        'border-bottom:1.5px solid #F0F0F0;margin-bottom:4px;">'
                        f'<span style="padding-right:8px;">항목</span><span style="text-align:right;padding:0 8px;border-left:1px solid var(--border-light);">{cur_label}</span>'
                        '<span style="text-align:right;padding:0 8px;border-left:1px solid var(--border-light);">시뮬레이션</span>'
                        '<span style="text-align:right;padding:0 8px;border-left:1px solid var(--border-light);">변화</span></div>')
                for label, cur, nxt, chg in sim_rows:
                    w = "700" if "순이익" in label else "400"
                    chg_c = "#2E7D32" if ("+" in chg and "₩-" not in chg) else "#C62828" if ("-" in chg and "₩+" not in chg) else "#484848"
                    html += (f'<div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;'
                             f'padding:9px 0;border-bottom:1px solid var(--border-light);font-weight:{w};">'
                             f'<span style="font-size:13px;padding-right:8px;">{label}</span>'
                             f'<span style="text-align:right;font-size:13px;padding:0 8px;border-left:1px solid var(--border-light);">{cur}</span>'
                             f'<span style="text-align:right;font-size:13px;padding:0 8px;border-left:1px solid var(--border-light);">{nxt}</span>'
                             f'<span style="text-align:right;font-size:13px;padding:0 8px;border-left:1px solid var(--border-light);color:{chg_c};">{chg}</span></div>')
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)

                base_net = net_profit if host_type == "existing" else _ml["net_profit"]
                p_change = sim_net - base_net
                if delta_pct == 0:
                    st.info("슬라이더를 움직여 요금 변화 효과를 확인하세요.", icon=":material/info:")
                elif p_change > 0:
                    st.success(f"순이익 ₩{p_change:+,.0f} 증가", icon=":material/check_circle:")
                else:
                    st.warning(f"순이익 ₩{abs(p_change):,.0f} 감소", icon=":material/warning:")

            with cs2:
                fig4, ax4 = plt.subplots(figsize=(5, 3.8))
                adr_pred_pct = (adr_pred / my_adr - 1) * 100
                ax4.plot(pct_range, sim_profits, color="#FF5A5F", linewidth=2.5)
                ax4.axhline(0, color="#767676", linestyle="--", lw=1.2, alpha=0.6, label="손익분기선")
                ax4.axvline(delta_pct, color="#FFB400", linestyle="--", lw=1.5, label=f"현재 ({delta_pct:+d}%)")
                ax4.scatter([delta_pct], [sim_net], color="#FFB400", s=70, zorder=6)
                ax4.axvline(adr_pred_pct, color="#2196F3", linestyle=":", lw=1.5, label=f"시장 적정가 ({adr_pred_pct:+.0f}%)")
                ax4.fill_between(pct_range, sim_profits, 0, where=[p > 0 for p in sim_profits], alpha=0.07, color="#4CAF50")
                ax4.fill_between(pct_range, sim_profits, 0, where=[p <= 0 for p in sim_profits], alpha=0.07, color="#FF5A5F")
                ax4.set_xlabel("요금 변화율 (%)"); ax4.set_ylabel("월 순이익 (원)")
                ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:+.0f}%"))
                ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"₩{y/10000:.0f}만"))
                ax4.legend(fontsize=8)
                ax4.spines["top"].set_visible(False); ax4.spines["right"].set_visible(False)
                ax4.set_facecolor("none"); fig4.patch.set_facecolor("none")
                fig4.tight_layout()
                st.pyplot(fig4); plt.close()
                best_idx  = int(np.argmax(sim_profits))
                best_pct  = pct_range[best_idx]
                best_adr  = price_range[best_idx]
                best_prof = sim_profits[best_idx]
                st.success(f"최대 순이익: {best_pct:+.0f}% (₩{int(best_adr):,}) → 월 ₩{int(best_prof):,}", icon=":material/target:")

        elif host_type == "existing":
            # 탄력성 폴백 (ML 불가 시)
            st.subheader(":material/bar_chart: 요금 변경 시뮬레이션")
            st.caption(f"이 지역({cluster_name})은 요금을 10% 올리면 예약률이 약 {abs(elasticity)*10:.0f}% 변화합니다.")

            delta_pct = st.slider("요금 변화율 (%)", -30, 50, 0, 1)
            delta     = delta_pct / 100
            new_adr   = my_adr * (1 + delta)
            new_occ   = min(1.0, max(0.0, my_occ * (1 + elasticity * delta)))
            new_revp  = new_adr * new_occ
            new_net   = new_revp * 30 * 0.97 - total_opex
            p_change  = new_net - net_profit

            cs1, cs2 = st.columns(2)
            with cs1:
                sim_rows = [
                    ("1박 요금",    f"₩{int(my_adr):,}",   f"₩{int(new_adr):,}", f"{delta_pct:+d}%"),
                    ("예약률",      f"{my_occ:.0%}",        f"{new_occ:.0%}",     f"{(new_occ-my_occ)*100:+.1f}%p"),
                    ("하루 실수익", f"₩{int(my_revpar):,}", f"₩{int(new_revp):,}",
                     f"{(new_revp/my_revpar-1)*100:+.1f}%" if my_revpar > 0 else "-"),
                    ("월 순이익",   fmt_krw(net_profit),    fmt_krw(new_net),     f"₩{p_change:+,.0f}"),
                ]
                html = ('<div style="background:var(--bg-card);border-radius:12px;padding:20px;'
                        'box-shadow:0 2px 10px rgba(0,0,0,0.06);">'
                        '<div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;'
                        'color:var(--text-muted);font-size:12px;font-weight:600;padding-bottom:8px;'
                        'border-bottom:1.5px solid #F0F0F0;margin-bottom:4px;">'
                        '<span style="padding-right:8px;">항목</span><span style="text-align:right;padding:0 8px;border-left:1px solid var(--border-light);">현재</span>'
                        '<span style="text-align:right;padding:0 8px;border-left:1px solid var(--border-light);">변경 후</span>'
                        '<span style="text-align:right;padding:0 8px;border-left:1px solid var(--border-light);">변화</span></div>')
                for label, cur, nxt, chg in sim_rows:
                    w = "700" if "순이익" in label else "400"
                    chg_c = "#2E7D32" if ("+" in chg and "₩-" not in chg) else "#C62828" if ("-" in chg and "₩+" not in chg) else "#484848"
                    html += (f'<div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;'
                             f'padding:9px 0;border-bottom:1px solid var(--border-light);font-weight:{w};">'
                             f'<span style="font-size:13px;padding-right:8px;">{label}</span>'
                             f'<span style="text-align:right;font-size:13px;padding:0 8px;border-left:1px solid var(--border-light);">{cur}</span>'
                             f'<span style="text-align:right;font-size:13px;padding:0 8px;border-left:1px solid var(--border-light);">{nxt}</span>'
                             f'<span style="text-align:right;font-size:13px;padding:0 8px;border-left:1px solid var(--border-light);color:{chg_c};">{chg}</span></div>')
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)

                if delta_pct == 0:
                    st.info("슬라이더를 움직여 요금 변화 효과를 확인하세요.", icon=":material/info:")
                elif delta_pct > 0 and p_change > 0:
                    st.success(f"요금 인상 효과 — 순이익 ₩{p_change:+,.0f} 증가", icon=":material/check_circle:")
                elif delta_pct > 0:
                    st.error(f"요금 인상 역효과 — 순이익 ₩{abs(p_change):,.0f} 감소", icon=":material/error:")
                elif p_change > 0:
                    st.success(f"요금 인하로 예약률 상승 → 순이익 ₩{p_change:+,.0f} 증가", icon=":material/check_circle:")
                else:
                    st.warning(f"요금 인하 시 순이익 ₩{abs(p_change):,.0f} 감소", icon=":material/warning:")

            with cs2:
                x_range = np.linspace(-0.30, 0.50, 80)
                profits = [
                    my_adr*(1+d) * min(1., max(0., my_occ*(1+elasticity*d))) * 30 * 0.97 - total_opex
                    for d in x_range
                ]
                fig4, ax4 = plt.subplots(figsize=(5, 3.8))
                ax4.plot(x_range*100, profits, color="#FF5A5F", linewidth=2.5)
                ax4.axhline(0, color="#767676", linestyle="--", lw=1.2, alpha=0.6, label="손익분기선")
                ax4.axvline(delta_pct, color="#FFB400", linestyle="--", lw=1.5, label=f"현재 ({delta_pct:+d}%)")
                ax4.scatter([delta_pct], [new_net], color="#FFB400", s=70, zorder=6)
                ax4.fill_between(x_range*100, profits, 0, where=[p > 0 for p in profits], alpha=0.07, color="#4CAF50")
                ax4.fill_between(x_range*100, profits, 0, where=[p <= 0 for p in profits], alpha=0.07, color="#FF5A5F")
                ax4.set_xlabel("요금 변화율 (%)"); ax4.set_ylabel("월 순이익 (원)")
                ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"₩{y/10000:.0f}만"))
                ax4.legend(fontsize=8)
                ax4.spines["top"].set_visible(False); ax4.spines["right"].set_visible(False)
                ax4.set_facecolor("none"); fig4.patch.set_facecolor("none")
                fig4.tight_layout()
                st.pyplot(fig4); plt.close()
                best_idx  = int(np.argmax(profits))
                best_adr  = my_adr * (1 + x_range[best_idx])
                best_prof = profits[best_idx]
                st.success(f"최대 순이익: ₩{int(best_adr):,} ({x_range[best_idx]*100:+.0f}%) → 월 ₩{int(best_prof):,}", icon=":material/target:")

    # ── TAB 3: 주변 관광지 ────────────────────────────────────────────────────
    with tab3:
        section_title(
            ":material/place: 숙소 주변 관광지 분석",
            f"위치: {my_loc_name or d_name} 기준 — 데이터베이스 내 2,965개 POI 기반",
        )

        if my_lat and my_lng:
            with st.spinner("주변 관광지 분석 중..."):
                nearby = find_nearby_pois(my_lat, my_lng, max_km=2.0)

            cnt_500m = sum(1 for p in nearby if p["dist_m"] <= 500)
            cnt_1km  = sum(1 for p in nearby if p["dist_m"] <= 1000)
            cnt_2km  = len(nearby)

            # 강조 메트릭 카드
            _poi_cards = st.columns(3)
            _card_data = [
                ("500m 이내", cnt_500m, "도보 6분", "#FF5A5F"),
                ("1km 이내", cnt_1km, "도보 12분", "#4A6CF7"),
                ("2km 이내", cnt_2km, "전체 반경", "#767676"),
            ]
            for _col, (_label, _cnt, _sub, _color) in zip(_poi_cards, _card_data):
                with _col:
                    st.markdown(
                        f'<div style="border:2px solid {_color};border-radius:14px;padding:20px 16px;text-align:center;">'
                        f'<div style="font-size:12px;color:var(--text-muted);font-weight:600;">{_label} 관광지</div>'
                        f'<div style="font-size:32px;font-weight:800;color:{_color};margin:4px 0;">{_cnt}개</div>'
                        f'<div style="font-size:11px;color:var(--text-faint);">{_sub} 거리</div></div>',
                        unsafe_allow_html=True,
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**:material/place: 가장 가까운 관광지 TOP 5**")
            if nearby:
                _badge_colors = {
                    "관광지": "red", "문화시설": "violet", "음식점": "orange",
                    "쇼핑": "blue", "숙박": "green", "레포츠": "green",
                    "여행코스": "orange", "축제공연행사": "red",
                }
                for i, poi in enumerate(nearby[:5], 1):
                    dist_m = poi["dist_m"]
                    dist_txt = f"{dist_m}m" if dist_m < 1000 else f"{poi['dist_km']:.2f}km"
                    # 500m 이내 = 코랄 강조, 1km 이내 = 블루, 그 외 = 기본
                    if dist_m <= 500:
                        _border_c = "#FF5A5F"
                        _dist_badge = f'<span style="display:inline-block;background:#FF5A5F;color:white;font-size:11px;font-weight:700;padding:2px 10px;border-radius:12px;">{dist_txt}</span>'
                    elif dist_m <= 1000:
                        _border_c = "#4A6CF7"
                        _dist_badge = f'<span style="display:inline-block;background:#4A6CF715;color:#4A6CF7;font-size:11px;font-weight:700;padding:2px 10px;border-radius:12px;border:1px solid #4A6CF7;">{dist_txt}</span>'
                    else:
                        _border_c = "var(--border-light, #E0E0E0)"
                        _dist_badge = f'<span style="font-size:12px;color:var(--text-muted);font-weight:600;">{dist_txt}</span>'

                    with st.container(border=True):
                        _pc1, _pc2 = st.columns([4, 1])
                        with _pc1:
                            st.markdown(f"**{i}. {poi['name']}**")
                            if poi.get("addr"):
                                st.caption(poi["addr"])
                        with _pc2:
                            _bc = _badge_colors.get(poi["type"], "gray")
                            st.badge(poi["type"], color=_bc)
                            st.markdown(_dist_badge, unsafe_allow_html=True)
            else:
                st.info("데이터베이스에서 2km 이내 관광지를 찾지 못했습니다.")

            if nearby:
                st.markdown("**:material/bar_chart: 1km 이내 관광지 유형 분포**")
                nearby_1km = [p for p in nearby if p["dist_m"] <= 1000]
                if nearby_1km:
                    type_counts = {}
                    for p in nearby_1km:
                        t = p["type"]
                        type_counts[t] = type_counts.get(t, 0) + 1
                    type_counts = dict(sorted(type_counts.items(), key=lambda x: x[1], reverse=True))

                    _badge_colors_poi = {
                        "관광지": "red", "문화시설": "violet", "음식점": "orange",
                        "쇼핑": "blue", "숙박": "green", "레포츠": "green",
                        "여행코스": "orange", "축제공연행사": "red",
                    }
                    for t, cnt in type_counts.items():
                        _bc = _badge_colors_poi.get(t, "gray")
                        st.badge(f"{t} {cnt}개", color=_bc)

                    bench_500m = bench_val(bench, "nearest_500m", 19)
                    bench_1km  = bench_val(bench, "nearest_1km", 79)

                    # 지역 평균 비교 + 인사이트 요약
                    _adv_500 = cnt_500m >= bench_500m
                    _adv_1km = cnt_1km >= bench_1km
                    st.markdown(
                        f'<div style="background:var(--bg-secondary, #F7F7F7);border-radius:12px;padding:16px 20px;margin-top:12px;">'
                        f'<div style="font-size:14px;font-weight:700;color:var(--text-primary);margin-bottom:8px;">지역 평균 비교</div>'
                        f'<div style="font-size:13px;color:var(--text-secondary);line-height:1.8;">'
                        f'500m 이내: 평균 <b>{int(bench_500m)}개</b> vs 내 숙소 <b style="color:{"#2E7D32" if _adv_500 else "#C62828"};">{cnt_500m}개</b>'
                        f' &nbsp;|&nbsp; '
                        f'1km 이내: 평균 <b>{int(bench_1km)}개</b> vs 내 숙소 <b style="color:{"#2E7D32" if _adv_1km else "#C62828"};">{cnt_1km}개</b>'
                        f'</div></div>',
                        unsafe_allow_html=True,
                    )

                    # 인사이트 요약
                    if _adv_500 and _adv_1km:
                        st.success(
                            "관광지 밀집 지역에 위치해 있습니다. 숙소 설명에 '도보 이동 가능한 관광지'를 강조하고, "
                            "요금을 지역 평균 이상으로 설정해도 경쟁력이 있습니다.",
                            icon=":material/lightbulb:",
                        )
                    elif _adv_500 or _adv_1km:
                        st.info(
                            "주변 관광지가 평균 수준입니다. 가까운 주요 관광지 이름을 숙소 제목과 설명에 포함하면 "
                            "검색 노출에 유리합니다.",
                            icon=":material/lightbulb:",
                        )
                    else:
                        st.warning(
                            "관광지 접근성이 지역 평균보다 낮습니다. '조용한 로컬 동네 체험', "
                            "'교통 편의성(지하철 접근)' 등 차별화 전략이 필요합니다.",
                            icon=":material/lightbulb:",
                        )
                else:
                    st.info("1km 이내 관광지가 없습니다. 관광지 접근성이 낮은 지역에 위치해 있습니다.")
        else:
            st.info("주소를 입력하면 주변 관광지 분석 결과가 여기에 표시됩니다.")

    # ── TAB 4: 운영 개선(기존) / 지역진단(신규) ──────────────────────────────
    _cluster_unicode_emoji = {
        "핫플 수익형": "🏆", "프리미엄 비즈니스": "📈",
        "로컬 주거형": "⚖️", "가성비 신흥형": "🛡️",
    }

    def _render_market_tab(tab_obj):
        with tab_obj:
            _uni_emoji = _cluster_unicode_emoji.get(cluster_name, "📊")
            section_title(
                f"{c_info['emoji']} {d_name} 시장 유형: {cluster_name}",
                c_info["desc"],
            )
            col_m1, col_m2 = st.columns([1, 1.4])
            with col_m1:
                with st.container(border=True):
                    st.markdown(
                        f'<div style="text-align:center;padding:8px 0;">'
                        f'<div style="font-size:36px;">{_uni_emoji}</div>'
                        f'<div style="font-size:16px;font-weight:700;color:var(--coral);margin:4px 0;">{cluster_name}</div>'
                        f'<div style="font-size:12px;color:var(--text-muted);">{c_info["desc"]}</div></div>',
                        unsafe_allow_html=True,
                    )
                if len(d_row) > 0:
                    row = d_row.iloc[0]
                    _revpar_val = int(row.get('median_revpar_ao', 0))
                    _dormant = row.get('dormant_ratio', 0)
                    info_row("지역 평균 하루 수익", f"₩{_revpar_val:,}", value_color="var(--coral)")
                    _dormant_color = "#C62828" if _dormant > 0.5 else "#FFB400" if _dormant > 0.3 else "var(--green)"
                    info_row("비활성 숙소 비율", f"{_dormant:.1%}", value_color=_dormant_color)
                    info_row("슈퍼호스트 비율", f"{row.get('superhost_rate', 0):.1%}")
            with col_m2:
                st.markdown("**이 지역에서 수익을 올리는 전략:**")
                for i, strat in enumerate(c_info["strategy"], 1):
                    st.markdown(
                        f'<div style="border-left:4px solid var(--coral);padding:12px 16px;'
                        f'background:var(--bg-coral-light);border-radius:0 8px 8px 0;margin:6px 0;">'
                        f'<div style="font-weight:700;color:var(--text-primary);">{i}. {strat}</div></div>',
                        unsafe_allow_html=True,
                    )

    # ── 숙소 설명 탭 렌더링 함수 ────────────────────────────────────────────
    def _render_description_tab():
        _room_style = st.session_state.get("my_room_style", "모던/미니멀")
        _guests   = int(st.session_state.my_guests   or 2)
        _bedrooms = int(st.session_state.my_bedrooms or 1)
        _baths    = float(st.session_state.my_baths_count or 1)
        _beds     = int(st.session_state.my_beds or 1)

        section_title(
            ":material/edit_note: 숙소 설명 생성",
            "내 숙소 유형에 맞는 설명 템플릿입니다. [직접 입력] 부분을 채워 완성하세요.",
        )

        _style_adj = {
            "모던/미니멀": "깔끔하고 심플한 모던",
            "빈티지/레트로": "감성적인 빈티지",
            "한옥/전통": "한국 전통 감성이 살아있는",
            "아늑/가정적": "따뜻하고 아늑한",
            "럭셔리/프리미엄": "고급스러운 프리미엄",
        }.get(_room_style, "세련된")

        if room_type == "entire_home":
            _privacy = "숙소 전체를 단독으로 사용하실 수 있어 프라이빗한 공간이 필요하신 분께 적합합니다."
            _space   = f"침실 {_bedrooms}개, 욕실 {int(_baths)}개로 구성된 집 전체입니다."
            _intro   = f"{_style_adj} 감성의 {d_name} 집 전체를 단독으로 즐겨보세요."
        elif room_type == "private_room":
            _privacy = "침실은 단독으로 사용하시고, 거실·주방·욕실은 다른 게스트와 함께 이용합니다."
            _space   = "개인 침실을 단독으로 이용하시며, 그 외 공간은 공용입니다."
            _intro   = f"{_style_adj} 분위기의 {d_name} 개인실에서 편안하게 머무르세요."
        elif room_type == "hotel_room":
            _privacy = "호텔 수준의 서비스와 편의시설을 갖춘 독립 객실입니다."
            _space   = "객실 내 침실과 욕실이 완비되어 있습니다."
            _intro   = f"{d_name}에 위치한 {_style_adj} 호텔 스타일 객실입니다."
        else:
            _privacy = "합리적인 가격으로 서울을 여행하시는 분께 적합한 다인실입니다."
            _space   = "침대와 기본 수납공간이 제공됩니다."
            _intro   = f"{d_name}의 {_style_adj} 다인실에서 새로운 여행자들을 만나보세요."

        template = f"""◼ 숙소 소개
{_intro} [가까운 지하철역 또는 주요 명소 — 직접 입력: 예) 홍대입구역 도보 5분 거리에 위치하여] 서울 주요 지역으로의 이동이 편리합니다.
{_privacy}

[숙소만의 특별한 포인트 — 직접 입력: 예) 통창으로 들어오는 자연광, 루프탑 테라스, 한강 뷰 등]

◼ 숙소 구성
최대 {_guests}명 이용 가능 · {_space}

침실에는 [침대 종류 — 직접 입력: 예) 킹사이즈 침대 / 더블베드 / 싱글 침대 {_beds}개]이 갖춰져 있으며, [주요 가전·가구 — 직접 입력: 예) 에어컨, 난방, TV, 냉장고, 전자레인지, 세탁기, 드레스룸]가 제공됩니다.

◼ 기본 제공 어메니티
[직접 입력: 예) 수건, 헤어드라이기, 샴푸, 컨디셔너, 바디워시, 핸드워시, 비누, 티슈, 슬리퍼]가 기본으로 제공됩니다.
[별도 준비 필요 항목 — 직접 입력: 예) 칫솔·치약은 개별적으로 준비해주시기 바랍니다.]

◼ 체크인 / 체크아웃
체크인: [직접 입력: 예) 15:00 이후] / 체크아웃: [직접 입력: 예) 11:00 이전]
[입실 방법 — 직접 입력: 예) 도어락으로 키 없이 입실 가능합니다. 예약 확정 후 비밀번호를 안내드립니다.]

◼ 주의사항
[직접 입력: 예) 금연 / 반려동물 동반 불가 / 파티·행사 불가 / 층간소음 주의 / 쓰레기 분리수거 안내]"""

        st.info(
            "**사용 방법**: 아래 텍스트를 복사해 에어비앤비 숙소 설명란에 붙여넣은 뒤, "
            "**[직접 입력]** 부분을 내 숙소 상황에 맞게 직접 수정해주세요. "
            "가구·가전·어메니티는 실제 보유 여부를 확인 후 작성해야 합니다.",
            icon=":material/lightbulb:",
        )

        st.text_area(
            "숙소 설명 템플릿 (복사 후 수정하여 사용)",
            value=template,
            height=430,
            key="desc_template_area",
        )

        with st.container(border=True):
            st.markdown(
                ":material/push_pin: **설명 작성 꿀팁**\n\n"
                "- **첫 문장**이 검색 결과 미리보기로 노출됩니다. 가장 매력적인 포인트를 먼저 쓰세요.\n"
                "- **지하철역·버스 정류장** 이름과 도보 시간을 구체적으로 명시하면 예약률이 높아집니다.\n"
                "- **어메니티 목록**은 구체적일수록 좋습니다. 없는 항목을 적으면 나중에 분쟁 원인이 됩니다.\n"
                "- **주의사항**은 명확하게 적어야 불필요한 환불 요청을 예방할 수 있습니다."
            )

    if host_type == "existing":
        with tab4:
            section_title(":material/checklist: 지금 바로 개선할 수 있는 것들")

            # (icon, item_icon, title, desc, status)
            # item_icon: 각 항목을 시각적으로 구분하는 머티리얼 아이콘
            checks = []
            if my_superhost:
                checks.append((":material/check_circle:", ":material/workspace_premium:", "슈퍼호스트 달성", "수익 +83% 프리미엄 유지 중", "done"))
            else:
                est = my_revpar * 1.831
                checks.append((":material/error:", ":material/workspace_premium:", "슈퍼호스트 미달성",
                    f"달성 시 하루 수익 ₩{int(my_revpar):,} → ₩{int(est):,} 잠재", "todo"))
            if my_instant:
                checks.append((":material/check_circle:", ":material/bolt:", "즉시예약 켜짐", "예약률 최대화 중", "done"))
            else:
                checks.append((":material/info:", ":material/bolt:", "즉시예약 꺼짐", "설정 1분, 비용 없음 → 예약률 +5~10% 기대", "quick"))
            if 20 <= my_photos <= 35:
                checks.append((":material/check_circle:", ":material/photo_camera:", f"사진 {my_photos}장 (최적)", "최적 20~35장 구간 유지 중", "done"))
            elif my_photos < 20:
                checks.append((":material/error:", ":material/photo_camera:", f"사진 {my_photos}장 (부족)", f"{20-my_photos}장 추가 → 클릭률 상승", "todo"))
            else:
                checks.append((":material/info:", ":material/photo_camera:", f"사진 {my_photos}장 (많음)", "35장 초과 — 좋은 사진만 추려서 정리 권장", "quick"))
            if not my_extra_fee:
                checks.append((":material/check_circle:", ":material/payments:", "추가 게스트 요금 없음", "요금에 포함 — 최적 구조", "done"))
            else:
                checks.append((":material/error:", ":material/payments:", "추가 게스트 요금 있음", "없애고 1박 요금에 통합 → 수익 +25~56% 회복", "quick"))
            if 2 <= my_min_nights <= 3:
                checks.append((":material/check_circle:", ":material/hotel:", f"최소 {my_min_nights}박 (최적)", "수익 최적 + 리뷰 축적 속도 최적", "done"))
            elif my_min_nights == 1:
                checks.append((":material/info:", ":material/hotel:", "최소 1박", "수익 효율 낮음 — 2박으로 변경 추천", "quick"))
            else:
                checks.append((":material/info:", ":material/hotel:", f"최소 {my_min_nights}박 (길음)", "리뷰 축적 속도 느림 — 2~3박으로 줄이기", "quick"))
            if my_rating >= 4.8:
                checks.append((":material/check_circle:", ":material/star:", f"평점 {my_rating:.1f}", "슈퍼호스트 기준 충족 + 검색 상위", "done"))
            elif my_rating >= 4.5:
                checks.append((":material/info:", ":material/star:", f"평점 {my_rating:.1f}", "4.8 이상이면 슈퍼호스트 + 검색 부스트", "todo"))
            else:
                checks.append((":material/error:", ":material/star:", f"평점 {my_rating:.1f} (낮음)", "4.5 미만 — 검색 노출 불이익", "todo"))
            if my_reviews >= 10:
                checks.append((":material/check_circle:", ":material/rate_review:", f"리뷰 {my_reviews}건", "슈퍼호스트 최소 요건 충족", "done"))
            else:
                checks.append((":material/error:", ":material/rate_review:", f"리뷰 {my_reviews}건",
                    f"슈퍼호스트 최소 10건 필요 — {10-my_reviews}건 더 필요", "todo"))

            # 요약 카운트 카드
            done_cnt = sum(1 for *_, s in checks if s == "done")
            quick_cnt = sum(1 for *_, s in checks if s == "quick")
            todo_cnt = sum(1 for *_, s in checks if s == "todo")

            cols_summary = st.columns(3)
            with cols_summary[0]:
                st.metric(":material/verified: 잘 하고 있어요", f"{done_cnt}개",
                          delta="유지하세요!", delta_color="off", border=True)
            with cols_summary[1]:
                st.metric(":material/bolt: 빠른 개선", f"{quick_cnt}개",
                          delta="쉽게 바꿀 수 있어요" if quick_cnt > 0 else "없음",
                          delta_color="inverse" if quick_cnt > 0 else "off", border=True)
            with cols_summary[2]:
                st.metric(":material/construction: 개선 필요", f"{todo_cnt}개",
                          delta="수익에 영향을 줘요" if todo_cnt > 0 else "없음",
                          delta_color="inverse" if todo_cnt > 0 else "off", border=True)

            # ── 개선이 필요한 항목 (quick + todo) 먼저 표시
            improve_items = [(icon, item_icon, title, desc, status)
                             for icon, item_icon, title, desc, status in checks
                             if status in ("quick", "todo")]
            if improve_items:
                st.markdown("#### :material/construction: 개선이 필요한 항목")
                col_a, col_b = st.columns(2)
                for i, (icon, item_icon, title, desc, status) in enumerate(improve_items):
                    col = col_a if i % 2 == 0 else col_b
                    _badge_c = "orange" if status == "quick" else "red"
                    _badge_t = "빠른 개선" if status == "quick" else "개선 필요"
                    with col:
                        with st.container(border=True):
                            st.badge(_badge_t, color=_badge_c)
                            st.markdown(f"{item_icon} **{title}**")
                            st.caption(desc)

            # ── 잘 하고 있는 항목 (done)
            done_items = [(icon, item_icon, title, desc, status)
                          for icon, item_icon, title, desc, status in checks
                          if status == "done"]
            if done_items:
                st.markdown("#### :material/verified: 잘 하고 있는 항목")
                col_a, col_b = st.columns(2)
                for i, (icon, item_icon, title, desc, status) in enumerate(done_items):
                    col = col_a if i % 2 == 0 else col_b
                    with col:
                        with st.container(border=True):
                            st.badge("완료", color="green")
                            st.markdown(f"{item_icon} **{title}**")
                            st.caption(desc)

            quick_list = [(icon, item_icon, title, desc) for icon, item_icon, title, desc, status in checks if status in ("quick","todo")]
            if quick_list:
                st.subheader(":material/target: 지금 당장 실행하면 효과 큰 TOP 3")
                for i, (icon, item_icon, title, desc) in enumerate(quick_list[:3], 1):
                    st.markdown(
                        f'<div style="border-left:4px solid var(--coral);padding:12px 16px;'
                        f'background:var(--bg-coral-light);border-radius:0 8px 8px 0;margin:6px 0;">'
                        f'<div style="font-weight:700;color:var(--text-primary);">{i}. {title}</div>'
                        f'<div style="font-size:12px;color:var(--text-secondary);margin-top:2px;">{desc}</div></div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.success("모든 운영 레버가 최적 상태입니다!", icon=":material/celebration:")

        _render_market_tab(tab5)

        with tab7:
            _render_description_tab()

        # ── TAB 6: 헬스 스코어 (기존 호스트) ────────────────────────────────
        with tab6:
            section_title(
                ":material/health_and_safety: 숙소 운영 건강 점수",
                f"동일 클러스터({cluster_name}) 내 Active+Operating 숙소 {len(_cluster_listings):,}개와 비교한 5가지 운영 건강 지표입니다.",
            )
            if _hs_ok:
                grade_colors = {
                    "A": "#2E7D32", "B": "#00A699",
                    "C": "#FFB400", "D": "#FF8C00", "F": "#C62828",
                }
                gc = grade_colors.get(_hs["grade"], "#767676")

                hs_c1, hs_c2 = st.columns([1, 2])
                with hs_c1:
                    with st.container(border=True):
                        st.markdown(
                            f'<div style="text-align:center;padding:16px;border-radius:12px;'
                            f'border:2px solid {gc};background:{gc}10;">'
                            f'<div style="font-size:36px;font-weight:800;color:{gc};">{int(_hs["composite"])}</div>'
                            f'<div style="font-size:12px;color:var(--text-muted);">/ 100점</div>'
                            f'<div style="margin-top:8px;display:inline-block;padding:4px 14px;'
                            f'border-radius:20px;background:{gc}18;color:{gc};'
                            f'font-size:14px;font-weight:700;">등급 {_hs["grade"]}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                        st.caption("같은 지역 유형의 숙소들과 비교한 점수입니다")

                with hs_c2:
                    comp_labels = {
                        "review_signal":   ("리뷰 신호",   "리뷰 수 & 평점 백분위"),
                        "listing_quality": ("사진 품질",   "최적 23~35장 기준"),
                        "booking_policy":  ("예약 정책",   "즉시예약·최소박·추가요금"),
                        "location":        ("위치",        "POI 거리 (가까울수록 높음)"),
                        "listing_config":  ("숙소 구성",   "침실·욕실 수 백분위"),
                    }
                    for key, (label, hint) in comp_labels.items():
                        v = _hs["components"][key]
                        _score_color = "#2E7D32" if v >= 70 else "#FFB400" if v >= 40 else "#C62828"
                        st.markdown(
                            f'**{label}** :small[{hint}] — '
                            f'<span style="color:{_score_color};font-weight:700;">{int(v)}</span>/100',
                            unsafe_allow_html=True,
                        )
                        st.progress(int(v))

                # 개선 액션 (full width)
                if _hs["actions"] and not _hs["actions"][0].startswith(":material/check_circle:"):
                    st.warning(":material/target: **지금 개선하면 점수가 올라가요**", icon=":material/target:")
                    for a in _hs["actions"]:
                        st.markdown(f"- {a}")
                else:
                    st.success("모든 운영 지표가 클러스터 상위권입니다! 현재 상태를 유지하세요.", icon=":material/celebration:")
            else:
                st.warning("헬스 스코어 계산 중 오류가 발생했습니다.")

    else:
        _render_market_tab(tab4)
        with tab5:
            _render_description_tab()

    # ── 다시 시작 ────────────────────────────────────────────────────────────
    _, c_center, _ = st.columns([1, 2, 1])
    with c_center:
        st.markdown('<div class="nav-primary">', unsafe_allow_html=True)
        if st.button("처음부터 다시 입력하기", key="restart", use_container_width=True, type="primary", icon=":material/refresh:"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.caption("서울 Airbnb 수익 최적화 · 데이터 기간: 2024-10 ~ 2025-09 · 32,061개 리스팅 기반")

# ─────────────────────────────────────────────────────────────────────────────
# 라우터
# ─────────────────────────────────────────────────────────────────────────────
step      = st.session_state.get("step", 1)
host_type = st.session_state.get("host_type", None)

if step == 1:
    step1()
elif step == 2:
    if host_type == "new":
        step2_new()
    else:
        step2_existing()
elif step == 3:
    step3()
elif step == 4:
    step4_existing()
else:
    step5()
