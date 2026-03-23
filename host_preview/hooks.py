"""
host_preview/hooks.py
======================
PostToolUse 훅 진입점 — 호스트 프리뷰 이메일 파이프라인 통합.

Claude Code가 final_seoul_airbnb_cleaned.csv 또는
district_clustered.csv를 수정할 때 자동 호출됩니다.

사용법
------
  # 훅 자동 트리거 (Claude Code 내부 호출)
  python3 hooks.py --trigger postToolUse --file path/to/file.csv

  # 수동 트리거 (테스트용)
  python3 hooks.py --trigger manual
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# 패키지 루트를 sys.path에 추가 (직접 실행 시 필요)
_PKG_ROOT = Path(__file__).parent.parent
if str(_PKG_ROOT) not in sys.path:
  sys.path.insert(0, str(_PKG_ROOT))

from host_preview.analyzer import build_preview_report
from host_preview.email_builder import send_demo_emails
from host_preview.config import REPORT_PATH, PREVIEW_DIR, DUPLICATE_HISTORY_PATH
from risk_detection.duplicate_tracker import DuplicateTracker


# ── 트리거 조건 ──────────────────────────────────────
_TRIGGER_KEYWORDS = [
  'final_seoul_airbnb_cleaned.csv',
  'district_clustered.csv',
]


def should_trigger(file_path: str) -> bool:
  """
  변경 파일이 호스트 프리뷰 트리거 대상인지 판별.

  Parameters
  ----------
  file_path : Write/Edit 훅에서 전달된 파일 경로

  Returns
  -------
  bool
  """
  if not file_path:
    return False
  return any(kw in file_path for kw in _TRIGGER_KEYWORDS)


def run_preview_scan(csv_path=None) -> dict:
  """
  호스트 프리뷰 전체 파이프라인 실행.

  1. AO 서브셋 분석 (Z-score / 추세 / STL)
  2. 데모 3건 선택
  3. HTML 저장 + 이메일 발송

  Parameters
  ----------
  csv_path : 사용하지 않음 (config.DATA_PATH 고정), 인터페이스 통일용

  Returns
  -------
  dict : scan_meta
  """
  ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  print(f'[{ts}] 호스트 프리뷰 스캔 시작...')

  try:
    full_df, demo_df, meta = build_preview_report()
  except Exception as e:
    print(f'[오류] 파이프라인 실행 실패: {e}')
    import traceback
    traceback.print_exc()
    return {}

  # ── 결과 요약 출력 ───────────────────────────────
  print(f'  → 총 분석 (AO): {meta["total_ao"]:,}건')
  print(f'  → CRITICAL: {meta["critical_count"]}건 / '
        f'WARNING: {meta["warning_count"]}건 / '
        f'OK: {meta["ok_count"]}건')

  # ── 중복 필터: 7일 이내 동일 상태 스킵 ─────────────
  tracker = DuplicateTracker(history_path=DUPLICATE_HISTORY_PATH)
  tracker.purge_old(days=30)

  # full_df 중 CRITICAL/WARNING 리스팅에 대해 중복 판별
  # analyzer.py는 'anomaly_level' 컬럼을 생성 (기존 'status'는 존재하지 않음)
  _level_col = 'anomaly_level' if 'anomaly_level' in full_df.columns else None
  if _level_col:
    flagged = full_df[full_df[_level_col].isin(['CRITICAL', 'WARNING'])].copy()
  else:
    flagged = full_df.copy()
  if not flagged.empty and 'listing_idx' in flagged.columns:
    if _level_col:
      flagged['rules_triggered'] = flagged[_level_col].astype(str)
    new_flagged, skipped = tracker.filter_new(flagged, cooldown_days=7)
    if skipped > 0:
      print(f'  → 중복 스킵: {skipped}건 (7일 내 동일 상태)')
    if not new_flagged.empty:
      tracker.record_batch(new_flagged)

  # ── 데모 이메일 생성·발송 ────────────────────────
  email_result = send_demo_emails(demo_df, full_df)

  # ── JSON 리포트 저장 ─────────────────────────────
  PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
  REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

  def _safe(v):
    """JSON 직렬화 안전 변환"""
    import numpy as np, math
    if isinstance(v, bool):
      return v
    if isinstance(v, float) and math.isnan(v):
      return None
    if hasattr(v, 'item'):
      return v.item()
    return v

  demo_records = [
    {k: _safe(val) for k, val in row.items()}
    for _, row in demo_df.iterrows()
  ]

  report = {
    'scan_meta': meta,
    'demo_listings': demo_records,
    'email_result': email_result,
  }

  with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2, default=str)

  print(f'  → JSON 저장: {REPORT_PATH}')

  if email_result['saved']:
    print(f'  → HTML 저장: {", ".join(email_result["saved"])}')
  if email_result['errors']:
    for err in email_result['errors']:
      print(f'  [오류] {err}')

  return meta


def _parse_args():
  parser = argparse.ArgumentParser(description='호스트 프리뷰 이메일 훅')
  parser.add_argument('--trigger', default='manual',
                      help='트리거 유형 (postToolUse | manual)')
  parser.add_argument('--file', default='',
                      help='변경된 파일 경로 (postToolUse 시 전달)')
  return parser.parse_args()


if __name__ == '__main__':
  args = _parse_args()

  if args.trigger == 'postToolUse':
    if should_trigger(args.file):
      print(f'[훅] 관련 파일 변경 감지: {args.file}')
      run_preview_scan()
    else:
      sys.exit(0)
  else:
    print('[수동 트리거] 호스트 프리뷰 스캔 실행 중...')
    run_preview_scan()
