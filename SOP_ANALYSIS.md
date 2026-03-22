# 📋 Analysis SOP (Standard Operating Procedure)

**Domain:** 서울 에어비앤비 (Hospitality)
**Version:** 1.0
**Analysis Targets:**
- 호스트 관점: 물건 단위 RevPAR 최적화 포인트 탐색
- 자치구 단위 보조 분석: 자치구 RevPAR 패턴 탐색

## 1️⃣ 데이터 전처리 (완료)

> ⚠️ **전처리는 _final.ipynb에서 이미 완료됨 — 추가 전처리 불필요**

완료된 전처리:
- district 결측치 → Spatial Join으로 채움
- 이상치 제거: min_nights>730, ttm_avg_rate>2M
- 외부 데이터 병합: POI, 환율, 인구
- 파생변수: refined_status, operation_status, baths_group 등

제외 컬럼: exng, ttm_exng (상수), nearest_poi_image (23.9% 결측, 불필요)

## 2️⃣ RevPAR 분석 필터

전체 32,061개 분석 + 활성(Active+Operating) 14,399개 서브셋 별도 분석

## 3️⃣ 필수 파생 변수

- `revpar_trend` = (l90d_revpar - ttm_revpar/4) / (ttm_revpar/4 + 1e-6)
- `log_ttm_revpar` = np.log1p(ttm_revpar)
- `is_active_operating` = (refined_status=='Active') & (operation_status=='Operating')

## 4️⃣ 시각화 기준

- 폰트: AppleGothic
- 최대 figure 크기: (14, 8)
- 서브플롯: 최대 2×2
- DPI: 100
- 색상 팔레트: Set2

## 5️⃣ KPI 정의

- **RevPAR** = ADR × Occupancy Rate
- **ADR** = ttm_avg_rate (일평균 가격)
- **Occupancy** = ttm_occupancy (0-1 스케일)
- **Trend** = l90d_revpar vs ttm_revpar 비교

## 6️⃣ 재현성

- Random seed: **42** (항상!)
- Train/test: 80/20
- CV: 5-fold
