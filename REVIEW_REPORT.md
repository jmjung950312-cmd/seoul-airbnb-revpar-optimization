# 포트폴리오 리뷰 리포트 — 서울 에어비앤비 수익 최적화

> 리뷰 일자: 2026-03-22 (2차 통합) | 리뷰어: analysis, code, portfolio

## 종합 점수

| 관점 | 1차 (03-20) | 2차 (03-22) | 요약 |
|------|------------|------------|------|
| 분석 논리 | 8.0/10 | 8.0/10 | 2-stage ML + OOF 우수, 모델 검증 코드 이제 포함 |
| 코드 품질 | 8.5/10 | 8.0/10 | 한글 폰트 호환, 캐싱 전략 우수 |
| 채용 관점 | 8.5/10 | 8.5/10 | 도메인 전문성 + 프로덕트 완성도 |
| **평균** | **8.3** | **8.2** | |

---

## 잘된 점

### 분석 논리
- 2-stage ML (ADR + Occupancy 분리) + Isotonic Regression 보정이 도메인에 적합
- price_gap_oof 피처로 가격 탄력성 포착, OOF로 데이터 누수 방지
- 4개 클러스터별 전략 차별화 (핫플 수익형, 프리미엄 비즈니스 등)
- 헬스 스코어 5개 컴포넌트 설계가 해석 가능하고 액셔너블
- 노트북 7개로 분석 전 과정을 재현 가능하게 문서화

### 코드 품질
- OS별 한글 폰트 분기 + Noto Sans KR 우선 + unicode_minus 처리 완벽
- `@st.cache_data` / `@st.cache_resource` 적절 분리
- predict_utils.py docstring이 모범적 (입출력 스펙, 사용 예시)
- requirements.txt에 최소 버전 명시로 재현성 확보
- BEP 예약률 0% 예외 처리 추가 (2차)

### 채용 관점
- README 첫 문장에서 가치 제안 명확 ("3분 만에 맞춤 수익 전략")
- 스크린샷 풍부 (라이트/다크 모드 비교)
- PORTFOLIO.md 이력서 바로 복사 가능 수준
- 에어비앤비 Korea 6년 경력과 직접 연계되는 프로젝트
- 라이브 대시보드 배포로 프로덕트 완성도 증명
- End-to-End 구조 (분석 노트북 + ML + 대시보드 + Web)

---

## 수정 체크리스트

### [필수]

- [x] **모델 학습/검증 코드**: 레포에 노트북(notebooks/03_host_modeling.ipynb) 포함으로 해결 — (analysis, portfolio)

### [권장]

- [x] **revpar_trend 공식 단위 명시** (`predict_utils.py:178`): l90d_revpar, ttm_revpar 모두 일평균 RevPAR(₩/일) 단위 주석 추가 — (analysis)
- [x] **Isotonic Regression 외삽 경고** (`predict_utils.py:170-171`): 학습 범위 밖 입력 시 flat 예측 가능성에 대한 경고 주석 추가 — (analysis)
- [x] **BEP 예약률 0% 안내** (`app.py:1839`): my_occ=0일 때 "BEP 계산 불가 — 예약이 없으면 손익분기를 달성할 수 없습니다" 안내로 변경 — (analysis)
- [x] **app.py 단일 파일 방어 논리 보강**: PORTFOLIO.md에 "향후 모듈화 계획" 한 줄 추가 — (portfolio)
- [x] **라이브 데모 링크 추가**: README 상단에 Streamlit Cloud 배포 URL 배치 — (portfolio)
- [x] **requirements.txt에 requests 추가**: Nominatim API 호출에 필요한 패키지 명시 — (code)
- [x] **슈퍼호스트 프리미엄 표현 수정**: "데이터로 입증" → "데이터에서 관찰"로 변경 — (portfolio)
- [x] **클러스터링 k=4 선택 근거**: README에 실루엣 분석 기반 선택 근거 한 줄 추가 — (portfolio)
- [ ] **수수료 로직 이중화**: predict_utils.py에서 수수료 미반영, app.py:1837에서 별도 계산. 한 곳에서 관리 — (code)
- [ ] **4단계 스크린샷 누락**: 5단계 위자드 중 4단계(운영 체크)만 빠져 있음 — (portfolio)

### 2차 통합에서 추가된 작업

- [x] **프로젝트 통합**: cleaned_B를 메인 레포로, Streamlit/Web 대시보드를 dashboard/ 하위로 복사
- [x] **루트 README.md 재작성**: 분석 프로젝트 전체를 포괄하는 통합 문서
- [x] **루트 PORTFOLIO.md 생성**: 분석 + 대시보드 전체를 포괄하는 포트폴리오 요약
- [x] **.gitignore 업데이트**: _archive/, node_modules/, .next/ 등 추가

---

## 수정 규모: 중규모 (프로젝트 구조 통합)

---

## 다음 단계

1. 4단계(운영 체크) 스크린샷 추가
2. Web 대시보드(Next.js + FastAPI) 배포
3. 수수료 로직 일원화 (predict_utils.py 또는 app.py 한 곳에서 관리)
4. GitHub 레포 공개 및 포트폴리오 사이트 연동
