"""
HTML 템플릿 모듈 — 슬라이드별 HTML 생성
하이브리드 PPT: 복잡한 비주얼은 HTML→PNG, 단순 텍스트는 네이티브 python-pptx
"""

# ── 공통 CSS ──────────────────────────────────────────────
BASE_CSS = """
@font-face { font-family: 'Pretendard'; font-weight: 100; src: url('file:///Users/jungmo/Downloads/Pretendard-otf/Pretendard-Thin.otf') format('opentype'); }
@font-face { font-family: 'Pretendard'; font-weight: 200; src: url('file:///Users/jungmo/Downloads/Pretendard-otf/Pretendard-ExtraLight.otf') format('opentype'); }
@font-face { font-family: 'Pretendard'; font-weight: 300; src: url('file:///Users/jungmo/Downloads/Pretendard-otf/Pretendard-Light.otf') format('opentype'); }
@font-face { font-family: 'Pretendard'; font-weight: 400; src: url('file:///Users/jungmo/Downloads/Pretendard-otf/Pretendard-Regular.otf') format('opentype'); }
@font-face { font-family: 'Pretendard'; font-weight: 500; src: url('file:///Users/jungmo/Downloads/Pretendard-otf/Pretendard-Medium.otf') format('opentype'); }
@font-face { font-family: 'Pretendard'; font-weight: 600; src: url('file:///Users/jungmo/Downloads/Pretendard-otf/Pretendard-SemiBold.otf') format('opentype'); }
@font-face { font-family: 'Pretendard'; font-weight: 700; src: url('file:///Users/jungmo/Downloads/Pretendard-otf/Pretendard-Bold.otf') format('opentype'); }
@font-face { font-family: 'Pretendard'; font-weight: 800; src: url('file:///Users/jungmo/Downloads/Pretendard-otf/Pretendard-ExtraBold.otf') format('opentype'); }
@font-face { font-family: 'Pretendard'; font-weight: 900; src: url('file:///Users/jungmo/Downloads/Pretendard-otf/Pretendard-Black.otf') format('opentype'); }

* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1920px; height: 1080px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
}

/* 색상 시스템 */
:root {
  --coral: #FF5A5F;
  --coral-light: #FF787C;
  --coral-dark: #E04347;
  --teal: #00A699;
  --teal-light: #00C9B7;
  --charcoal: #484848;
  --dark-bg: #1A1A2E;
  --dark-bg-2: #16213E;
  --light-bg: #FFFFFF;
  --white: #FFFFFF;
  --insight-bg: #FFF0F3;
  --card-radius: 6px;
  --underline-width: 192px;
  --underline-height: 3px;
  --orange: #FC642D;
  --gray-100: #F5F5F5;
  --gray-200: #E8E8E8;
  --gray-300: #DBDBDB;
  --gray-400: #B0B0B0;
  --gray-500: #767676;
  --gray-600: #484848;
}

.slide {
  width: 1920px; height: 1080px;
  position: relative;
  overflow: hidden;
}

/* 다크 슬라이드 */
.slide-dark {
  background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
  color: white;
}

/* 라이트 슬라이드 */
.slide-light {
  background: #FFFFFF;
  color: var(--charcoal);
}

/* 카드 컴포넌트 */
.card {
  background: #F5F5F5;
  border-radius: 6px;
  box-shadow: none;
  padding: 32px;
}
.card-coral {
  background: var(--coral);
  color: white;
}
.card-teal {
  background: var(--teal);
  color: white;
}
.card-dark {
  background: #2B2B3D;
  color: white;
}

/* 태그 */
.tag {
  display: inline-block;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}
.tag-coral { background: rgba(255,90,95,0.15); color: var(--coral); }
.tag-teal { background: rgba(0,166,153,0.15); color: var(--teal); }

/* 큰 숫자 */
.big-number {
  font-size: 72px;
  font-weight: 900;
  line-height: 1;
  color: var(--coral);
}
.big-number-white {
  font-size: 72px;
  font-weight: 900;
  line-height: 1;
  color: white;
}

/* 페이지 번호 */
.page-num {
  position: absolute;
  bottom: 30px;
  right: 50px;
  font-size: 14px;
  color: var(--gray-400);
}
.page-num-light {
  color: rgba(255,255,255,0.4);
}

/* 장식 요소 — 비활성화 */
.deco-circle {
  display: none;
}
.deco-line {
  width: 60px;
  height: 4px;
  background: var(--coral);
  border-radius: 2px;
  margin: 16px 0;
}

/* ── 신규 공통 클래스 ── */
.breadcrumb {
  font-size: 13px;
  color: var(--gray-500);
  font-weight: 500;
  letter-spacing: 1px;
}
.slide-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--charcoal);
  margin: 6px 0 8px;
}
.title-underline {
  width: var(--underline-width);
  height: var(--underline-height);
  background: var(--coral);
  border-radius: 2px;
  margin-bottom: 32px;
}
.insight-box {
  background: var(--insight-bg);
  border-left: 4px solid var(--coral);
  border-radius: 0 6px 6px 0;
  padding: 20px 24px;
  font-size: 15px;
  line-height: 1.6;
  color: var(--charcoal);
}
.list-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  font-size: 15px;
}
.pill {
  display: inline-block;
  padding: 4px 14px;
  border-radius: 14px;
  font-size: 12px;
  font-weight: 600;
}
.pill-coral { background: rgba(255,90,95,0.12); color: var(--coral); }
.pill-teal { background: rgba(0,166,153,0.12); color: var(--teal); }
.pill-gray { background: var(--gray-100); color: var(--gray-500); }

/* 테이블 헤더 공통 */
table th {
  background: #484848;
  color: white;
}
"""


def slide_01_cover(page=1):
  """표지 — 순백 배경, 사용자 PPT 스타일"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .cover-wrap {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; background: #FFFFFF; position: relative; }}
  .cover-icon {{ font-size: 48px; margin-bottom: 32px; color: var(--coral); }}
  .cover-title {{ font-size: 48px; font-weight: 800; color: var(--charcoal); letter-spacing: -1px; line-height: 1.3; }}
  .cover-title-accent {{ color: var(--coral); }}
  .cover-subtitle {{ font-size: 17px; color: var(--gray-500); margin-top: 24px; letter-spacing: 1px; }}
  .cover-pills {{ display: flex; gap: 12px; justify-content: center; margin-top: 28px; }}
  .cover-pill {{ padding: 6px 18px; border: 1.5px solid var(--coral); border-radius: 20px; font-size: 13px; color: var(--coral); font-weight: 500; }}
  .cover-quote {{ margin-top: 32px; font-size: 15px; color: var(--gray-400); font-style: italic; }}
  .cover-bottom {{ position: absolute; bottom: 50px; left: 0; right: 0; text-align: center; }}
  .cover-line {{ width: 200px; height: 2px; background: var(--coral); margin: 0 auto 16px; }}
  .cover-team {{ font-size: 14px; color: var(--gray-500); }}
  .cover-date {{ position: absolute; top: 36px; right: 50px; padding: 6px 16px; border: 1.5px solid var(--coral); border-radius: 16px; font-size: 12px; color: var(--coral); font-weight: 500; }}
  </style></head><body>
  <div class="slide" style="background: #FFFFFF; overflow: hidden;">
    <div class="cover-date">2026.03</div>
    <div class="cover-wrap">
      <div class="cover-icon">📊</div>
      <div class="cover-title">서울 에어비앤비<br><span class="cover-title-accent">수익 최적화 가이드</span></div>
      <div class="cover-subtitle">3개월 / 12개월 · 32,061 리스팅 · 서울 25개 자치구</div>
      <div class="cover-pills">
        <div class="cover-pill">TTM 12개월</div>
        <div class="cover-pill">L90D 3개월</div>
      </div>
      <div class="cover-quote">"데이터로 호스트의 수익을 설계하다"</div>
    </div>
    <div class="cover-bottom">
      <div class="cover-line"></div>
      <div class="cover-team">4조 · 데이터분석 부트캠프</div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_02_toc(page=2):
  """목차 — 6개 스텝"""
  steps = [
    ("01", "문제정의", "Why · What · How", False),
    ("02", "데이터·전처리", "품질 이슈 대응", False),
    ("03", "분석방법", "EDA 가설 검증", False),
    ("04", "통계검증", "비모수 검정", False),
    ("05", "모델링", "Dual Model + 건강점수", False),
    ("06", "대시보드·자동화", "★ 핵심 차별점", True),
  ]
  cards = ""
  for num, title, sub, highlight in steps:
    bg = "background: var(--coral); color: white;" if highlight else "background: #F5F5F5; color: var(--charcoal);"
    num_color = "color: rgba(255,255,255,0.3);" if highlight else "color: var(--gray-300);"
    sub_color = "color: rgba(255,255,255,0.8);" if highlight else "color: var(--gray-500);"
    star = '<span style="position:absolute;top:12px;right:16px;font-size:12px;background:rgba(255,255,255,0.25);padding:4px 10px;border-radius:10px;">★ 핵심</span>' if highlight else ''
    cards += f"""
    <div class="toc-card" style="{bg}; border-radius: 6px; padding: 36px 28px; flex: 1; position:relative;">
      {star}
      <div style="font-size: 48px; font-weight: 900; {num_color}">{num}</div>
      <div style="font-size: 22px; font-weight: 700; margin-top: 16px;">{title}</div>
      <div style="font-size: 14px; {sub_color}; margin-top: 8px;">{sub}</div>
    </div>"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .toc-wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; }}
  .toc-grid {{ display: flex; gap: 20px; flex: 1; align-items: center; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="toc-wrap">
      <div class="breadcrumb">CONTENTS</div>
      <div class="slide-title" style="font-size: 36px;">목차</div>
      <div class="title-underline" style="margin-bottom: 50px;"></div>
      <div class="toc-grid">{cards}</div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_section(num, title, subtitle="", page=0, purpose="", items=None):
  """섹션 구분 슬라이드 — 좌 coral + 우 white 분할"""
  sub_html = f'<div class="sec-subtitle">{subtitle}</div>' if subtitle else ''
  # 우측 패널 콘텐츠
  right_inner = ""
  if purpose or items:
    purpose_html = f'<div class="sec-purpose">{purpose}</div>' if purpose else ''
    items_html = ""
    if items:
      for item in items:
        color = item.get("color", "var(--coral)")
        items_html += f"""
        <div class="sec-item">
          <div class="sec-item-pill" style="background: {color};"></div>
          <div class="sec-item-text">{item["text"]}</div>
        </div>"""
    right_inner = f"""
      <div class="sec-right-content">
        {purpose_html}
        {items_html}
      </div>"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .sec-wrap {{ display: flex; width: 100%; height: 100%; }}
  .sec-left {{ width: 40%; background: var(--coral); display: flex; flex-direction: column; justify-content: center; padding: 80px 60px; }}
  .sec-right {{ width: 60%; background: #FFFFFF; display: flex; flex-direction: column; justify-content: center; padding: 80px 80px; }}
  .sec-label {{ font-size: 15px; color: rgba(255,255,255,0.7); font-weight: 600; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px; }}
  .sec-title {{ font-size: 44px; font-weight: 800; color: white; line-height: 1.3; }}
  .sec-subtitle {{ font-size: 17px; color: rgba(255,255,255,0.75); margin-top: 20px; line-height: 1.5; }}
  .sec-right-content {{ display: flex; flex-direction: column; gap: 16px; }}
  .sec-purpose {{ font-size: 18px; color: var(--gray-500); font-weight: 500; margin-bottom: 12px; line-height: 1.6; }}
  .sec-item {{ display: flex; align-items: center; gap: 14px; padding: 14px 20px; border-left: 3px solid var(--gray-200); background: #FAFAFA; border-radius: 0 6px 6px 0; }}
  .sec-item-pill {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}
  .sec-item-text {{ font-size: 16px; color: var(--charcoal); font-weight: 500; }}
  </style></head><body>
  <div class="slide" style="overflow: hidden;">
    <div class="sec-wrap">
      <div class="sec-left">
        <div class="sec-label">SECTION {num}</div>
        <div class="sec-title">{title}</div>
        {sub_html}
      </div>
      <div class="sec-right">
        {right_inner}
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_04_why(page=4):
  """WHY — 시장 현황 3대 숫자"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; }}
  .cards {{ display: flex; gap: 28px; flex: 1; align-items: center; }}
  .stat-card {{ flex: 1; border-radius: 6px; padding: 44px 36px; text-align: center; background: #F5F5F5; }}
  .stat-card .num {{ font-size: 64px; font-weight: 900; line-height: 1.1; }}
  .stat-card .label {{ font-size: 16px; color: var(--gray-500); margin-top: 12px; }}
  .stat-card .sub {{ font-size: 14px; margin-top: 8px; padding: 6px 16px; border-radius: 20px; display: inline-block; }}
  .bottom-msg {{ margin-top: 32px; padding: 24px 36px; background: #F5F5F5; border-left: 5px solid var(--coral); border-radius: 0 6px 6px 0; font-size: 18px; font-weight: 500; color: var(--charcoal); }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">WHY — 왜 이 분석이 필요한가?</div>
      <div class="slide-title">서울 에어비앤비 시장 현황</div>
      <div class="title-underline"></div>
      <div class="cards">
        <div class="stat-card">
          <div class="num" style="color: var(--charcoal);">32,061</div>
          <div class="label">전체 리스팅 (서울 25개 자치구)</div>
          <div class="sub" style="background: var(--gray-200); color: var(--gray-500);">데이터 규모</div>
        </div>
        <div class="stat-card" style="background: var(--insight-bg);">
          <div class="num" style="color: var(--coral);">54.3%</div>
          <div class="label">Dormant 비율</div>
          <div class="sub" style="background: rgba(255,90,95,0.15); color: var(--coral);">시장의 절반이 비활성</div>
        </div>
        <div class="stat-card">
          <div class="num" style="color: var(--charcoal);">₩8,868</div>
          <div class="label">TTM RevPAR 중위값</div>
          <div class="sub" style="background: var(--gray-200); color: var(--gray-500);">월 1만원 미만 수익</div>
        </div>
      </div>
      <div class="bottom-msg">
        호스트는 가격을 낮추면 수익이 줄고, 올리면 예약이 줄어드는 <strong style="color: var(--coral);">딜레마</strong>에 빠져 있다
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_05_what(page=5):
  """WHAT — 수익의 두 가지 레버"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; }}
  .formula-row {{ display: flex; align-items: center; justify-content: center; gap: 24px; margin-bottom: 48px; }}
  .formula-box {{ padding: 28px 44px; border-radius: 6px; font-size: 28px; font-weight: 700; text-align: center; }}
  .formula-op {{ font-size: 36px; font-weight: 300; color: var(--gray-400); }}
  .lever-section {{ flex: 1; display: flex; gap: 40px; align-items: stretch; margin-bottom: 36px; }}
  .lever-card {{ flex: 1; border-radius: 6px; padding: 36px 32px; display: flex; flex-direction: column; gap: 16px; background: #F5F5F5; }}
  .lever-num {{ font-size: 13px; font-weight: 700; letter-spacing: 2px; }}
  .lever-name {{ font-size: 24px; font-weight: 800; }}
  .lever-sub {{ font-size: 15px; color: var(--gray-500); line-height: 1.6; }}
  .lever-question {{ font-size: 17px; font-weight: 700; line-height: 1.5; margin-top: auto; padding-top: 20px; border-top: 2px solid rgba(0,0,0,0.08); }}
  .bottom-msg {{ background: #F5F5F5; border-radius: 6px; padding: 24px 32px; text-align: center; font-size: 17px; font-weight: 600; color: var(--charcoal); line-height: 1.7; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">WHAT — 무엇을 분석하는가?</div>
      <div class="slide-title">수익의 두 가지 레버</div>
      <div class="title-underline"></div>
      <div class="formula-row">
        <div class="formula-box" style="background: var(--coral); color: white;">RevPAR</div>
        <div class="formula-op">=</div>
        <div class="formula-box" style="background: #F5F5F5; color: var(--charcoal);">ADR<br><span style="font-size:14px;font-weight:400;color:var(--gray-500);">평균 일일 요금</span></div>
        <div class="formula-op">×</div>
        <div class="formula-box" style="background: var(--teal); color: white;">Occupancy Rate<br><span style="font-size:14px;font-weight:300;">점유율</span></div>
      </div>
      <div class="lever-section">
        <div class="lever-card" style="border-left: 4px solid var(--charcoal);">
          <div class="lever-num" style="color: var(--gray-500);">LEVER 1</div>
          <div class="lever-name">객실 요금 (ADR)</div>
          <div class="lever-sub">호스트가 직접 설정하는 가격.<br>시장 대비 높거나 낮은 포지셔닝.</div>
          <div class="lever-question" style="color: var(--charcoal);">"가격을 낮추면<br>예약이 늘까?"</div>
        </div>
        <div class="lever-card" style="border-left: 4px solid var(--teal);">
          <div class="lever-num" style="color: var(--teal);">LEVER 2</div>
          <div class="lever-name">예약률 (Occupancy)</div>
          <div class="lever-sub">리뷰, 사진, 즉시예약 등<br>운영 변수가 결정하는 지표.</div>
          <div class="lever-question" style="color: var(--teal);">"예약률을 올리려면<br>무엇을 바꿔야 하나?"</div>
        </div>
      </div>
      <div class="bottom-msg">이 프로젝트는 두 레버의 균형점을 찾아,<br>호스트가 직접 바꿀 수 있는 변수로 RevPAR을 최적화하는 방법을 데이터로 검증합니다</div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_06_how(page=6):
  """HOW — 분석 프레임워크"""
  steps = [
    ("📥", "데이터 수집", "32,061 리스팅"),
    ("🔧", "전처리", "Spatial Join, 이상치"),
    ("📊", "EDA", "9개 가설 검증"),
    ("🤖", "모델링", "Dual Model + SHAP"),
    ("🖥️", "대시보드", "Streamlit 배포"),
    ("⚡", "자동화", "Hooks + 이메일"),
  ]
  step_html = ""
  for i, (icon, title, sub) in enumerate(steps):
    bg = "background: var(--coral); color: white;" if i >= 2 and i <= 3 else "background: #F5F5F5; color: var(--charcoal);"
    arrow = '<div style="font-size: 28px; color: var(--gray-300); display: flex; align-items: center;">→</div>' if i < 5 else ''
    step_html += f"""
    <div style="flex: 1; {bg}; border-radius: 6px; padding: 28px 20px; text-align: center;">
      <div style="font-size: 36px; margin-bottom: 12px;">{icon}</div>
      <div style="font-size: 18px; font-weight: 700;">{title}</div>
      <div style="font-size: 13px; opacity: 0.7; margin-top: 8px;">{sub}</div>
    </div>
    {arrow}"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; }}
  .steps {{ display: flex; gap: 16px; align-items: center; margin-bottom: 40px; }}
  .agent-box {{ background: #F5F5F5; border: 2px solid var(--coral); border-radius: 6px; padding: 28px 36px; display: flex; align-items: center; gap: 20px; }}
  .agent-box .badge {{ background: var(--coral); color: white; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: 700; }}
  .result-row {{ display: flex; gap: 20px; margin-top: auto; }}
  .result-card {{ flex: 1; background: #F5F5F5; border-radius: 6px; padding: 20px; text-align: center; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">HOW — 어떻게 분석하는가?</div>
      <div class="slide-title">분석 프레임워크 & Multi-Agent AI</div>
      <div class="title-underline"></div>
      <div class="steps">{step_html}</div>
      <div class="agent-box">
        <div class="badge">Multi-Agent AI</div>
        <div style="flex: 1;">
          <div style="font-size: 18px; font-weight: 700;">EDA ~ 모델링 구간은 Multi-Agent AI가 자동 수행</div>
          <div style="font-size: 14px; color: var(--gray-500); margin-top: 6px;">18개 에이전트 · SOP 기반 · 분석 재현성 100%</div>
        </div>
        <div style="font-size: 14px; color: var(--teal); font-weight: 600;">일관성 보장 ✓</div>
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_07_result(page=7):
  """RESULT — 문제 정의 & 기대 결과물"""
  deliverables = [
    ("📊", "분석 리포트", "9개 가설 검증, SHAP 해석"),
    ("🖥️", "대시보드", "RevPAR 예측 + 최적화 가이드"),
    ("📧", "자동화", "이메일 알림 + 위험 감지"),
    ("🤖", "AI 시스템", "Multi-Agent 분석 자동화"),
  ]
  cards = ""
  for icon, title, sub in deliverables:
    cards += f"""
    <div class="card" style="flex: 1; text-align: center;">
      <div style="font-size: 40px; margin-bottom: 16px;">{icon}</div>
      <div style="font-size: 18px; font-weight: 700;">{title}</div>
      <div style="font-size: 14px; color: var(--gray-500); margin-top: 8px;">{sub}</div>
    </div>"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; }}
  .problem-box {{ background: #F5F5F5; border-left: 6px solid var(--coral); border-radius: 0 6px 6px 0; padding: 36px 44px; font-size: 22px; font-weight: 600; line-height: 1.6; margin-bottom: 40px; }}
  .deliverables {{ display: flex; gap: 24px; flex: 1; align-items: center; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">RESULT — 무엇을 만드는가?</div>
      <div class="slide-title">문제 정의 & 기대 결과물</div>
      <div class="title-underline"></div>
      <div class="problem-box">
        호스트가 통제 가능한 변수만으로 RevPAR를 극대화하는<br>
        <span style="color: var(--coral);">데이터 기반 의사결정 체계</span>를 구축한다
      </div>
      <div class="deliverables">{cards}</div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_12_eda_top5(page=12):
  """호스트 관점 EDA — 핵심 발견 Top 5"""
  findings = [
    ("H1", "슈퍼호스트 프리미엄", "+83.1%", "RevPAR", "var(--coral)"),
    ("H3", "사진 최적 구간", "21~35장", "r=0.30", "var(--teal)"),
    ("H4", "최소숙박 최적점", "2~3박", "RevPAR 최대", "var(--coral)"),
    ("H5", "추가요금 역효과", "-55.9%", "7인 이상", "#E67E22"),
    ("★", "Perfectionism Paradox", "4.85~4.95", "최적 평점", "#8E44AD"),
  ]
  cards = ""
  for tag, title, num, sub, color in findings:
    cards += f"""
    <div class="card" style="flex: 1; text-align: center; position: relative; overflow: hidden;">
      <div style="position: absolute; top: 16px; left: 16px; background: {color}; color: white; padding: 4px 12px; border-radius: 8px; font-size: 13px; font-weight: 700;">{tag}</div>
      <div style="font-size: 48px; font-weight: 900; color: {color}; margin-top: 24px;">{num}</div>
      <div style="font-size: 16px; font-weight: 700; margin-top: 12px;">{title}</div>
      <div style="font-size: 14px; color: var(--gray-500); margin-top: 6px;">{sub}</div>
    </div>"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; }}
  .top-sub {{ font-size: 16px; color: var(--gray-500); margin-bottom: 40px; }}
  .findings {{ display: flex; gap: 20px; flex: 1; align-items: center; }}
  .badge-row {{ margin-top: 24px; text-align: center; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">EDA</div>
      <div class="slide-title">호스트 관점 — 핵심 발견 Top 5</div>
      <div class="title-underline"></div>
      <div class="top-sub">9개 가설 중 7개 채택 · 호스트가 즉시 바꿀 수 있는 5가지</div>
      <div class="findings">{cards}</div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_17_dual_model(page=17):
  """Dual Model 아키텍처"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 80px; height: 100%; display: flex; flex-direction: column; }}
  .flow {{ display: flex; gap: 20px; align-items: center; flex: 1; }}
  .flow-card {{ border-radius: 6px; padding: 32px 28px; text-align: center; }}
  .flow-arrow {{ font-size: 28px; color: var(--gray-300); }}
  .bottom-msg {{ margin-top: 28px; padding: 24px 36px; background: #F5F5F5; border-radius: 6px; font-size: 18px; font-weight: 600; text-align: center; }}
  .feature-list {{ font-size: 13px; color: rgba(255,255,255,0.8); text-align: left; margin-top: 12px; line-height: 1.8; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">모델링 A</div>
      <div class="slide-title">Dual Model 아키텍처 — ADR × Occupancy 분리 예측</div>
      <div class="title-underline"></div>
      <div class="flow">
        <div class="flow-card" style="flex: 1.2; background: #2B2B3D; color: white;">
          <div style="font-size: 13px; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 6px; display: inline-block; margin-bottom: 12px;">Model A</div>
          <div style="font-size: 22px; font-weight: 700;">ADR 예측</div>
          <div style="font-size: 14px; opacity: 0.6; margin-top: 4px;">시장이 결정하는 적정 가격</div>
          <div class="feature-list">· 위치 (자치구)<br>· 숙소 규모 (침실·욕실)<br>· POI 근접도</div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-card" style="flex: 0.8; background: var(--coral); color: white;">
          <div style="font-size: 13px; background: rgba(255,255,255,0.25); padding: 4px 12px; border-radius: 6px; display: inline-block; margin-bottom: 12px;">Bridge</div>
          <div style="font-size: 22px; font-weight: 700;">price_gap</div>
          <div style="font-size: 14px; opacity: 0.8; margin-top: 8px;">현재 ADR − 예측 ADR</div>
          <div style="font-size: 13px; opacity: 0.6; margin-top: 4px;">가격 괴리 정량화</div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-card" style="flex: 1.2; background: var(--teal); color: white;">
          <div style="font-size: 13px; background: rgba(255,255,255,0.25); padding: 4px 12px; border-radius: 6px; display: inline-block; margin-bottom: 12px;">Model B</div>
          <div style="font-size: 22px; font-weight: 700;">Occupancy 예측</div>
          <div style="font-size: 14px; opacity: 0.6; margin-top: 4px;">호스트가 통제하는 점유율</div>
          <div class="feature-list">· 예약 정책, 리뷰, 평점<br>· 사진 + price_gap</div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-card" style="flex: 0.8; background: #F5F5F5; color: var(--charcoal); border: 2px solid var(--gray-200);">
          <div style="font-size: 13px; background: var(--gray-200); padding: 4px 12px; border-radius: 6px; display: inline-block; margin-bottom: 12px;">Calibration</div>
          <div style="font-size: 22px; font-weight: 700;">Isotonic</div>
          <div style="font-size: 14px; color: var(--gray-500); margin-top: 8px;">단조증가 보정<br>→ 최종 RevPAR</div>
        </div>
      </div>
      <div class="bottom-msg">
        ADR과 점유율은 서로 다른 운전자 → <span style="color: var(--coral);">분리해야 호스트가 각각 조종 가능</span>
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_21_health_score(page=21):
  """건강점수 5컴포넌트"""
  components = [
    ("리뷰 신호", "20%", "리뷰수 + 평점 백분위", "var(--coral)"),
    ("사진 품질", "20%", "23~35장 = 100점", "var(--teal)"),
    ("예약 정책", "20%", "즉시예약·최소박·추가요금", "#E67E22"),
    ("위치", "20%", "POI 근접도 역백분위", "#3498DB"),
    ("숙소 구성", "20%", "침실·욕실 백분위", "#8E44AD"),
  ]
  comp_html = ""
  for name, weight, desc, color in components:
    comp_html += f"""
    <div style="display: flex; align-items: center; gap: 16px; padding: 16px 0; border-bottom: 1px solid var(--gray-200);">
      <div style="width: 12px; height: 12px; border-radius: 50%; background: {color};"></div>
      <div style="flex: 1; font-size: 18px; font-weight: 600;">{name}</div>
      <div style="font-size: 16px; font-weight: 700; color: {color};">{weight}</div>
      <div style="font-size: 14px; color: var(--gray-500); width: 240px;">{desc}</div>
    </div>"""

  grades = [("A", "≥ 80", "상위 20%", "var(--teal)"), ("B", "≥ 60", "양호", "#3498DB"), ("C", "≥ 40", "보통", "#E67E22"), ("D", "≥ 20", "취약", "var(--coral)"), ("F", "< 20", "위험", "#E74C3C")]
  grade_html = ""
  for g, rng, meaning, color in grades:
    grade_html += f"""
    <div style="display: flex; align-items: center; gap: 12px; padding: 8px 0;">
      <div style="width: 36px; height: 36px; border-radius: 8px; background: {color}; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px;">{g}</div>
      <div style="font-size: 14px; color: var(--gray-500);">{rng}</div>
      <div style="font-size: 14px; font-weight: 600;">{meaning}</div>
    </div>"""

  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; }}
  .content {{ display: flex; gap: 40px; flex: 1; }}
  .left {{ flex: 1.2; }}
  .right {{ flex: 0.8; display: flex; flex-direction: column; gap: 20px; }}
  .example {{ background: #F5F5F5; border-radius: 6px; padding: 20px; font-size: 15px; line-height: 1.6; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">모델링 B</div>
      <div class="slide-title">숙소 건강점수 — 5컴포넌트 × A~F 등급</div>
      <div class="title-underline"></div>
      <div class="content">
        <div class="left">
          <div class="card" style="padding: 28px 32px;">
            <div style="font-size: 14px; color: var(--gray-500); font-weight: 600; letter-spacing: 1px; margin-bottom: 12px;">건강점수 (0~100)</div>
            {comp_html}
          </div>
        </div>
        <div class="right">
          <div class="card" style="padding: 24px;">
            <div style="font-size: 14px; color: var(--gray-500); font-weight: 600; letter-spacing: 1px; margin-bottom: 12px;">등급 매트릭스</div>
            {grade_html}
          </div>
          <div class="example">
            <strong>예시:</strong> 마포구 원룸, 리뷰 12건, 평점 4.6<br>
            → 건강점수 <strong style="color: #E67E22;">C (52점)</strong> — 사진·예약정책 취약
          </div>
        </div>
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_23_cluster_result(page=23):
  """자치구 군집 결과 — 4대 시장"""
  clusters = [
    ("C1", "핫플 수익형", "마포구", "₩63,366", "품질 밀도 강화, 공급 과잉 경계", "var(--coral)"),
    ("C2", "프리미엄 비즈니스", "강남·종로·용산", "₩53,052", "슈퍼호스트 전환 인센티브", "var(--teal)"),
    ("C3", "로컬 주거형", "13개 자치구", "₩35,881", "사진·평점 표준 가이드", "#3498DB"),
    ("C4", "가성비 신흥형", "동대문·관악 등", "₩26,413", "Dormant 63.3%, 비활성 정리", "#E67E22"),
  ]
  cards = ""
  for i, (cid, name, districts, revpar, strategy, color) in enumerate(clusters):
    cards += f"""
    <div class="card" style="flex: 1; position: relative; overflow: hidden;">
      <div style="position: absolute; top: 0; left: 0; right: 0; height: 6px; background: {color};"></div>
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
        <div style="background: {color}; color: white; padding: 4px 12px; border-radius: 8px; font-size: 14px; font-weight: 700;">{cid}</div>
        <div style="font-size: 18px; font-weight: 700;">{name}</div>
      </div>
      <div style="font-size: 40px; font-weight: 900; color: {color}; margin: 12px 0;">{revpar}</div>
      <div style="font-size: 14px; color: var(--gray-500); margin-bottom: 12px;">{districts}</div>
      <div style="font-size: 13px; background: var(--gray-100); padding: 10px 14px; border-radius: 8px; color: var(--charcoal);">{strategy}</div>
    </div>"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; }}
  .top-sub {{ font-size: 16px; color: var(--gray-500); margin-bottom: 36px; }}
  .grid {{ display: flex; gap: 24px; flex: 1; align-items: stretch; }}
  .bottom {{ margin-top: 24px; text-align: center; font-size: 16px; color: var(--gray-500); }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">모델링 C</div>
      <div class="slide-title">자치구 군집 결과 — 4대 시장 전략</div>
      <div class="title-underline"></div>
      <div class="top-sub">K-Means (k=4) · 25개 자치구 군집화</div>
      <div class="grid">{cards}</div>
      <div class="bottom">이 군집 결과가 대시보드의 <strong>'자치구 벤치마킹'</strong> 기능으로 이어집니다</div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_25_biz_model(page=25):
  """비즈니스 모델 개요"""
  tiers = [
    ("Free", "이메일 자동화", ["리스팅 사전 분석", "위험 신호 알림", "Google Sheets 연동"], "무료", "var(--gray-200)", "var(--charcoal)"),
    ("Basic", "대시보드 (무료)", ["RevPAR 예측", "기본 최적화 가이드", "액션 추천"], "₩9,900/월", "white", "var(--charcoal)"),
    ("Pro", "대시보드 (유료)", ["자치구 벤치마킹", "리얼타임 모니터링", "위험 감지 알림"], "₩29,900/월", "var(--teal)", "white"),
    ("Enterprise", "AI Orchestration", ["Multi-Agent 자동분석", "맞춤형 가설 검증", "자동 리포팅"], "문의", "var(--coral)", "white"),
  ]
  cards = ""
  for name, sub, features, price, bg, text_color in tiers:
    feat_html = "".join(f'<div style="padding: 6px 0; font-size: 14px;">· {f}</div>' for f in features)
    bg_style = f"background: {bg};"
    cards += f"""
    <div style="{bg_style} color: {text_color}; border-radius: 6px; padding: 32px 28px; flex: 1; display: flex; flex-direction: column;">
      <div style="font-size: 14px; opacity: 0.6; font-weight: 600;">{name}</div>
      <div style="font-size: 20px; font-weight: 700; margin: 8px 0 20px;">{sub}</div>
      <div style="flex: 1;">{feat_html}</div>
      <div style="margin-top: 20px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.2); font-size: 22px; font-weight: 900;">{price}</div>
    </div>"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; }}
  .tiers {{ display: flex; gap: 24px; flex: 1; align-items: stretch; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">대시보드 · 자동화</div>
      <div class="slide-title">비즈니스 모델 개요</div>
      <div class="title-underline"></div>
      <div class="tiers">{cards}</div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_29_risk_rules(page=29):
  """위험 감지 엔진 R1~R5"""
  rules = [
    ("R1", "유령수익", "Phantom Revenue", "리뷰 0건 + 수익 > 1,000만", "HIGH", "var(--coral)"),
    ("R2", "점유율-수익 불일치", "Mismatch", "점유율 = 0% & 수익 > 0", "HIGH", "var(--coral)"),
    ("R3", "가격 이상치", "Rate Outlier", "ADR > 구 평균 + 3σ & 리뷰 < 5", "MEDIUM", "#E67E22"),
    ("R4", "유령 액티브", "Ghost Active", "Active 상태 & 수익 < 500만", "MEDIUM", "#E67E22"),
    ("R5", "평점 없는 고수익", "No Rating", "수익 > 1,000만 & 평점 결측", "HIGH", "var(--coral)"),
  ]
  cards = ""
  for rid, name, eng, condition, level, color in rules:
    level_bg = "rgba(255,90,95,0.12)" if level == "HIGH" else "rgba(230,126,34,0.12)"
    cards += f"""
    <div class="card" style="flex: 1; position: relative; overflow: hidden;">
      <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: {color};"></div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="background: {color}; color: white; padding: 4px 12px; border-radius: 8px; font-size: 14px; font-weight: 700;">{rid}</div>
        <div style="background: {level_bg}; color: {color}; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700;">{level}</div>
      </div>
      <div style="font-size: 18px; font-weight: 700; margin-top: 8px;">{name}</div>
      <div style="font-size: 13px; color: var(--gray-400); margin-top: 2px;">{eng}</div>
      <div style="font-size: 14px; color: var(--gray-600); margin-top: 12px; background: var(--gray-100); padding: 10px 12px; border-radius: 8px;">{condition}</div>
    </div>"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 80px; height: 100%; display: flex; flex-direction: column; }}
  .rules {{ display: flex; gap: 20px; margin-bottom: 32px; }}
  .bottom-row {{ display: flex; gap: 24px; }}
  .bottom-card {{ flex: 1; background: #F5F5F5; border-radius: 6px; padding: 24px; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">자동화</div>
      <div class="slide-title">위험 감지 엔진 — R1~R5 규칙</div>
      <div class="title-underline"></div>
      <div class="rules">{cards}</div>
      <div class="bottom-row">
        <div class="bottom-card">
          <div style="font-size: 14px; color: var(--gray-500); font-weight: 600; margin-bottom: 12px;">통계 이상치 보조</div>
          <div style="font-size: 15px;">· <strong>IQR 기반</strong>: 자치구 내 수익 범위 밖 → 지역 이상치<br>· <strong>Z-score</strong>: 전체 ADR Z > 3.0 → 글로벌 이상치</div>
        </div>
        <div class="bottom-card">
          <div style="font-size: 14px; color: var(--gray-500); font-weight: 600; margin-bottom: 12px;">리스크 레벨 분류</div>
          <div style="font-size: 15px;">· <strong style="color: var(--coral);">HIGH</strong>: 2개+ 규칙 동시 트리거<br>· <strong style="color: #E67E22;">MEDIUM</strong>: 1개 규칙 또는 통계 이상치</div>
        </div>
        <div class="bottom-card">
          <div style="font-size: 14px; color: var(--gray-500); font-weight: 600; margin-bottom: 12px;">중복 필터</div>
          <div style="font-size: 15px;">· 동일 리스팅 <strong>7일 내</strong> 재알림 방지<br>· duplicate_tracker.py</div>
        </div>
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_31_multi_agent(page=31):
  """Multi-Agent AI 아키텍처"""
  agents = [
    ("Domain\nResearch", "도메인 지식", "var(--coral)"),
    ("Hypothesis", "H1~H9 자동 생성", "#E67E22"),
    ("EDA ×3", "38개 차트, 통계", "var(--teal)"),
    ("Feature\nEngineering", "14개 파생변수", "#3498DB"),
    ("Modeling", "LightGBM + SHAP", "#8E44AD"),
    ("Model\nReview", "누수 검출, 품질", "#2C3E50"),
  ]
  agent_html = ""
  for name, desc, color in agents:
    name_display = name.replace('\n', '<br>')
    agent_html += f"""
    <div style="flex: 1; background: #F5F5F5; border-radius: 6px; padding: 24px 16px; text-align: center; border-top: 4px solid {color};">
      <div style="font-size: 17px; font-weight: 700; line-height: 1.4;">{name_display}</div>
      <div style="font-size: 13px; color: var(--gray-500); margin-top: 8px;">{desc}</div>
    </div>"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 70px 80px; height: 100%; display: flex; flex-direction: column; }}
  .orch {{ background: var(--coral); color: white; border-radius: 6px; padding: 24px 40px; text-align: center; margin-bottom: 20px; }}
  .arrow-down {{ text-align: center; font-size: 28px; color: var(--gray-300); margin: 8px 0; }}
  .agents {{ display: flex; gap: 16px; margin-bottom: 20px; }}
  .results {{ display: flex; gap: 20px; margin-top: auto; }}
  .result-card {{ flex: 1; background: #F5F5F5; border-radius: 6px; padding: 20px; text-align: center; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">대시보드 · 자동화</div>
      <div class="slide-title">Multi-Agent AI 아키텍처</div>
      <div class="title-underline"></div>
      <div class="orch">
        <div style="font-size: 14px; opacity: 0.7;">Central</div>
        <div style="font-size: 24px; font-weight: 700;">Orchestrator</div>
        <div style="font-size: 14px; opacity: 0.7; margin-top: 4px;">SOP 기반 순차 호출 · JSON 산출물 관리</div>
      </div>
      <div class="arrow-down">↓</div>
      <div class="agents">{agent_html}</div>
      <div class="arrow-down">↓</div>
      <div class="results">
        <div class="result-card">
          <div style="font-size: 36px; font-weight: 900; color: var(--coral);">9</div>
          <div style="font-size: 14px; color: var(--gray-500);">가설 검증</div>
        </div>
        <div class="result-card">
          <div style="font-size: 36px; font-weight: 900; color: var(--teal);">14</div>
          <div style="font-size: 14px; color: var(--gray-500);">파생변수</div>
        </div>
        <div class="result-card">
          <div style="font-size: 36px; font-weight: 900; color: #3498DB;">38</div>
          <div style="font-size: 14px; color: var(--gray-500);">차트</div>
        </div>
        <div class="result-card">
          <div style="font-size: 36px; font-weight: 900; color: #8E44AD;">R² 0.85</div>
          <div style="font-size: 14px; color: var(--gray-500);">모델 성능</div>
        </div>
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_33_impact(page=33):
  """프로젝트 임팩트 요약"""
  metrics = [
    ("R² = 0.85", "Dual Model로 RevPAR의 85% 설명", "var(--coral)"),
    ("5컴포넌트", "건강점수로 숙소 상태 종합 진단", "var(--teal)"),
    ("5규칙 24/7", "위험 감지 엔진이 쉬지 않고 감시", "#3498DB"),
    ("End-to-End", "분석 → 대시보드 → 자동화 → AI", "#8E44AD"),
  ]
  cards = ""
  for metric, desc, color in metrics:
    cards += f"""
    <div class="card" style="flex: 1; text-align: center; border-top: 5px solid {color};">
      <div style="font-size: 42px; font-weight: 900; color: {color}; margin-bottom: 16px;">{metric}</div>
      <div style="font-size: 16px; color: var(--gray-600); line-height: 1.5;">{desc}</div>
    </div>"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; justify-content: center; }}
  .metrics {{ display: flex; gap: 28px; margin-bottom: 50px; }}
  .slogan {{ text-align: center; font-size: 24px; font-weight: 700; color: var(--coral); }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb" style="text-align: center;">종합</div>
      <div class="slide-title" style="text-align: center; font-size: 36px; margin-bottom: 50px;">프로젝트 임팩트 요약</div>
      <div class="metrics">{cards}</div>
      <div class="slogan">"데이터로 호스트의 수익을 설계하다"</div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_34_thankyou(page=34):
  """Q&A — 중앙 coral 라운드 카드 스타일"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .qa-wrap {{ display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; background: #FFFFFF; }}
  .qa-card {{ background: var(--coral); border-radius: 24px; padding: 80px 120px; text-align: center; color: white; }}
  .qa-icon {{ font-size: 56px; margin-bottom: 24px; }}
  .qa-title {{ font-size: 56px; font-weight: 800; letter-spacing: 4px; }}
  .qa-subtitle {{ font-size: 20px; color: rgba(255,255,255,0.85); margin-top: 16px; font-weight: 400; }}
  .qa-team {{ margin-top: 48px; font-size: 14px; color: var(--gray-500); }}
  </style></head><body>
  <div class="slide" style="background: #FFFFFF; overflow: hidden;">
    <div class="qa-wrap">
      <div class="qa-card">
        <div class="qa-icon">💬</div>
        <div class="qa-title">Q & A</div>
        <div class="qa-subtitle">질문과 의견을 환영합니다</div>
      </div>
      <div class="qa-team">4조 · 데이터분석 부트캠프 · 2026</div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_09_data_overview(page=9):
  """데이터 소개 & 품질 이슈"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; }}
  .content {{ display: flex; gap: 36px; flex: 1; }}
  .left {{ flex: 1; }}
  .right {{ flex: 1; display: flex; flex-direction: column; gap: 16px; }}
  table {{ width: 100%; border-collapse: separate; border-spacing: 0; }}
  th {{ text-align: left; padding: 14px 20px; font-size: 14px; font-weight: 600; }}
  td {{ padding: 16px 20px; border-bottom: 1px solid var(--gray-200); font-size: 16px; }}
  th:first-child {{ border-radius: 6px 0 0 0; }} th:last-child {{ border-radius: 0 6px 0 0; }}
  .issue-card {{ background: #F5F5F5; border-radius: 6px; padding: 20px 24px; display: flex; gap: 16px; align-items: flex-start; }}
  .issue-icon {{ font-size: 24px; }}
  .issue-title {{ font-size: 15px; font-weight: 700; }}
  .issue-desc {{ font-size: 13px; color: var(--gray-500); margin-top: 4px; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">데이터 개요</div>
      <div class="slide-title">데이터 소개 & 품질 이슈 대응</div>
      <div class="title-underline"></div>
      <div class="content">
        <div class="left">
          <div class="card" style="padding: 0; overflow: hidden;">
            <table>
              <tr><th>항목</th><th>값</th></tr>
              <tr><td style="font-weight:600;">원본</td><td>32,061행 × 42열</td></tr>
              <tr><td style="font-weight:600;">기간</td><td>2024.10 ~ 2025.09 (TTM 12개월)</td></tr>
              <tr><td style="font-weight:600;">서브셋</td><td>Active+Operating <strong>14,399</strong>개</td></tr>
              <tr><td style="font-weight:600;">외부 데이터</td><td>POI, 환율, 인구 병합</td></tr>
            </table>
          </div>
        </div>
        <div class="right">
          <div class="issue-card">
            <div class="issue-icon">🔧</div>
            <div>
              <div class="issue-title">district 결측치</div>
              <div class="issue-desc">Spatial Join으로 좌표 기반 자치구 보정</div>
            </div>
          </div>
          <div class="issue-card">
            <div class="issue-icon">🔧</div>
            <div>
              <div class="issue-title">이상치 제거</div>
              <div class="issue-desc">min_nights > 730, ADR > 200만 필터링</div>
            </div>
          </div>
          <div class="issue-card">
            <div class="issue-icon">🔧</div>
            <div>
              <div class="issue-title">상수 컬럼 제외</div>
              <div class="issue-desc">exng, ttm_exng (분산 0)</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_10_feature_eng(page=10):
  """피처 엔지니어링 — 전처리 관점, 변수 유형별 분류"""
  # 구간화 변수
  group_features = [
    ("photos_tier", "사진 수 → 구간 분류", "0~10 / 11~20 / 21~35 / 36+"),
    ("bedrooms_group", "침실 수 → 구간 분류", "0 / 1 / 2 / 3+"),
    ("baths_group", "욕실 수 → 구간 분류", "1 / 1.5 / 2 / 2.5+"),
    ("guests_group", "수용 인원 → 구간 분류", "1~2 / 3~4 / 5~6 / 7+"),
  ]
  # 비율·지표 변수
  ratio_features = [
    ("poi_dist_category", "POI 거리 카테고리화", "도보권 / 근거리 / 원거리 등급"),
    ("extra_guest_fee_policy", "추가요금 유무 이진화", "추가인원 요금 있음/없음"),
    ("revpar_trend", "최근 90일 vs 연평균", "수익 방향성 (성장/하락)"),
  ]

  group_cards = ""
  for name, desc, note in group_features:
    group_cards += f"""
      <div class="feat-card">
        <code class="feat-name">{name}</code>
        <div class="feat-desc">{desc}</div>
        <div class="feat-note">{note}</div>
      </div>"""

  ratio_cards = ""
  for name, desc, note in ratio_features:
    ratio_cards += f"""
      <div class="feat-card feat-card-teal">
        <code class="feat-name feat-name-teal">{name}</code>
        <div class="feat-desc">{desc}</div>
        <div class="feat-note">{note}</div>
      </div>"""

  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 56px 100px 44px; height: 100%; display: flex; flex-direction: column; }}
  .subtitle-row {{ display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }}
  .badge {{ display: inline-flex; align-items: center; gap: 6px; padding: 7px 18px; border-radius: 20px; font-size: 14px; font-weight: 600; }}
  .badge-coral {{ background: rgba(255,90,95,0.1); color: var(--coral); }}
  .badge-teal {{ background: rgba(0,166,153,0.1); color: var(--teal); }}
  .badge-gray {{ background: var(--gray-100); color: var(--gray-500); }}

  .section-label {{ font-size: 16px; font-weight: 700; color: var(--charcoal); margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }}
  .section-label .dot {{ width: 10px; height: 10px; border-radius: 50%; }}

  /* 카드 그리드 */
  .feat-grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin-bottom: 40px; }}
  .feat-card {{
    background: var(--gray-100); border-radius: 10px; padding: 36px 26px 32px;
    border-left: 4px solid var(--coral);
    min-height: 195px;
    display: flex; flex-direction: column; justify-content: center;
  }}
  .feat-card-teal {{ border-left-color: var(--teal); }}
  .feat-name {{
    display: inline-block; background: white; padding: 6px 16px; border-radius: 6px;
    font-size: 15px; font-weight: 700; color: var(--coral); font-family: 'SF Mono', 'Fira Code', monospace;
    letter-spacing: -0.3px; margin-bottom: 20px; border: 1px solid rgba(255,90,95,0.15);
    align-self: flex-start;
  }}
  .feat-name-teal {{ color: var(--teal); border-color: rgba(0,166,153,0.2); }}
  .feat-desc {{ font-size: 18px; font-weight: 600; color: var(--charcoal); margin-bottom: 10px; }}
  .feat-note {{ font-size: 14px; color: var(--gray-500); line-height: 1.5; }}

  /* 타겟 변환 카드 (특별) */
  .target-card {{
    background: rgba(0,166,153,0.06); border-radius: 10px; padding: 36px 26px 32px;
    border-left: 4px solid var(--teal);
    min-height: 195px;
    display: flex; flex-direction: column; justify-content: center;
  }}
  .target-card code {{ color: var(--teal); border-color: rgba(0,166,153,0.2); }}

  /* 인사이트 박스 */
  .insight-bar {{
    background: var(--insight-bg); border-left: 4px solid var(--coral);
    border-radius: 0 10px 10px 0; padding: 28px 36px;
  }}
  .insight-title {{ font-size: 17px; font-weight: 700; color: var(--charcoal); margin-bottom: 16px; }}
  .insight-points {{ display: flex; gap: 48px; }}
  .insight-point {{ font-size: 15px; color: var(--charcoal); line-height: 1.7; }}
  .insight-point strong {{ color: var(--coral); }}

  /* 하단 바 */
  .bottom-bar {{ display: flex; gap: 24px; margin-top: 20px; }}
  .bottom-card {{
    flex: 1; border-radius: 10px; padding: 24px 28px;
    display: flex; align-items: center; gap: 20px;
  }}
  .bottom-card-teal {{ background: rgba(0,166,153,0.08); border-left: 4px solid var(--teal); }}
  .bottom-card-coral {{ background: rgba(255,90,95,0.06); border-left: 4px solid var(--coral); }}
  .bottom-num {{ font-size: 42px; font-weight: 900; line-height: 1; }}
  .bottom-label {{ font-size: 14px; color: var(--gray-600); line-height: 1.6; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">전처리</div>
      <div class="slide-title">피처 엔지니어링 — 원본 데이터를 분석 가능한 형태로</div>
      <div class="title-underline" style="width: 360px;"></div>

      <div class="subtitle-row">
        <span class="badge badge-coral">구간화 4개</span>
        <span class="badge badge-teal">비율·지표 3개</span>
        <span class="badge badge-gray">타겟 변환 1개</span>
        <span style="font-size: 13px; color: var(--gray-500);">원본 42열 → 14개 파생변수 추가 생성</span>
      </div>

      <!-- 구간화 변수 -->
      <div class="section-label">
        <div class="dot" style="background: var(--coral);"></div>
        구간화 — 연속형 변수를 의미 있는 구간으로 변환
      </div>
      <div class="feat-grid-4">
        {group_cards}
      </div>

      <!-- 비율·지표 + 타겟 변환 -->
      <div class="section-label">
        <div class="dot" style="background: var(--teal);"></div>
        비율·지표 — 기존 컬럼을 조합하여 새로운 의미 부여
      </div>
      <div class="feat-grid-4">
        {ratio_cards}
        <div class="target-card">
          <code class="feat-name feat-name-teal">log_ttm_revpar</code>
          <div class="feat-desc">RevPAR → log1p 변환</div>
          <div class="feat-note">skewness 3.76 → 정규분포화</div>
        </div>
      </div>

      <!-- 인사이트 -->
      <div class="insight-bar">
        <div class="insight-title">왜 이런 변수를 만들었나?</div>
        <div class="insight-points">
          <div class="insight-point"><strong>→</strong> 사진 21장과 22장의 차이는 무의미 — 의미 있는 구간으로 묶어 패턴 탐지</div>
          <div class="insight-point"><strong>→</strong> 기존 컬럼의 비율·조합으로 숨은 패턴을 드러냄</div>
          <div class="insight-point"><strong>→</strong> RevPAR 분포가 극단적으로 치우쳐 log 변환으로 분석 안정성 확보</div>
        </div>
      </div>

      <!-- 하단 바 -->
      <div class="bottom-bar">
        <div class="bottom-card bottom-card-teal">
          <div class="bottom-num" style="color: var(--teal);">14</div>
          <div class="bottom-label">파생변수 생성<br>원본 42열에서 추가 파생</div>
        </div>
        <div class="bottom-card bottom-card-coral">
          <div class="bottom-num" style="color: var(--coral);">4+3+1</div>
          <div class="bottom-label">구간화 · 비율 · 타겟<br>세 가지 유형으로 설계</div>
        </div>
        <div class="bottom-card" style="background: var(--gray-100); border-left: 4px solid var(--gray-400);">
          <div class="bottom-num" style="color: var(--charcoal);">log1p</div>
          <div class="bottom-label">타겟 변환<br>skewness 3.76 → 정규분포화</div>
        </div>
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_19_performance(page=19):
  """호스트 모델 성능 비교"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 100px; height: 100%; display: flex; flex-direction: column; }}
  table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin-bottom: 36px; }}
  th {{ padding: 16px 24px; font-size: 15px; font-weight: 600; text-align: center; }}
  td {{ padding: 18px 24px; border-bottom: 1px solid var(--gray-200); font-size: 17px; text-align: center; }}
  th:first-child {{ border-radius: 6px 0 0 0; text-align: left; }} th:last-child {{ border-radius: 0 6px 0 0; }}
  tr.highlight td {{ background: rgba(255,90,95,0.04); font-weight: 700; }}
  .insights {{ display: flex; gap: 24px; }}
  .insight {{ flex: 1; background: #F5F5F5; border-radius: 6px; padding: 24px 28px; text-align: center; }}
  .insight .num {{ font-size: 32px; font-weight: 900; margin-bottom: 8px; }}
  .insight .label {{ font-size: 14px; color: var(--gray-500); }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">모델링 A</div>
      <div class="slide-title">호스트 모델 — 성능 비교</div>
      <div class="title-underline"></div>
      <div class="card" style="padding: 0; overflow: hidden; margin-bottom: 36px;">
        <table>
          <tr><th style="text-align:left;">모델</th><th>CV R²</th><th>Test R²</th><th>Test MAE</th><th>Test MAPE</th></tr>
          <tr class="highlight">
            <td style="text-align:left; color: var(--coral);">LightGBM</td>
            <td><strong>0.847</strong></td><td><strong>0.85</strong></td><td><strong>₩19,554</strong></td><td><strong>32.6%</strong></td>
          </tr>
          <tr><td style="text-align:left;">Random Forest</td><td>0.744</td><td>0.75</td><td>₩24,470</td><td>45.6%</td></tr>
          <tr><td style="text-align:left;">Ridge</td><td>0.579</td><td>0.57</td><td>₩27,595</td><td>70.4%</td></tr>
          <tr><td style="text-align:left; color: var(--gray-400);">Baseline (중위값)</td><td>-0.025</td><td>—</td><td>—</td><td>—</td></tr>
        </table>
      </div>
      <div class="insights">
        <div class="insight">
          <div class="num" style="color: var(--coral);">85%</div>
          <div class="label">호스트 통제 변수만으로<br>RevPAR 설명</div>
        </div>
        <div class="insight">
          <div class="num" style="color: var(--teal);">+0.875</div>
          <div class="label">Baseline 대비 R² 개선<br>→ 모델 존재 가치 증명</div>
        </div>
        <div class="insight">
          <div class="num" style="color: var(--charcoal);">₩19,554</div>
          <div class="label">평균 예측 오차<br>→ 실무 의사결정 활용 수준</div>
        </div>
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_20_shap(page=20):
  """SHAP → 비즈니스 액션"""
  actions = [
    ("num_reviews", "0.51", "리뷰 요청 자동화", "🥇", "var(--coral)"),
    ("review_rate", "0.33", "체크아웃 후 리마인더", "🥈", "var(--teal)"),
    ("rating_overall", "0.12", "4.85~4.95 유지", "🥉", "#E67E22"),
    ("min_nights", "0.08", "2~3박 설정", "4", "#3498DB"),
    ("photos_count", "0.07", "21~35장 업로드", "5", "#8E44AD"),
  ]
  # 좌측: SHAP 바
  bars = ""
  for feat, imp, _, _, color in actions:
    width = float(imp) * 100 / 0.51 * 80  # max 80%
    bars += f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 14px;">
      <div style="width: 140px; text-align: right; font-size: 14px; font-weight: 600;">{feat}</div>
      <div style="flex: 1; height: 32px; background: var(--gray-100); border-radius: 6px; overflow: hidden;">
        <div style="width: {width}%; height: 100%; background: {color}; border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 10px;">
          <span style="color: white; font-size: 13px; font-weight: 700;">{imp}</span>
        </div>
      </div>
    </div>"""
  # 우측: 액션 테이블
  rows = ""
  for feat, imp, action, rank, color in actions:
    rows += f"""
    <div style="display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--gray-200); gap: 12px;">
      <div style="font-size: 20px; width: 32px; text-align: center;">{rank}</div>
      <div style="flex: 1; font-size: 15px; font-weight: 600;">{action}</div>
      <div style="font-size: 13px; color: var(--gray-500);">{feat}</div>
    </div>"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 80px 80px; height: 100%; display: flex; flex-direction: column; }}
  .content {{ display: flex; gap: 36px; flex: 1; }}
  .left {{ flex: 1.1; }}
  .right {{ flex: 0.9; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">모델링 A</div>
      <div class="slide-title">SHAP → 비즈니스 액션</div>
      <div class="title-underline"></div>
      <div class="content">
        <div class="left">
          <div class="card">
            <div style="font-size: 14px; color: var(--gray-500); font-weight: 600; margin-bottom: 20px;">SHAP Feature Importance (Top 5)</div>
            {bars}
            <div style="margin-top: 12px; font-size: 13px; color: var(--gray-400);">호스트 통제 가능 변수 (컬러) vs 통제 불가 (회색)</div>
          </div>
        </div>
        <div class="right">
          <div class="card">
            <div style="font-size: 14px; color: var(--gray-500); font-weight: 600; margin-bottom: 16px;">SHAP → 액션 전환</div>
            {rows}
          </div>
        </div>
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_30_automation_flow(page=30):
  """자동화 시스템 전체 플로우"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 70px 80px; height: 100%; display: flex; flex-direction: column; }}
  .flow-section {{ background: #F5F5F5; border-radius: 6px; padding: 28px 32px; margin-bottom: 24px; }}
  .flow-label {{ font-size: 14px; font-weight: 700; color: var(--gray-500); letter-spacing: 1px; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}
  .flow-steps {{ display: flex; align-items: center; gap: 12px; }}
  .flow-step {{ background: white; border-radius: 6px; padding: 16px 20px; text-align: center; flex: 1; }}
  .flow-step-title {{ font-size: 14px; font-weight: 700; }}
  .flow-step-sub {{ font-size: 12px; color: var(--gray-400); margin-top: 4px; }}
  .flow-arrow {{ font-size: 20px; color: var(--gray-300); }}
  .bottom-box {{ background: var(--coral); color: white; border-radius: 6px; padding: 24px 36px; text-align: center; margin-top: auto; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">자동화</div>
      <div class="slide-title">자동화 시스템 — 전체 플로우</div>
      <div class="title-underline"></div>
      <div class="flow-section">
        <div class="flow-label"><span style="color: var(--coral);">●</span> 위험 감지 (risk_detection/)</div>
        <div class="flow-steps">
          <div class="flow-step"><div class="flow-step-title">데이터 변경</div><div class="flow-step-sub">hooks.py</div></div>
          <div class="flow-arrow">→</div>
          <div class="flow-step"><div class="flow-step-title">R1~R5 규칙</div><div class="flow-step-sub">detector.py</div></div>
          <div class="flow-arrow">→</div>
          <div class="flow-step"><div class="flow-step-title">IQR/Z-score</div><div class="flow-step-sub">scorer.py</div></div>
          <div class="flow-arrow">→</div>
          <div class="flow-step"><div class="flow-step-title">리스크 레벨</div><div class="flow-step-sub">중복필터 7일</div></div>
          <div class="flow-arrow">→</div>
          <div class="flow-step" style="background: rgba(255,90,95,0.1);"><div class="flow-step-title" style="color: var(--coral);">이메일 알림</div><div class="flow-step-sub">email_alert.py</div></div>
        </div>
      </div>
      <div class="flow-section">
        <div class="flow-label"><span style="color: var(--teal);">●</span> 호스트 사전 분석 (host_preview/)</div>
        <div class="flow-steps">
          <div class="flow-step"><div class="flow-step-title">URL 입력</div><div class="flow-step-sub">hooks.py</div></div>
          <div class="flow-arrow">→</div>
          <div class="flow-step"><div class="flow-step-title">이상신호 3종</div><div class="flow-step-sub">analyzer.py</div></div>
          <div class="flow-arrow">→</div>
          <div class="flow-step"><div class="flow-step-title">시장 포지셔닝</div><div class="flow-step-sub">4사분면</div></div>
          <div class="flow-arrow">→</div>
          <div class="flow-step"><div class="flow-step-title">건강점수 (blur)</div><div class="flow-step-sub">유료 전환 유도</div></div>
          <div class="flow-arrow">→</div>
          <div class="flow-step" style="background: rgba(0,166,153,0.1);"><div class="flow-step-title" style="color: var(--teal);">이메일 발송</div><div class="flow-step-sub">email_builder.py</div></div>
        </div>
      </div>
      <div class="bottom-box">
        <div style="font-size: 20px; font-weight: 700;">Claude Code Hooks로 자동화 — 호스트 개입 없이 24/7 동작</div>
      </div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""


def slide_32_action_guide(page=32):
  """호스트 액션 가이드"""
  actions = [
    ("🥇", "1", "리뷰 요청 자동화", "SHAP 1위 (0.51)", "+5~10% / 10건", "낮음", "var(--coral)"),
    ("🥈", "2", "슈퍼호스트 달성", "H1 검증 (+83.1%)", "+83.1% RevPAR", "중간", "var(--teal)"),
    ("🥉", "3", "최소숙박 2~3박", "H4 검증", "RevPAR 최적점", "낮음", "#E67E22"),
    ("", "4", "사진 21~35장", "H3 검증 (r=0.30)", "한계효용 최대", "낮음", "#3498DB"),
    ("", "5", "평점 4.85~4.95", "Paradox 발견", "최적 점유율", "중간", "#8E44AD"),
    ("", "6", "추가요금 7인+ 제거", "H5 검증", "+55.9% 회복", "낮음", "#95A5A6"),
    ("", "7", "Entire Home 전환", "H2 검증", "2.7배 RevPAR", "높음", "#95A5A6"),
  ]
  rows = ""
  for medal, rank, action, evidence, effect, difficulty, color in actions:
    medal_display = medal if medal else rank
    rows += f"""
    <div style="display: flex; align-items: center; padding: 14px 0; border-bottom: 1px solid var(--gray-200); gap: 16px;">
      <div style="width: 40px; text-align: center; font-size: 20px;">{medal_display}</div>
      <div style="flex: 1.2; font-size: 16px; font-weight: 700; color: {color};">{action}</div>
      <div style="flex: 1; font-size: 14px; color: var(--gray-500);">{evidence}</div>
      <div style="flex: 0.8; font-size: 14px; font-weight: 600;">{effect}</div>
      <div style="width: 60px; text-align: center;"><span style="font-size: 13px; padding: 4px 10px; border-radius: 6px; background: var(--gray-100);">{difficulty}</span></div>
    </div>"""
  return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
  .wrap {{ padding: 70px 100px; height: 100%; display: flex; flex-direction: column; }}
  .bottom-msg {{ margin-top: 28px; padding: 20px 32px; background: var(--coral); color: white; border-radius: 6px; text-align: center; font-size: 18px; font-weight: 600; }}
  </style></head><body>
  <div class="slide slide-light">
    <div class="wrap">
      <div class="breadcrumb">종합</div>
      <div class="slide-title">호스트 액션 가이드 — 종합 실행 로드맵</div>
      <div class="title-underline"></div>
      <div class="card" style="padding: 20px 28px; flex: 1;">
        <div style="display: flex; padding: 10px 0; border-bottom: 2px solid var(--gray-300); gap: 16px;">
          <div style="width: 40px; font-size: 13px; font-weight: 600; color: var(--gray-500); text-align: center;">#</div>
          <div style="flex: 1.2; font-size: 13px; font-weight: 600; color: var(--gray-500);">액션</div>
          <div style="flex: 1; font-size: 13px; font-weight: 600; color: var(--gray-500);">근거</div>
          <div style="flex: 0.8; font-size: 13px; font-weight: 600; color: var(--gray-500);">기대 효과</div>
          <div style="width: 60px; font-size: 13px; font-weight: 600; color: var(--gray-500); text-align: center;">난이도</div>
        </div>
        {rows}
      </div>
      <div class="bottom-msg">분석 → 모델 → 대시보드 → 자동화 → 액션. 데이터로 호스트의 수익을 설계하다.</div>
    </div>
    <div class="page-num">{page}</div>
  </div></body></html>"""
