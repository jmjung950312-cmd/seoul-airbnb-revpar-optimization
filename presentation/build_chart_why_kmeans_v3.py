"""
K-Means 자치구 분류 차트 — v3 클린 버전
원칙: 한 차트에 메시지 하나. "같은 서울, 다른 시장"
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Ellipse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_PATH = os.path.join(PROJECT_DIR, "data/processed/district_clustered.csv")
VIZ_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(VIZ_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# ─── 설정 ─────────────────────────────────────────
COLORS = {
    "핫플 수익형":       "#FF5A5F",
    "프리미엄 비즈니스": "#00A699",
    "로컬 주거형":       "#B0B8C1",
    "가성비 신흥형":     "#6B7280",
}
CLUSTER_ORDER = ["핫플 수익형", "프리미엄 비즈니스", "로컬 주거형", "가성비 신흥형"]

DISTRICT_KR = {
    'Mapo-gu': '마포구', 'Gangnam-gu': '강남구', 'Jongno-gu': '종로구',
    'Jung-gu': '중구', 'Yongsan-gu': '용산구', 'Seocho-gu': '서초구',
    'Gwanak-gu': '관악구', 'Seodaemun-gu': '서대문구', 'Songpa-gu': '송파구',
    'Gwangjin-gu': '광진구', 'Seongdong-gu': '성동구',
    'Dongdaemun-gu': '동대문구', 'Dongjak-gu': '동작구',
    'Geumcheon-gu': '금천구', 'Guro-gu': '구로구',
    'Yeongdeungpo-gu': '영등포구', 'Gangseo-gu': '강서구',
    'Gangdong-gu': '강동구', 'Gangbuk-gu': '강북구',
    'Eunpyeong-gu': '은평구', 'Seongbuk-gu': '성북구',
    'Yangcheon-gu': '양천구', 'Nowon-gu': '노원구',
    'Dobong-gu': '도봉구', 'Jungnang-gu': '중랑구',
}

# 클러스터별 대표 자치구만 라벨 (나머지는 점만)
LABEL_SHOW = {
    'Mapo-gu', 'Gangnam-gu', 'Yongsan-gu',  # 상위
    'Geumcheon-gu', 'Gwanak-gu',             # 하위 (대비)
}

# ─── 차트 ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# 차트 제목
ax.set_title('25개 자치구, 4개 시장 유형',
             fontsize=16, fontweight='bold', color='#484848',
             pad=16, loc='left')

# 1. 클러스터 영역 (가볍게)
for name in CLUSTER_ORDER:
    group = df[df['cluster_name'] == name]
    cx = group['total_listings'].mean()
    cy = group['median_revpar_ao'].mean()
    if len(group) > 1:
        sx = (group['total_listings'].max() - group['total_listings'].min()) + 800
        sy = (group['median_revpar_ao'].max() - group['median_revpar_ao'].min()) + 6000
    else:
        sx, sy = 1500, 6000
    ellipse = Ellipse(
        (cx, cy), sx, sy,
        alpha=0.06, facecolor=COLORS[name],
        edgecolor='none', zorder=1
    )
    ax.add_patch(ellipse)

# 2. 점 찍기
for name in CLUSTER_ORDER:
    group = df[df['cluster_name'] == name]
    color = COLORS[name]
    size = 350 if name == "핫플 수익형" else 120
    ax.scatter(
        group['total_listings'], group['median_revpar_ao'],
        s=size, color=color, alpha=0.85,
        edgecolors='white', linewidths=1.5, zorder=5,
        label=name
    )

# 3. 라벨 — 대표 자치구만
LABEL_OFFSETS = {
    'Mapo-gu':     (0, 16),
    'Gangnam-gu':  (0, -16),
    'Yongsan-gu':  (0, 14),
    'Geumcheon-gu': (30, -10),
    'Gwanak-gu':   (30, 5),
}
for _, row in df.iterrows():
    if row['district'] not in LABEL_SHOW:
        continue
    label = DISTRICT_KR[row['district']]
    offset = LABEL_OFFSETS.get(row['district'], (0, 10))
    is_hero = row['district'] == 'Mapo-gu'
    ax.annotate(
        label,
        (row['total_listings'], row['median_revpar_ao']),
        fontsize=11 if is_hero else 9,
        fontweight='bold' if is_hero else 'medium',
        ha='center', va='center',
        textcoords="offset points", xytext=offset,
        color=COLORS[row['cluster_name']],
        zorder=15
    )

# 4. 격차 표시 — 세로 점선 + 라벨 (마포 vs 금천)
mid_x = 3800
ax.plot(
    [mid_x, mid_x], [26500, 63000],
    color='#FF5A5F', linewidth=1.2, linestyle=':', alpha=0.6, zorder=2
)
ax.annotate(
    '같은 서울,\nRevPAR 2.4배 차이',
    xy=(mid_x, 44500),
    fontsize=10, color='#FF5A5F', fontweight='bold',
    ha='left', va='center',
    xytext=(mid_x + 200, 44500),
    bbox=dict(
        boxstyle='round,pad=0.4',
        facecolor='#FFF0F1', edgecolor='none', alpha=0.9
    ),
    zorder=20
)

# 5. 축 스타일링
ax.set_xlabel('총 리스팅 수', fontsize=12, color='#484848', labelpad=12)
ax.set_ylabel('RevPAR 중위값', fontsize=12, color='#484848', labelpad=12)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#E5E7EB')
ax.spines['bottom'].set_color('#E5E7EB')
ax.tick_params(colors='#9CA3AF', labelsize=10)

# y축: ₩ + 천단위
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₩{x/10000:.1f}만'))
ax.yaxis.set_major_locator(mticker.MultipleLocator(10000))

# x축: 천단위 (겹침 해결)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1000:.0f}천' if x > 0 else '0'))
ax.xaxis.set_major_locator(mticker.MultipleLocator(1000))
ax.tick_params(axis='x', rotation=0)

ax.grid(axis='y', alpha=0.12, color='#D1D5DB')

ax.set_ylim(20000, 68000)
ax.set_xlim(-200, 7500)

# 6. 범례 — 우측 빈 공간 (4천~7천 × ₩2만~₩4만 영역)
legend = ax.legend(
    fontsize=10, loc='center right',
    ncol=1, frameon=True, fancybox=True, shadow=False,
    edgecolor='#E5E7EB', facecolor='white',
    bbox_to_anchor=(0.98, 0.28),
    handletextpad=0.5, labelspacing=0.8,
    markerscale=1.3
)
legend.get_frame().set_linewidth(0.8)
legend.get_frame().set_alpha(0.95)

plt.tight_layout()

# ─── 저장 ─────────────────────────────────────────
chart_path = os.path.join(VIZ_DIR, "ppt_why_kmeans_scatter_v3.png")
plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"✅ 차트 저장: {chart_path}")
