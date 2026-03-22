"""
host_preview/email_builder.py
==============================
호스트 향 진단 이메일 빌더 + 발송.

- 통계 용어 사용 금지 → 비전문가 친화적 일상 언어
- 에어비앤비 브랜드 색상 (#FF385C, #00A699, #F7F7F7 등)
- 사분면 차트를 base64 PNG로 인라인 삽입
- 데모 모드: HTML 저장 (항상) + SMTP 발송 (비밀번호 있을 때)
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pandas as pd

from .config import EMAIL_CONFIG, COLORS, PREVIEW_DIR
from .analyzer import generate_quadrant_chart


# ── 유틸 ──────────────────────────────────────────────
def _won(value) -> str:
  """원화 포맷 (예: ₩47,850)"""
  try:
    return f'₩{int(value):,}'
  except (ValueError, TypeError):
    return 'N/A'


def _pct(value, decimals: int = 1) -> str:
  """소수 → 퍼센트 문자열"""
  try:
    return f'{float(value) * 100:.{decimals}f}%'
  except (ValueError, TypeError):
    return 'N/A'


def _level_badge(level: str) -> str:
  """레벨 배지 HTML"""
  badges = {
    'CRITICAL': (COLORS['primary'],  '🚨 즉시 점검이 필요해요'),
    'WARNING':  (COLORS['warning'],  '💡 개선할 여지가 있어요'),
    'OK':       (COLORS['teal'],     '✅ 현재 양호하게 운영 중이에요'),
  }
  color, text = badges.get(level, (COLORS['subtitle'], level))
  return (
    f'<span style="background:{color};color:white;padding:4px 12px;'
    f'border-radius:20px;font-size:13px;font-weight:bold">{text}</span>'
  )


def _quadrant_label(adr_pct: float, occ_pct: float) -> tuple[str, str]:
  """사분면 위치 레이블 (텍스트, 색상)"""
  if adr_pct >= 50 and occ_pct >= 50:
    return '고수익형 — 요금과 예약률 모두 상위권이에요', COLORS['teal']
  if adr_pct >= 50 and occ_pct < 50:
    return '고가위험형 — 요금은 높지만 예약이 적어요', '#E65100'
  if adr_pct < 50 and occ_pct >= 50:
    return '물량형 — 예약은 많지만 요금이 낮은 편이에요', '#B45309'
  return '침체형 — 요금과 예약률 모두 낮은 편이에요', '#B71C1C'


# ── 섹션 빌더 ─────────────────────────────────────────

def _section_header(listing_row: pd.Series) -> str:
  district_ko = listing_row.get('district_ko', listing_row.get('district', '서울'))
  room_type   = listing_row.get('room_type', '숙소')
  return f'''
<div style="background:{COLORS['primary']};color:white;padding:28px 28px 20px;
            border-radius:12px 12px 0 0">
  <p style="margin:0 0 4px;font-size:13px;opacity:0.85">📍 {district_ko} · {room_type}</p>
  <h1 style="margin:0;font-size:22px;font-weight:800;line-height:1.3">
    내 숙소, 서울에서<br>어디쯤 있을까요?
  </h1>
  <p style="margin:12px 0 0;font-size:13px;opacity:0.9">
    지금 바로 수익 진단 결과를 확인해 보세요.
  </p>
</div>'''


def _section_market_cards(listing_row: pd.Series) -> str:
  seoul_pct  = listing_row.get('revpar_percentile_seoul', 50.0)
  rank       = listing_row.get('revpar_rank_district', '?')
  total      = listing_row.get('district_listing_count', '?')
  cluster_nm = listing_row.get('cluster_name', '미분류')
  district_ko = listing_row.get('district_ko', '')

  # 서울 전체 상위 %
  top_pct = round(100 - seoul_pct, 1)

  cards = [
    ('🏙️', '서울 전체에서', f'상위 <b>{top_pct}%</b>', f'{seoul_pct:.0f}번째 백분위'),
    ('📍', f'{district_ko} 안에서', f'<b>{rank}번째</b> 수익', f'총 {total}개 숙소 중'),
    ('🏷️', '시장 유형', f'<b>{cluster_nm}</b>', '에어비앤비 분류 기준'),
  ]

  card_html = ''
  for icon, title, main, sub in cards:
    card_html += f'''
    <div style="flex:1;min-width:140px;background:{COLORS['card']};border:1px solid {COLORS['border']};
                border-radius:10px;padding:16px 14px;text-align:center">
      <div style="font-size:22px;margin-bottom:6px">{icon}</div>
      <div style="font-size:11px;color:{COLORS['subtitle']};margin-bottom:4px">{title}</div>
      <div style="font-size:16px;color:{COLORS['body']};margin-bottom:2px">{main}</div>
      <div style="font-size:11px;color:{COLORS['subtitle']}">{sub}</div>
    </div>'''

  return f'''
<div style="padding:20px 24px;background:{COLORS['bg']};border-bottom:1px solid {COLORS['border']}">
  <h3 style="margin:0 0 14px;color:{COLORS['body']};font-size:14px">내 숙소 시장 위치</h3>
  <div style="display:flex;gap:12px;flex-wrap:wrap">
    {card_html}
  </div>
</div>'''


def _section_diagnosis(listing_row: pd.Series) -> str:
  level          = listing_row.get('anomaly_level', 'OK')
  zscore_anom    = listing_row.get('zscore_anomaly', False)
  trend_anom     = listing_row.get('trend_anomaly', False)
  stl_anom       = listing_row.get('stl_anomaly', False)
  trend_ratio    = listing_row.get('trend_ratio', 0.0)
  district_ko    = listing_row.get('district_ko', '구')

  def _row(ok: bool, label: str, ok_msg: str, warn_msg: str) -> str:
    icon  = '✅' if not ok else '⚠️'
    color = COLORS['teal'] if not ok else COLORS['warning']
    msg   = warn_msg if ok else ok_msg
    return f'''
    <tr>
      <td style="padding:10px 12px;font-size:13px;color:{COLORS['body']}">{label}</td>
      <td style="padding:10px 12px;font-size:13px;color:{color};font-weight:500">{icon} {msg}</td>
    </tr>'''

  trend_pct = abs(round(trend_ratio * 100, 1))
  trend_direction = '하락' if trend_ratio < 0 else '상승'

  rows = (
    _row(
      zscore_anom, '구 대비 수익 수준',
      '같은 구 숙소들과 비슷하거나 높은 수익이에요',
      f'{district_ko} 평균보다 수익이 크게 낮은 편이에요'
    )
    + _row(
      trend_anom, '최근 3개월 추이',
      '연간 평균과 비교해 최근 3개월이 안정적이에요',
      f'최근 3개월 수익이 연간 평균보다 {trend_pct}% {trend_direction}했어요'
    )
    + _row(
      stl_anom, '숙소 유형·위치 대비',
      '같은 유형·위치 숙소들과 비교해 수익이 양호해요',
      '숙소 유형과 위치를 고려해도 수익이 낮은 편이에요'
    )
  )

  return f'''
<div style="padding:20px 24px;border-bottom:1px solid {COLORS['border']}">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">
    <h3 style="margin:0;color:{COLORS['body']};font-size:14px">수익 진단 결과</h3>
    {_level_badge(level)}
  </div>
  <table style="width:100%;border-collapse:collapse;background:{COLORS['card']};
                border:1px solid {COLORS['border']};border-radius:8px;overflow:hidden">
    <thead>
      <tr style="background:{COLORS['bg']}">
        <th style="padding:10px 12px;text-align:left;font-size:12px;color:{COLORS['subtitle']};
                   font-weight:600;width:40%">진단 항목</th>
        <th style="padding:10px 12px;text-align:left;font-size:12px;color:{COLORS['subtitle']};
                   font-weight:600">결과</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</div>'''


def _section_quadrant_chart(listing_row: pd.Series, full_df: pd.DataFrame) -> str:
  base64_chart = generate_quadrant_chart(full_df, listing_row)

  if not base64_chart:
    return ''

  return f'''
<div style="padding:20px 24px;background:{COLORS['bg']};border-bottom:1px solid {COLORS['border']}">
  <h3 style="color:{COLORS['body']};font-size:14px;margin:0 0 8px">
    📊 내 숙소의 경쟁력 지도 (맛보기)
  </h3>
  <p style="font-size:12px;color:{COLORS['subtitle']};margin:0 0 12px">
    같은 유형의 숙소들과 비교했을 때, 내 숙소가 어느 사분면에 속하는지 확인하세요.
  </p>
  <img src="{base64_chart}"
       style="width:100%;max-width:480px;border-radius:8px;border:1px solid {COLORS['border']}"
       alt="내 숙소 경쟁력 포지셔닝">
  <p style="font-size:11px;color:{COLORS['subtitle']};margin:8px 0 0">
    ※ 전체 대시보드에서는 실시간으로 조건을 바꿔가며 확인할 수 있습니다
  </p>
</div>'''


def _section_blur_teaser() -> str:
  items = [
    ('💰', '내 가격을 X% 올리면 수익이 어떻게 바뀔까요?'),
    ('⭐', '슈퍼호스트가 되면 수익이 얼마나 늘어날까요?'),
    ('📸', '사진을 몇 장까지 올려야 가장 효과적일까요?'),
    ('🌙', '최소 숙박일을 몇 박으로 설정해야 할까요?'),
  ]
  rows = ''
  for icon, text in items:
    rows += f'''
    <div style="display:flex;align-items:center;gap:10px;padding:10px 0;
                border-bottom:1px solid {COLORS['border']}">
      <span style="font-size:18px">{icon}</span>
      <span style="font-size:13px;color:{COLORS['body']};
                   filter:blur(4px);user-select:none">{text}</span>
      <span style="margin-left:auto;font-size:11px;color:{COLORS['primary']};
                   white-space:nowrap">🔒 잠김</span>
    </div>'''

  return f'''
<div style="padding:20px 24px;border-bottom:1px solid {COLORS['border']}">
  <h3 style="color:{COLORS['body']};font-size:14px;margin:0 0 4px">
    🔓 전체 대시보드에서 확인할 수 있어요
  </h3>
  <p style="font-size:12px;color:{COLORS['subtitle']};margin:0 0 14px">
    아래 항목들은 대시보드에서 개인 맞춤형으로 제공됩니다.
  </p>
  {rows}
</div>'''


def _section_cta() -> str:
  return f'''
<div style="padding:24px;text-align:center;background:{COLORS['card']};border-radius:0 0 12px 12px">
  <a href="#"
     style="display:inline-block;background:{COLORS['primary']};color:white;
            padding:14px 36px;border-radius:30px;text-decoration:none;
            font-size:15px;font-weight:bold;letter-spacing:0.3px">
    지금 무료로 전체 분석 보기 →
  </a>
  <p style="margin:14px 0 0;font-size:11px;color:{COLORS['subtitle']}">
    이 이메일은 서울 에어비앤비 RevPAR 분석 시스템이 자동 생성했습니다.
  </p>
</div>'''


# ── 메인 빌더 ─────────────────────────────────────────

def build_host_email(listing_row: pd.Series, full_df: pd.DataFrame) -> str:
  """
  단일 리스팅에 대한 호스트 진단 HTML 이메일 생성.

  Parameters
  ----------
  listing_row : 분석된 리스팅 1행 (Series)
  full_df     : 사분면 차트용 전체 AO DataFrame

  Returns
  -------
  str : 완성된 HTML 문자열
  """
  body = (
    _section_header(listing_row)
    + _section_market_cards(listing_row)
    + _section_diagnosis(listing_row)
    + _section_quadrant_chart(listing_row, full_df)
    + _section_blur_teaser()
    + _section_cta()
  )

  return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>내 숙소 수익 진단</title>
</head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;
             margin:0;padding:20px;background:{COLORS['bg']}">
  <div style="max-width:600px;margin:0 auto;background:{COLORS['card']};
              border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,0.08)">
    {body}
  </div>
</body>
</html>'''


def send_demo_emails(demo_df: pd.DataFrame, full_df: pd.DataFrame) -> dict:
  """
  데모 3건 이메일 처리:
    1. HTML 파일로 저장 (항상 실행 — 폴백)
    2. SMTP 발송 (비밀번호 있을 때)

  Parameters
  ----------
  demo_df  : select_demo_listings() 결과 (최대 3행)
  full_df  : 사분면 차트용 전체 AO DataFrame

  Returns
  -------
  dict : {'saved': [...], 'sent': [...], 'errors': [...]}
  """
  PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

  result = {'saved': [], 'sent': [], 'errors': []}
  password = EMAIL_CONFIG.get('password', '')

  for _, row in demo_df.iterrows():
    level = row.get('anomaly_level', 'OK')
    html  = build_host_email(row, full_df)

    # ── 1. HTML 저장 (항상) ─────────────────────────
    save_path = PREVIEW_DIR / f'{level}.html'
    try:
      save_path.write_text(html, encoding='utf-8')
      result['saved'].append(str(save_path))
      print(f'  → HTML 저장: {save_path}')
    except Exception as e:
      result['errors'].append(f'저장 실패 ({level}): {e}')

    # ── 2. 이메일 발송 (비밀번호 있을 때) ──────────
    if not password:
      continue

    msg = MIMEMultipart('alternative')
    district_ko = row.get('district_ko', row.get('district', ''))
    msg['Subject'] = (
      f"{EMAIL_CONFIG['subject_prefix']} "
      f"{district_ko} 숙소 — {level} 진단"
    )
    msg['From'] = EMAIL_CONFIG['sender']
    msg['To']   = ', '.join(EMAIL_CONFIG['recipients'])
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    try:
      with smtplib.SMTP(EMAIL_CONFIG['smtp_host'], EMAIL_CONFIG['smtp_port']) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_CONFIG['sender'], password)
        server.sendmail(
          EMAIL_CONFIG['sender'],
          EMAIL_CONFIG['recipients'],
          msg.as_string()
        )
      result['sent'].append(level)
      print(f'  → 이메일 발송: {level} → {EMAIL_CONFIG["recipients"]}')
    except Exception as e:
      result['errors'].append(f'발송 실패 ({level}): {e}')
      print(f'  [오류] 이메일 발송 실패 ({level}): {e}')

  return result
