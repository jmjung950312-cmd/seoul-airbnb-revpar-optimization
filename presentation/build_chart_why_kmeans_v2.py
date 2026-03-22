"""
K-Means 자치구 분류 차트 — 발표용 리디자인 v2
청중이 3초 안에 "같은 서울인데 시장이 이렇게 다르다"를 파악할 수 있도록 설계
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.offsetbox import AnchoredText

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_PATH = os.path.join(PROJECT_DIR, "data/processed/district_clustered.csv")
VIZ_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(VIZ_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# ─── 색상 + 클러스터 정보 ─────────────────────────
CLUSTER_META = {
    "핫플 수익형":       {"color": "#FF5A5F", "light": "#FFF0F1", "marker": "★", "tag": "공급 최대 + 수익 최고"},
    "프리미엄 비즈니스": {"color": "#00A699", "light": "#E0F7F5", "marker": "◆", "tag": "관광·비즈니스 중심지"},
    "로컬 주거형":       {"color": "#9CA3AF", "light": "#F3F4F6", "marker": "●", "tag": "생활권 기반 중간 수익"},
    "가성비 신흥형":     {"color": "#6B7280", "light": "#F9FAFB", "marker": "▲", "tag": "비활성 63%, 수요 부족"},
}
CLUSTER_ORDER = ["핫플 수익형", "프리미엄 비즈니스", "로컬 주거형", "가성비 신흥형"]

# 자치구명 한글 매핑
DISTRICT_KR = {
    'Mapo-gu': '마포', 'Gangnam-gu': '강남', 'Jongno-gu': '종로',
    'Jung-gu': '중구', 'Yongsan-gu': '용산', 'Seocho-gu': '서초',
    'Gwanak-gu': '관악', 'Seodaemun-gu': '서대문', 'Songpa-gu': '송파',
    'Gwangjin-gu': '광진', 'Seongdong-gu': '성동',
    'Dongdaemun-gu': '동대문', 'Dongjak-gu': '동작',
    'Geumcheon-gu': '금천', 'Guro-gu': '구로',
    'Yeongdeungpo-gu': '영등포', 'Gangseo-gu': '강서',
    'Gangdong-gu': '강동', 'Gangbuk-gu': '강북',
    'Eunpyeong-gu': '은평', 'Seongbuk-gu': '성북',
    'Yangcheon-gu': '양천', 'Nowon-gu': '노원',
    'Dobong-gu': '도봉', 'Jungnang-gu': '중랑',
}

# 주요 자치구만 라벨 표시 (나머지는 점만)
KEY_DISTRICTS = {
    'Mapo-gu', 'Gangnam-gu', 'Jongno-gu', 'Jung-gu', 'Yongsan-gu',
    'Seocho-gu', 'Gwanak-gu', 'Seodaemun-gu', 'Songpa-gu',
    'Gwangjin-gu', 'Seongdong-gu', 'Geumcheon-gu',
}

# ─── 차트 생성 ────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
fig.patch.set_facecolor('white')
ax.set_facecolor('#FAFAFA')

# --- 1. 클러스터별 영역 표시 (배경 타원) ---
from matplotlib.patches import Ellipse

cluster_zones = {}
for name in CLUSTER_ORDER:
    group = df[df['cluster_name'] == name]
    cx = group['total_listings'].mean()
    cy = group['median_revpar_ao'].mean()
    # 영역 크기: 데이터 범위 + 여유
    if len(group) > 1:
        sx = (group['total_listings'].max() - group['total_listings'].min()) * 0.7 + 400
        sy = (group['median_revpar_ao'].max() - group['median_revpar_ao'].min()) * 0.6 + 3000
    else:
        sx, sy = 1200, 5000  # 마포구 단독
    cluster_zones[name] = (cx, cy, sx, sy)

    ellipse = Ellipse(
        (cx, cy), sx, sy,
        alpha=0.08, facecolor=CLUSTER_META[name]['color'],
        edgecolor=CLUSTER_META[name]['color'], linewidth=1.2,
        linestyle='--', zorder=1
    )
    ax.add_patch(ellipse)

# --- 2. 데이터 포인트 ---
for name in CLUSTER_ORDER:
    group = df[df['cluster_name'] == name]
    meta = CLUSTER_META[name]

    # 마포구는 더 크게 강조
    if name == "핫플 수익형":
        sizes = [400]
        ax.scatter(
            group['total_listings'], group['median_revpar_ao'],
            s=sizes, color=meta['color'], alpha=0.9,
            edgecolors='white', linewidths=2.5, zorder=10,
            label=f"{meta['marker']} {name}"
        )
    else:
        ax.scatter(
            group['total_listings'], group['median_revpar_ao'],
            s=160, color=meta['color'], alpha=0.8,
            edgecolors='white', linewidths=1.5, zorder=5,
            label=f"{meta['marker']} {name}"
        )

# --- 3. 라벨 (주요 자치구만, 겹침 최소화) ---
# 라벨 위치 미세 조정
LABEL_OFFSETS = {
    'Mapo-gu': (0, 14),
    'Gangnam-gu': (0, -18),
    'Jongno-gu': (0, 12),
    'Jung-gu': (25, -5),
    'Yongsan-gu': (0, 12),
    'Seocho-gu': (0, -18),
    'Gwanak-gu': (0, 12),
    'Seodaemun-gu': (0, 12),
    'Songpa-gu': (25, 5),
    'Gwangjin-gu': (0, 12),
    'Seongdong-gu': (0, 12),
    'Geumcheon-gu': (0, 12),
}

for _, row in df.iterrows():
    if row['district'] not in KEY_DISTRICTS:
        continue
    label = DISTRICT_KR.get(row['district'], row['district'])
    offset = LABEL_OFFSETS.get(row['district'], (0, 10))
    fontsize = 11 if row['district'] == 'Mapo-gu' else 8.5
    fontweight = 'bold' if row['district'] == 'Mapo-gu' else 'medium'

    ax.annotate(
        label,
        (row['total_listings'], row['median_revpar_ao']),
        fontsize=fontsize, ha='center', va='center',
        textcoords="offset points", xytext=offset,
        color='#374151', fontweight=fontweight,
        zorder=15
    )

# --- 4. 마포구 콜아웃 화살표 ---
mapo = df[df['district'] == 'Mapo-gu'].iloc[0]
ax.annotate(
    '공급 6,699개\n(2위의 1.9배)\n수익도 1위',
    xy=(mapo['total_listings'], mapo['median_revpar_ao']),
    xytext=(5200, 58000),
    fontsize=9, color='#FF5A5F', fontweight='bold',
    ha='center', va='center',
    bbox=dict(
        boxstyle='round,pad=0.5',
        facecolor='#FFF0F1', edgecolor='#FF5A5F',
        linewidth=1.2, alpha=0.95
    ),
    arrowprops=dict(
        arrowstyle='->', color='#FF5A5F',
        lw=1.5, connectionstyle='arc3,rad=-0.2'
    ),
    zorder=20
)

# --- 5. 금천구 콜아웃 (대비용) ---
geum = df[df['district'] == 'Geumcheon-gu'].iloc[0]
ax.annotate(
    '공급 147개\n비활성 77%',
    xy=(geum['total_listings'], geum['median_revpar_ao']),
    xytext=(600, 22500),
    fontsize=8.5, color='#6B7280', fontweight='bold',
    ha='center', va='center',
    bbox=dict(
        boxstyle='round,pad=0.4',
        facecolor='#F3F4F6', edgecolor='#9CA3AF',
        linewidth=1, alpha=0.95
    ),
    arrowprops=dict(
        arrowstyle='->', color='#9CA3AF',
        lw=1.2, connectionstyle='arc3,rad=0.2'
    ),
    zorder=20
)

# --- 6. 격차 표시 (점선 + 라벨) ---
ax.annotate(
    '',
    xy=(3500, 63000), xytext=(3500, 26500),
    arrowprops=dict(
        arrowstyle='<->', color='#FF5A5F',
        lw=1.5, linestyle='--'
    ),
    zorder=3
)
ax.text(
    3700, 44500, 'RevPAR\n2.4배 차이',
    fontsize=10, color='#FF5A5F', fontweight='bold',
    ha='left', va='center',
    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none', alpha=0.8)
)

# --- 7. 축 스타일링 ---
ax.set_xlabel('총 리스팅 수 (공급량)', fontsize=12, color='#484848', labelpad=12)
ax.set_ylabel('RevPAR 중위값 (₩)', fontsize=12, color='#484848', labelpad=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#E5E7EB')
ax.spines['bottom'].set_color('#E5E7EB')
ax.tick_params(colors='#6B7280', labelsize=10)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₩{x:,.0f}'))
ax.grid(axis='both', alpha=0.15, color='#D1D5DB', linestyle='-')

# y축 범위 여유
ax.set_ylim(20000, 68000)
ax.set_xlim(-200, 7500)

# --- 8. 범례 (하단 중앙, 가로 배치) ---
legend = ax.legend(
    fontsize=10, loc='lower center',
    ncol=4, frameon=True, fancybox=True, shadow=False,
    edgecolor='#E5E7EB', facecolor='white',
    bbox_to_anchor=(0.5, -0.12),
    columnspacing=2.0, handletextpad=0.5
)
legend.get_frame().set_linewidth(0.8)

plt.tight_layout()
plt.subplots_adjust(bottom=0.13)

# ─── 저장 ────────────────────────────────────────
chart_path = os.path.join(VIZ_DIR, "ppt_why_kmeans_scatter_v2.png")
plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"✅ 차트 저장: {chart_path}")
