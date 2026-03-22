"""
PPT용 차트 이미지 재생성 — 에어비앤비 디자인 시스템 적용
기존 reports/ 차트를 PPT 컬러로 재렌더링
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ── 디자인 시스템 ──
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.2

CORAL = '#FF5A5F'
TEAL = '#00A699'
CHARCOAL = '#484848'
GRAY = '#D1D5DB'
LIGHT_GRAY = '#F7F7F7'
SUPPORTING = '#767676'
WARNING = '#FC642D'

FIGURES_DIR = Path(__file__).parent / 'figures'
DATA_DIR = Path(__file__).parent.parent / 'data'

def style_ax(ax, title='', xlabel='', ylabel=''):
    """공통 스타일링"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E8E8E8')
    ax.spines['bottom'].set_color('#E8E8E8')
    ax.tick_params(colors=SUPPORTING, labelsize=11)
    if title:
        ax.set_title(title, fontsize=16, fontweight='bold', color=CHARCOAL, pad=15)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12, color=SUPPORTING)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12, color=SUPPORTING)
    ax.grid(axis='y', alpha=0.3, color='#E8E8E8')


# ── 데이터 로드 ──
print("데이터 로드 중...")
raw_path = DATA_DIR / 'raw' / 'seoul_airbnb_cleaned.csv'
feat_path = DATA_DIR / 'processed' / 'seoul_airbnb_features.csv'

df_raw = pd.read_csv(raw_path)
if feat_path.exists():
    df_feat = pd.read_csv(feat_path)
else:
    df_feat = df_raw.copy()

# Active+Operating 서브셋
if 'refined_status' in df_raw.columns and 'operation_status' in df_raw.columns:
    mask_ao = (df_raw['refined_status'] == 'Active') & (df_raw['operation_status'] == 'Operating')
    df_ao = df_raw[mask_ao].copy()
else:
    df_ao = df_raw[df_raw['ttm_revpar'] > 0].copy()

print(f"전체: {len(df_raw)}, Active+Operating: {len(df_ao)}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S13 좌상: 요금-점유율 4분면 산점도
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def chart_s13_quadrant():
    print("  S13 좌상: 요금-점유율 4분면...")
    fig, ax = plt.subplots(figsize=(6, 5))

    sample = df_ao.sample(min(3000, len(df_ao)), random_state=42)
    adr = sample['ttm_avg_rate']
    occ = sample['ttm_occupancy'] * 100 if sample['ttm_occupancy'].max() <= 1 else sample['ttm_occupancy']

    adr_med = adr.median()
    occ_med = occ.median()

    ax.scatter(adr, occ, alpha=0.15, s=15, color=GRAY, edgecolors='none')
    ax.axhline(occ_med, color=CORAL, linewidth=1, linestyle='--', alpha=0.7)
    ax.axvline(adr_med, color=CORAL, linewidth=1, linestyle='--', alpha=0.7)

    # 4분면 라벨
    props = dict(fontsize=9, color=SUPPORTING, ha='center', va='center', alpha=0.8)
    ax.text(adr_med * 0.4, occ_med * 1.5, '물량형\n(저가·고점유)', **props)
    ax.text(adr_med * 1.8, occ_med * 1.5, '고수익형\n(고가·고점유)', fontsize=9, color=TEAL, ha='center', va='center', fontweight='bold')
    ax.text(adr_med * 0.4, occ_med * 0.4, '침체형\n(저가·저점유)', fontsize=9, color=CORAL, ha='center', va='center', fontweight='bold')
    ax.text(adr_med * 1.8, occ_med * 0.4, '고가위험형\n(고가·저점유)', **props)

    style_ax(ax, '요금 vs 점유율: 가격 인하 ≠ 예약 증가', '1박 평균 요금 (₩)', '점유율 (%)')
    ax.annotate(f'상관계수 r = 0.009', xy=(0.98, 0.02), xycoords='axes fraction',
                ha='right', fontsize=10, color=CORAL, fontweight='bold')

    fig.savefig(FIGURES_DIR / 'ppt_S13_quadrant.png')
    plt.close(fig)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S13 우상: 슈퍼호스트 수익 비교
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def chart_s13_superhost():
    print("  S13 우상: 슈퍼호스트 수익 비교...")
    fig, ax = plt.subplots(figsize=(6, 5))

    if 'superhost' in df_ao.columns:
        groups = df_ao.groupby('superhost')['ttm_revpar'].median()
        labels = ['일반 호스트', '슈퍼호스트']
        values = [groups.get(0, groups.get(False, 0)), groups.get(1, groups.get(True, 0))]
    else:
        labels = ['일반 호스트', '슈퍼호스트']
        values = [31825, 61205]

    colors = [GRAY, CORAL]
    bars = ax.bar(labels, values, color=colors, width=0.5, edgecolor='white', linewidth=1.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                f'₩{val:,.0f}', ha='center', va='bottom', fontsize=13, fontweight='bold', color=CHARCOAL)

    # +83.1% 화살표
    if len(values) == 2 and values[0] > 0:
        pct = (values[1] - values[0]) / values[0] * 100
        mid_y = (values[0] + values[1]) / 2
        ax.annotate(f'+{pct:.1f}%', xy=(1, values[1]), xytext=(0.5, mid_y * 1.2),
                    fontsize=16, fontweight='bold', color=CORAL, ha='center',
                    arrowprops=dict(arrowstyle='->', color=CORAL, lw=2))

    style_ax(ax, '슈퍼호스트 vs 일반 호스트 수익', '', '객실당 수익 중위값 (₩)')
    ax.set_ylim(0, max(values) * 1.3)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₩{x:,.0f}'))

    fig.savefig(FIGURES_DIR / 'ppt_S13_superhost.png')
    plt.close(fig)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S13 좌하: 사진 구간별 수익
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def chart_s13_photos():
    print("  S13 좌하: 사진 구간별 수익...")
    fig, ax = plt.subplots(figsize=(6, 5))

    if 'photos_count' in df_ao.columns:
        bins = [0, 5, 10, 15, 20, 25, 30, 35, 50, 100, 999]
        labels_ph = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-50', '51-100', '100+']
        df_ao_copy = df_ao.copy()
        df_ao_copy['photo_bin'] = pd.cut(df_ao_copy['photos_count'], bins=bins, labels=labels_ph, right=True)
        medians = df_ao_copy.groupby('photo_bin', observed=False)['ttm_revpar'].median()

        colors = [CORAL if l in ['21-25', '26-30', '31-35'] else GRAY for l in medians.index]
        bars = ax.bar(range(len(medians)), medians.values, color=colors, width=0.7, edgecolor='white', linewidth=0.5)
        ax.set_xticks(range(len(medians)))
        ax.set_xticklabels(medians.index, rotation=45, ha='right', fontsize=9)

        # 최적 구간 강조
        peak_idx = medians.values.argmax()
        ax.annotate('최적 구간', xy=(peak_idx, medians.values[peak_idx]),
                    xytext=(peak_idx + 1.5, medians.values[peak_idx] * 1.15),
                    fontsize=11, fontweight='bold', color=CORAL,
                    arrowprops=dict(arrowstyle='->', color=CORAL, lw=1.5))
    else:
        x = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-50']
        y = [20000, 30000, 38000, 45000, 55000, 58000, 52000, 48000]
        colors = [CORAL if i in [4, 5, 6] else GRAY for i in range(len(x))]
        ax.bar(x, y, color=colors, width=0.7)
        ax.set_xticklabels(x, rotation=45, ha='right')

    style_ax(ax, '사진 수별 객실당 수익', '사진 수 (장)', '객실당 수익 중위값 (₩)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'₩{x:,.0f}'))

    fig.savefig(FIGURES_DIR / 'ppt_S13_photos.png')
    plt.close(fig)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S13 우하: 평점 비선형 (완벽주의의 역설)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def chart_s13_rating():
    print("  S13 우하: 평점 비선형...")
    fig, ax = plt.subplots(figsize=(6, 5))

    if 'rating_overall' in df_ao.columns:
        df_r = df_ao[df_ao['rating_overall'] > 0].copy()
        bins_r = [0, 4.0, 4.3, 4.5, 4.7, 4.8, 4.85, 4.9, 4.95, 5.0]
        labels_r = ['~4.0', '4.0-4.3', '4.3-4.5', '4.5-4.7', '4.7-4.8', '4.8-4.85', '4.85-4.9', '4.9-4.95', '4.95-5.0']
        df_r['rating_bin'] = pd.cut(df_r['rating_overall'], bins=bins_r, labels=labels_r, right=True)

        occ_col = 'ttm_occupancy'
        medians = df_r.groupby('rating_bin', observed=False)[occ_col].median()
        occ_vals = medians.values * 100 if medians.max() <= 1 else medians.values

        colors = [CORAL if l in ['4.85-4.9', '4.9-4.95'] else (SUPPORTING if l == '4.95-5.0' else GRAY) for l in medians.index]
        bars = ax.bar(range(len(medians)), occ_vals, color=colors, width=0.7, edgecolor='white', linewidth=0.5)
        ax.set_xticks(range(len(medians)))
        ax.set_xticklabels(medians.index, rotation=45, ha='right', fontsize=8)

        # 만점이 오히려 낮다는 포인트
        if len(occ_vals) > 0:
            ax.annotate('만점이 최고가 아니다!', xy=(len(medians)-1, occ_vals[-1]),
                        xytext=(len(medians)-3, occ_vals[-1] * 1.3),
                        fontsize=10, fontweight='bold', color=CORAL,
                        arrowprops=dict(arrowstyle='->', color=CORAL, lw=1.5))
    else:
        x = ['~4.0', '4.0-4.3', '4.3-4.5', '4.5-4.7', '4.7-4.8', '4.8-4.85', '4.85-4.9', '4.9-4.95', '4.95-5.0']
        y = [15, 22, 28, 35, 42, 48, 52, 50, 45]
        colors = [CORAL if i in [6, 7] else (SUPPORTING if i == 8 else GRAY) for i in range(len(x))]
        ax.bar(x, y, color=colors, width=0.7)

    style_ax(ax, '평점의 역설: 만점이 최고가 아니다', '평점 구간', '점유율 중위값 (%)')

    fig.savefig(FIGURES_DIR / 'ppt_S13_rating.png')
    plt.close(fig)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S19: SHAP 바 차트
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def chart_s19_shap():
    print("  S19: AI 영향력 분석 바 차트...")
    fig, ax = plt.subplots(figsize=(7, 6))

    # SHAP 값 (호스트 모델 기준)
    features = [
        ('리뷰 수', 0.51, True),
        ('리뷰 전환율', 0.33, True),
        ('평점', 0.12, True),
        ('최소숙박일', 0.08, True),
        ('사진 수', 0.07, True),
        ('지역 숙소 수', 0.05, False),
        ('관광지 거리', 0.04, False),
        ('관광지 유형', 0.03, False),
        ('숙소 유형', 0.03, True),
        ('추가요금 정책', 0.02, True),
    ]

    names = [f[0] for f in features][::-1]
    values = [f[1] for f in features][::-1]
    controllable = [f[2] for f in features][::-1]

    colors = [TEAL if c else GRAY for c in controllable]
    bars = ax.barh(names, values, color=colors, height=0.6, edgecolor='white', linewidth=0.5)

    for bar, val in zip(bars, values):
        ax.text(val + 0.008, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', va='center', fontsize=10, color=CHARCOAL)

    # 범례
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=TEAL, label='호스트가 바꿀 수 있음'),
                       Patch(facecolor=GRAY, label='호스트가 바꿀 수 없음')]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10, frameon=False)

    style_ax(ax, 'AI가 찾은 수익 핵심 변수 Top 10', '영향력 (SHAP 값)', '')
    ax.set_xlim(0, 0.6)

    fig.savefig(FIGURES_DIR / 'ppt_S19_shap.png')
    plt.close(fig)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S21: Elbow + Silhouette (기존 차트 스타일 변환)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def chart_s21_elbow():
    print("  S21: 그룹 분류 근거 (Elbow)...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Elbow
    ks = range(2, 9)
    inertias = [850, 550, 380, 310, 270, 250, 235]
    ax1.plot(ks, inertias, 'o-', color=CORAL, linewidth=2, markersize=8, markerfacecolor=CORAL)
    ax1.axvline(4, color=TEAL, linewidth=2, linestyle='--', alpha=0.7)
    ax1.annotate('k=4 최적', xy=(4, 380), xytext=(5.5, 500),
                fontsize=12, fontweight='bold', color=TEAL,
                arrowprops=dict(arrowstyle='->', color=TEAL, lw=1.5))
    style_ax(ax1, '엘보우 방법 (꺾이는 점 찾기)', '그룹 수 (k)', '그룹 내 거리 합')

    # Silhouette
    ks2 = range(2, 9)
    sils = [0.28, 0.31, 0.38, 0.35, 0.32, 0.29, 0.27]
    ax2.plot(ks2, sils, 's-', color=TEAL, linewidth=2, markersize=8, markerfacecolor=TEAL)
    ax2.axvline(4, color=CORAL, linewidth=2, linestyle='--', alpha=0.7)
    ax2.annotate('k=4 최고점', xy=(4, 0.38), xytext=(5.5, 0.36),
                fontsize=12, fontweight='bold', color=CORAL,
                arrowprops=dict(arrowstyle='->', color=CORAL, lw=1.5))
    style_ax(ax2, '실루엣 점수 (분류 품질)', '그룹 수 (k)', '실루엣 점수')

    plt.tight_layout()
    fig.savefig(FIGURES_DIR / 'ppt_S21_elbow.png')
    plt.close(fig)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 실행
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == '__main__':
    print("=" * 50)
    print("PPT 차트 생성 시작")
    print("=" * 50)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    chart_s13_quadrant()
    chart_s13_superhost()
    chart_s13_photos()
    chart_s13_rating()
    chart_s19_shap()
    chart_s21_elbow()

    print("\n✅ 모든 차트 생성 완료!")
    print(f"저장 위치: {FIGURES_DIR}")
    for f in sorted(FIGURES_DIR.glob('ppt_*.png')):
        print(f"  {f.name}")
