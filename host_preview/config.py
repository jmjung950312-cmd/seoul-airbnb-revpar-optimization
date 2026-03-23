"""
host_preview/config.py
=======================
단일 진실 원천 — 호스트 프리뷰 이메일 훅의 모든 설정을 관리합니다.
risk_detection/config.py의 SMTP·구(區) 매핑을 재사용합니다.
"""

import os
import pathlib

# ──────────────────────────────────────────────
# 이상 신호 탐지 임계값
# ──────────────────────────────────────────────
THRESHOLDS = {
  # Z-score 이상: 구 평균 대비 log RevPAR 편차
  'zscore_threshold': -2.0,

  # 추세 이탈 (Prophet 근사): L90D RevPAR vs TTM/4 비율
  'trend_threshold': -0.20,

  # STL 잔차 이상 (STL 근사): 잔차 Z-score
  'stl_residual_threshold': -2.0,

  # 레벨 기준
  'critical_min_count': 3,   # 3개 신호 → CRITICAL
  'warning_min_count': 1,    # 1~2개 신호 → WARNING
}

# ──────────────────────────────────────────────
# 이메일 설정 (risk_detection과 동일 SMTP)
# ──────────────────────────────────────────────
EMAIL_CONFIG = {
  'smtp_host': 'smtp.gmail.com',
  'smtp_port': 587,
  'sender': 'jmjung950312@gmail.com',
  'password': os.environ.get('RISK_EMAIL_PASSWORD', ''),
  'recipients': [
    'jmjung950312@gmail.com',
  ],
  'subject_prefix': '[내 숙소 수익 진단]',
}

# ──────────────────────────────────────────────
# 에어비앤비 브랜드 색상
# ──────────────────────────────────────────────
COLORS = {
  'primary':    '#FF385C',   # Rausch — 헤더, CTA
  'teal':       '#00A699',   # Babu — 좋음 배지
  'bg':         '#F7F7F7',   # 섹션 배경
  'card':       '#FFFFFF',   # 카드 흰색
  'body':       '#484848',   # 본문 텍스트
  'subtitle':   '#767676',   # 부제목
  'border':     '#EBEBEB',   # 테두리
  'warning':    '#FC642D',   # 경고 주황
  'q_vol':      '#FFF3E0',   # 사분면 물량형 (좌상)
  'q_profit':   '#E8F5E9',   # 사분면 고수익형 (우상)
  'q_stagnant': '#FFEBEE',   # 사분면 침체형 (좌하)
  'q_risk':     '#FFF8E1',   # 사분면 고가위험형 (우하)
}

# ──────────────────────────────────────────────
# 파일 경로
# ──────────────────────────────────────────────
_BASE = pathlib.Path(__file__).parent.parent  # 프로젝트 루트

DATA_PATH = _BASE / 'data' / 'raw' / 'final_seoul_airbnb_cleaned.csv'
CLUSTER_PATH = _BASE / 'data' / 'processed' / 'district_clustered.csv'
PREVIEW_DIR = _BASE / 'reports' / 'host_preview'
REPORT_PATH = _BASE / 'reports' / 'host_preview_demo.json'

# 중복 감지 방지 — 히스토리 파일 경로
DUPLICATE_HISTORY_PATH = _BASE / 'logs' / 'host_preview_history.json'

# ──────────────────────────────────────────────
# 25개 자치구 영문→한글 매핑 (shared/constants.py 단일 소스)
# ──────────────────────────────────────────────
import sys as _sys
_sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from shared.constants import DISTRICT_KO  # noqa: E402
