"""
host_preview/analyzer.py
=========================
호스트 프리뷰 분석 파이프라인:
  1. 데이터 로드 + Active+Operating 필터 + 자치구 군집 조인
  2. 3개 이상 신호 탐지 (Z-score / 추세 이탈 / STL 잔차)
  3. 시장 위치 계산 (서울 전체 백분위 / 구 내 순위)
  4. 이상 레벨 부여 (CRITICAL / WARNING / OK)
  5. 데모 3건 선택
  6. 사분면 포지셔닝 차트 생성 → base64 PNG 반환
"""

import io
import base64
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # GUI 없는 환경에서도 렌더링 가능
import matplotlib.pyplot as plt

from .config import (
  DATA_PATH, CLUSTER_PATH, DISTRICT_KO, THRESHOLDS, COLORS
)


# ────────────────────────────────────────────────────
# 1. 데이터 로드 + 준비
# ────────────────────────────────────────────────────
def load_and_prepare() -> pd.DataFrame:
  """
  CSV 로드 → AO 서브셋 필터 → listing_idx / district_ko / cluster 컬럼 추가

  Returns
  -------
  pd.DataFrame : Active+Operating 14,399건 기준 DataFrame
  """
  df = pd.read_csv(DATA_PATH)

  # 대리 ID 생성 (원본에 listing_id 없음)
  df = df.reset_index(drop=False).rename(columns={'index': 'listing_idx'})

  # Active + Operating 서브셋만 사용 (Dormant 포함 시 Z-score 왜곡)
  mask = (df['refined_status'] == 'Active') & (df['operation_status'] == 'Operating')
  df = df[mask].copy()

  # 한글 자치구명 추가
  df['district_ko'] = df['district'].map(DISTRICT_KO).fillna(df['district'])

  # 군집 정보 조인 (district_clustered.csv)
  cluster_df = pd.read_csv(CLUSTER_PATH)[['district', 'cluster', 'cluster_name']]
  df = df.merge(cluster_df, on='district', how='left')
  df['cluster'] = df['cluster'].fillna(-1).astype(int)
  df['cluster_name'] = df['cluster_name'].fillna('미분류')

  return df.reset_index(drop=True)


# ────────────────────────────────────────────────────
# 2. Z-score 이상 탐지
# ────────────────────────────────────────────────────
def compute_zscore_anomaly(df: pd.DataFrame) -> pd.DataFrame:
  """
  구(區) 내 log RevPAR Z-score 계산.

  추가 컬럼: log_ttm_revpar, revpar_zscore, zscore_anomaly
  """
  df = df.copy()
  df['log_ttm_revpar'] = np.log1p(df['ttm_revpar'].fillna(0))

  grp = df.groupby('district')['log_ttm_revpar']
  df['_dist_mean'] = grp.transform('mean')
  df['_dist_std']  = grp.transform('std').replace(0, 1e-6)

  df['revpar_zscore'] = (df['log_ttm_revpar'] - df['_dist_mean']) / df['_dist_std']
  df['zscore_anomaly'] = df['revpar_zscore'] < THRESHOLDS['zscore_threshold']

  return df.drop(columns=['_dist_mean', '_dist_std'])


# ────────────────────────────────────────────────────
# 3. 추세 이탈 탐지 (Prophet 근사)
# ────────────────────────────────────────────────────
def compute_trend_anomaly(df: pd.DataFrame) -> pd.DataFrame:
  """
  L90D RevPAR vs TTM RevPAR/4 비율로 최근 3개월 하락 감지.

  추가 컬럼: ttm_revpar_quarterly, trend_ratio, trend_anomaly
  """
  df = df.copy()
  df['ttm_revpar_quarterly'] = df['ttm_revpar'] / 4
  df['trend_ratio'] = (
    (df['l90d_revpar'] - df['ttm_revpar_quarterly'])
    / (df['ttm_revpar_quarterly'] + 1e-6)
  )
  df['trend_anomaly'] = df['trend_ratio'] < THRESHOLDS['trend_threshold']
  return df


# ────────────────────────────────────────────────────
# 4. STL 잔차 이상 탐지 (STL 근사)
# ────────────────────────────────────────────────────
def compute_stl_residual(df: pd.DataFrame) -> pd.DataFrame:
  """
  교차 단면 STL 근사:
    Trend    = groupby(district) log RevPAR 평균
    Seasonal = groupby(room_type) log RevPAR 평균 - 전체 평균
    Residual = log RevPAR - Trend - Seasonal

  추가 컬럼: stl_district_trend, stl_room_seasonal, stl_residual,
             stl_residual_z, stl_anomaly
  """
  df = df.copy()

  # log RevPAR가 없으면 생성
  if 'log_ttm_revpar' not in df.columns:
    df['log_ttm_revpar'] = np.log1p(df['ttm_revpar'].fillna(0))

  global_mean = df['log_ttm_revpar'].mean()

  df['stl_district_trend'] = (
    df.groupby('district')['log_ttm_revpar'].transform('mean')
  )
  df['stl_room_seasonal'] = (
    df.groupby('room_type')['log_ttm_revpar'].transform('mean') - global_mean
  )
  df['stl_residual'] = (
    df['log_ttm_revpar'] - df['stl_district_trend'] - df['stl_room_seasonal']
  )

  resid_std = df['stl_residual'].std()
  resid_std = resid_std if resid_std > 1e-6 else 1e-6
  df['stl_residual_z'] = df['stl_residual'] / resid_std
  df['stl_anomaly'] = df['stl_residual_z'] < THRESHOLDS['stl_residual_threshold']

  return df


# ────────────────────────────────────────────────────
# 5. 시장 위치 계산
# ────────────────────────────────────────────────────
def compute_market_position(df: pd.DataFrame) -> pd.DataFrame:
  """
  서울 전체 백분위 + 구 내 순위 계산.

  추가 컬럼: revpar_percentile_seoul, revpar_rank_district,
             district_listing_count
  """
  df = df.copy()

  # 서울 전체 백분위 (높을수록 상위)
  revpar_vals = df['ttm_revpar'].fillna(0).values
  df['revpar_percentile_seoul'] = df['ttm_revpar'].fillna(0).apply(
    lambda x: float(np.mean(revpar_vals <= x) * 100)
  ).round(1)

  # 구 내 순위 (낮을수록 상위, 1위가 최고)
  df['revpar_rank_district'] = (
    df.groupby('district')['ttm_revpar']
    .rank(method='min', ascending=False)
    .astype(int)
  )
  df['district_listing_count'] = (
    df.groupby('district')['ttm_revpar'].transform('count').astype(int)
  )

  return df


# ────────────────────────────────────────────────────
# 6. 이상 레벨 부여
# ────────────────────────────────────────────────────
def score_listing(df: pd.DataFrame) -> pd.DataFrame:
  """
  3개 이상 신호를 합산해 CRITICAL / WARNING / OK 레벨 부여.

  추가 컬럼: anomaly_count, anomaly_flags, anomaly_level
  """
  df = df.copy()

  anomaly_cols = {
    'zscore_anomaly':  'Z-score',
    'trend_anomaly':   '추세이탈',
    'stl_anomaly':     'STL잔차',
  }

  def _count_flags(row):
    flags = [label for col, label in anomaly_cols.items() if row.get(col, False)]
    return len(flags), '+'.join(flags) if flags else 'none'

  results = df.apply(_count_flags, axis=1)
  df['anomaly_count'] = results.apply(lambda x: x[0])
  df['anomaly_flags'] = results.apply(lambda x: x[1])

  def _level(count):
    if count >= THRESHOLDS['critical_min_count']:
      return 'CRITICAL'
    if count >= THRESHOLDS['warning_min_count']:
      return 'WARNING'
    return 'OK'

  df['anomaly_level'] = df['anomaly_count'].apply(_level)
  return df


# ────────────────────────────────────────────────────
# 7. 데모 3건 선택
# ────────────────────────────────────────────────────
def select_demo_listings(df: pd.DataFrame, n: int = 1) -> pd.DataFrame:
  """
  CRITICAL 1건 + WARNING 1건 + OK 1건 선택 (데모용).

  Parameters
  ----------
  df : score_listing() 결과 DataFrame
  n  : 각 레벨당 선택 건수 (기본 1)

  Returns
  -------
  pd.DataFrame : 최대 3n건 (레벨이 없으면 해당 레벨 스킵)
  """
  parts = []
  for level in ['CRITICAL', 'WARNING', 'OK']:
    subset = df[df['anomaly_level'] == level]
    if len(subset) == 0:
      continue
    if level == 'CRITICAL':
      # CRITICAL: RevPAR 낮은 순
      parts.append(subset.nsmallest(n, 'ttm_revpar'))
    elif level == 'WARNING':
      # WARNING: 추세 하락이 가장 큰 순
      parts.append(subset.nsmallest(n, 'trend_ratio'))
    else:
      # OK: RevPAR 높은 순 (긍정 사례)
      parts.append(subset.nlargest(n, 'ttm_revpar'))

  return pd.concat(parts, ignore_index=True)


# ────────────────────────────────────────────────────
# 8. 사분면 포지셔닝 차트 → base64 PNG
# ────────────────────────────────────────────────────
def generate_quadrant_chart(df: pd.DataFrame, listing_row: pd.Series) -> str:
  """
  해당 리스팅의 클러스터 내 ADR / 예약률 사분면 포지셔닝 차트 생성.

  Parameters
  ----------
  df          : 전체 AO DataFrame (클러스터 동료 필터링용)
  listing_row : 대상 리스팅 1행 (Series)

  Returns
  -------
  str : base64 인코딩된 PNG 문자열 (data:image/png;base64,... 형식)
  """
  plt.rcParams['font.family'] = 'AppleGothic'
  plt.rcParams['axes.unicode_minus'] = False

  cluster_id = listing_row.get('cluster', -1)
  cluster_name = listing_row.get('cluster_name', '시장 유형')

  # 같은 클러스터 동료 추출
  peers = df[df['cluster'] == cluster_id].copy()
  if len(peers) < 5:
    peers = df.copy()  # 동료 너무 적으면 전체 사용

  adr_vals = peers['ttm_avg_rate'].dropna()
  occ_vals = peers['ttm_occupancy'].dropna()

  if len(adr_vals) < 5 or len(occ_vals) < 5:
    # 데이터 부족 시 빈 이미지 반환
    return ''

  # 동료 백분위
  peers = peers.copy()
  peers['adr_pct'] = peers['ttm_avg_rate'].apply(
    lambda x: float(np.mean(adr_vals <= x) * 100) if not pd.isna(x) else 50.0
  )
  peers['occ_pct'] = peers['ttm_occupancy'].apply(
    lambda x: float(np.mean(occ_vals <= x) * 100) if not pd.isna(x) else 50.0
  )

  # 해당 리스팅 백분위
  my_adr = listing_row.get('ttm_avg_rate', np.nan)
  my_occ = listing_row.get('ttm_occupancy', np.nan)
  user_adr_pct = float(np.mean(adr_vals <= my_adr) * 100) if not pd.isna(my_adr) else 50.0
  user_occ_pct = float(np.mean(occ_vals <= my_occ) * 100) if not pd.isna(my_occ) else 50.0

  # ── 차트 렌더링 ──────────────────────────────────
  fig, ax = plt.subplots(figsize=(5, 5), dpi=100)

  # 사분면 배경 (에어비앤비 컬러 계열)
  ax.axhspan(50, 100, xmin=0,   xmax=0.5, alpha=1.0, color=COLORS['q_vol'],      zorder=0)
  ax.axhspan(50, 100, xmin=0.5, xmax=1.0, alpha=1.0, color=COLORS['q_profit'],   zorder=0)
  ax.axhspan(0,  50,  xmin=0,   xmax=0.5, alpha=1.0, color=COLORS['q_stagnant'], zorder=0)
  ax.axhspan(0,  50,  xmin=0.5, xmax=1.0, alpha=1.0, color=COLORS['q_risk'],     zorder=0)

  # 중앙선
  ax.axhline(50, color='#CCCCCC', lw=1, ls='--', zorder=1)
  ax.axvline(50, color='#CCCCCC', lw=1, ls='--', zorder=1)

  # 사분면 레이블
  ax.text(25, 78, '물량형',     ha='center', va='center', fontsize=9, color='#B45309', alpha=0.8)
  ax.text(75, 78, '고수익형',   ha='center', va='center', fontsize=9, color='#1B5E20', alpha=0.8)
  ax.text(25, 22, '침체형',     ha='center', va='center', fontsize=9, color='#B71C1C', alpha=0.8)
  ax.text(75, 22, '고가위험형', ha='center', va='center', fontsize=9, color='#E65100', alpha=0.8)

  # 동료 산점도 (회색 점)
  ax.scatter(
    peers['adr_pct'].dropna(),
    peers['occ_pct'].dropna(),
    s=15, alpha=0.18, color='#9CA3AF', zorder=2,
  )

  # 해당 리스팅 (에어비앤비 레드 별 마커)
  ax.scatter(
    [user_adr_pct], [user_occ_pct],
    s=250, marker='*', color=COLORS['primary'], zorder=5, label='이 숙소',
  )
  ax.annotate(
    '이 숙소',
    (user_adr_pct, user_occ_pct),
    textcoords='offset points', xytext=(8, 6),
    fontsize=9, color=COLORS['primary'], fontweight='bold',
  )

  ax.set_xlim(0, 100)
  ax.set_ylim(0, 100)
  ax.set_xlabel('요금 분위 (클러스터 내, %)', fontsize=9)
  ax.set_ylabel('예약률 분위 (클러스터 내, %)', fontsize=9)
  ax.set_title(f'{cluster_name} 포지셔닝', fontsize=10, fontweight='bold')
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.set_facecolor('#FAFAFA')
  fig.patch.set_facecolor('#FAFAFA')
  fig.tight_layout()

  # base64 인코딩
  buf = io.BytesIO()
  fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
  plt.close(fig)
  buf.seek(0)
  encoded = base64.b64encode(buf.read()).decode('utf-8')
  return f'data:image/png;base64,{encoded}'


# ────────────────────────────────────────────────────
# 9. 전체 파이프라인 오케스트레이터
# ────────────────────────────────────────────────────
def build_preview_report() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
  """
  분석 파이프라인 전체 실행.

  Returns
  -------
  tuple :
    full_df  : AO 서브셋 전체 DataFrame (점수 포함)
    demo_df  : CRITICAL 1건 + WARNING 1건 + OK 1건
    meta     : 스캔 메타 딕셔너리
  """
  df = load_and_prepare()
  df = compute_zscore_anomaly(df)
  df = compute_trend_anomaly(df)
  df = compute_stl_residual(df)
  df = compute_market_position(df)
  df = score_listing(df)

  level_counts = df['anomaly_level'].value_counts().to_dict()
  meta = {
    'scanned_at': datetime.now().isoformat(),
    'total_ao': len(df),
    'critical_count': level_counts.get('CRITICAL', 0),
    'warning_count':  level_counts.get('WARNING', 0),
    'ok_count':       level_counts.get('OK', 0),
  }

  demo_df = select_demo_listings(df, n=1)
  return df, demo_df, meta
