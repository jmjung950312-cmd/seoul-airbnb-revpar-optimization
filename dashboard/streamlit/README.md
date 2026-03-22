# 서울 에어비앤비 수익 최적화 대시보드

[라이브 데모](https://seoul-airbnb-dashboard.streamlit.app/)

서울 에어비앤비 호스트를 위한 **수익 분석 및 최적화 대시보드**입니다.
32,061개 실운영 숙소 데이터와 머신러닝 모델을 기반으로, 숙소별 맞춤 수익 전략을 3분 만에 제공합니다.

## 주요 기능

### 5단계 위자드 플로우

| 단계 | 기능 | 설명 |
|------|------|------|
| 1단계 | 숙소 기본 정보 | 호스트 유형(신규/기존) 및 숙소 종류 선택 |
| 2단계 | 숙소 설정 | 1박 요금, 수용 인원, 숙소 구성, 인테리어 스타일, 주소 입력 |
| 3단계 | 월 운영비 입력 | 공과금, 관리비, 청소비, 대출이자 등 고정 비용 입력 |
| 4단계 | 운영 체크 (기존 호스트) | 예약 현황, 리뷰, 슈퍼호스트 여부 등 운영 지표 입력 |
| 5단계 | 분석 결과 | 6개 탭으로 구성된 종합 분석 리포트 |

### 분석 결과 (6개 탭)

- **수익 요약** -- 월 매출, 순이익, 적자 예방 최소 요금, 손익 계산서 (도넛 차트)
- **요금 추천** -- 지역 데이터 기반 적정 1박 요금 구간, 신규 진입 전략
- **주변 관광지** -- 숙소 반경 500m/1km/2km 관광지, 가장 가까운 POI TOP 5
- **지역 진단** -- 자치구 시장 유형(핫플 수익형 등), 수익 올리는 전략 5가지
- **헬스 스코어** -- 5가지 운영 지표(리뷰, 사진, 예약정책, 위치, 숙소구성) 종합 건강 점수
- **숙소 설명** -- AI 기반 한국어/영문 숙소 설명 자동 생성

### ML 예측 모델

- **Model A (ADR 예측)**: LightGBM -- 자치구 클러스터, POI 거리, 숙소 구성 등 13개 피처 기반 시장 적정 1박 요금 예측
- **Model B (예약률 예측)**: LightGBM -- 즉시예약, 슈퍼호스트, 리뷰, 사진 등 10개 피처 기반 예약률 예측
- **Isotonic Regression**: RevPAR(ADR x 예약률) 보정으로 예측 정확도 향상
- **헬스 스코어**: 클러스터 내 백분위 기반 5-컴포넌트 종합 점수 (0~100)

## 스크린샷

### 1단계: 숙소 기본 정보

| 라이트 모드 | 다크 모드 |
|:-:|:-:|
| ![Step 1 라이트](screenshot/step1-full.png) | ![Step 1 다크](screenshot/step1-dark-mode.png) |

### 2단계: 숙소 설정

![Step 2](screenshot/step2-full-v2.png)

### 3단계: 월 운영비 입력

![Step 3](screenshot/step3-operating-costs.png)

### 5단계: 분석 결과

| 수익 요약 | 요금 추천 |
|:-:|:-:|
| ![수익 요약](screenshot/step5-tab1-revenue.png) | ![요금 추천](screenshot/step5-tab2-pricing.png) |

### 헬스 스코어

![헬스 스코어](screenshot/final_health_score.png)

## 기술 스택

| 분류 | 기술 |
|------|------|
| 언어 | Python 3.11 |
| 프레임워크 | Streamlit 1.32+ |
| ML 모델 | LightGBM, Isotonic Regression (scikit-learn) |
| 데이터 처리 | Pandas, NumPy |
| 시각화 | Matplotlib (Noto Sans KR 한글 폰트) |
| 지리 데이터 | GeoPandas, Shapely |
| 외부 API | Nominatim (OpenStreetMap) 지오코딩 |
| 배포 | Streamlit Cloud, DevContainer |

## 프로젝트 구조

```
seoul-airbnb-dashboard-main/
├── app.py                      # 메인 앱 (~2,850줄, 단일 파일)
├── requirements.txt            # Python 의존성
├── packages.txt                # 시스템 패키지 (fonts-nanum)
├── .streamlit/
│   └── config.toml             # 테마 설정 (primaryColor: #FF5A5F)
├── .devcontainer/
│   └── devcontainer.json       # DevContainer 설정
├── data/
│   ├── raw/
│   │   └── seoul_airbnb_cleaned.csv    # 원본 리스팅 데이터
│   └── processed/
│       └── district_clustered.csv      # 클러스터링된 자치구 데이터
├── revpar_model_package/
│   ├── predict_utils.py        # 예측 헬퍼 함수
│   ├── INTEGRATION_GUIDE.md    # 모델 통합 가이드
│   ├── district_lookup.csv     # 25개 자치구 통계
│   ├── cluster_listings_ao.csv # 헬스스코어 비교용 14,399개 리스팅
│   └── models/
│       ├── model_a.pkl         # ADR 예측 모델 (LightGBM)
│       ├── model_b.pkl         # 예약률 예측 모델 (LightGBM)
│       ├── iso_reg.pkl         # Isotonic Regression 보정기
│       ├── encoders.pkl        # 카테고리 인코더
│       └── feature_config.json # 피처 설정
└── screenshot/                 # 스크린샷
```

## 실행 방법

### 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속합니다.

### DevContainer 실행

VS Code에서 프로젝트를 열고 **Reopen in Container**를 선택하면 자동으로 환경이 구성됩니다.

## 데이터

- **기간**: 2024년 10월 ~ 2025년 9월
- **규모**: 서울 25개 자치구, 32,061개 리스팅
- **출처**: Inside Airbnb 기반 가공 데이터
- **클러스터링**: K-Means 4개 클러스터 (핫플 수익형, 안정 밸류형 등) — 실루엣 분석에서 k=4가 최적 분리도를 보여 선택

## 디자인 시스템

- **컬러**: 에어비앤비 코랄(`#FF5A5F`) 기반 라이트/다크 모드
- **폰트**: Noto Sans KR (Google Fonts CDN)
- **아이콘**: Material Symbols (Streamlit 네이티브)
- **반응형**: 모바일/데스크톱 대응
