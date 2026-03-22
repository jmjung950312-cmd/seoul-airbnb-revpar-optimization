/* FastAPI 호출 클라이언트 */

import { API_BASE_URL } from './constants'
import type {
  PredictRequest,
  PredictResponse,
  HealthScoreResponse,
  BenchmarkResponse,
  GeocodeResponse,
  DashboardResults,
} from '@/types/api'

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    throw new Error(`API Error ${res.status}: ${await res.text()}`)
  }
  return res.json()
}

/* POST /predict */
export async function fetchPredict(body: PredictRequest): Promise<PredictResponse> {
  return apiFetch<PredictResponse>('/predict', {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

/* POST /health-score */
export async function fetchHealthScore(body: PredictRequest): Promise<HealthScoreResponse> {
  return apiFetch<HealthScoreResponse>('/health-score', {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

/* POST /benchmark */
export async function fetchBenchmark(
  district: string,
  roomType: string,
): Promise<BenchmarkResponse> {
  return apiFetch<BenchmarkResponse>('/benchmark', {
    method: 'POST',
    body: JSON.stringify({ district, room_type: roomType }),
  })
}

/* GET /geocode (Next.js API 프록시 사용) */
export async function fetchGeocode(address: string): Promise<GeocodeResponse> {
  const params = new URLSearchParams({ q: address })
  return apiFetch<GeocodeResponse>(`/api/geocode?${params.toString()}`)
}

/* ============================================
   Mock 데이터 (FastAPI 연결 전 개발용)
   ============================================ */
export function getMockResults(district: string): DashboardResults {
  return {
    predict: {
      adr_pred: 120000,
      occ_pred: 0.68,
      revpar_pred: 81600,
      monthly_revenue: 2448000,
      monthly_net_profit: 1850000,
      bep_rate: 55000,
      weekday_occ: 0.62,
      weekend_occ: 0.82,
      cluster_id: 2,
      cluster_label: '강남권 프리미엄 단기 숙박',
      percentile_rank: 65,
    },
    healthScore: {
      composite: 72,
      grade: 'B',
      components: [
        { name: '사진 품질', score: 15, max_score: 20, weight: 0.2, actions: ['사진을 20장 이상 추가하세요'] },
        { name: '응답률', score: 18, max_score: 20, weight: 0.2, actions: ['응답률 100% 유지'] },
        { name: '리뷰 점수', score: 17, max_score: 20, weight: 0.2, actions: [] },
        { name: '요금 경쟁력', score: 12, max_score: 20, weight: 0.2, actions: ['요금을 5% 조정하세요'] },
        { name: '예약 가용성', score: 10, max_score: 20, weight: 0.2, actions: ['가용 날짜를 늘려보세요'] },
      ],
      top_actions: ['사진을 20장 이상 추가하세요', '요금을 ₩110,000으로 조정하면 예약률이 15% 향상될 수 있습니다', '즉시 예약을 활성화하세요'],
    },
    benchmark: {
      adr_p25: 85000,
      adr_median: 110000,
      adr_p75: 145000,
      occ_p25: 0.52,
      occ_median: 0.65,
      occ_p75: 0.78,
      revpar_median: 71500,
      sample_size: 342,
    },
    pricingRec: {
      weekday_price: 110000,
      weekend_price: 145000,
      peak_multiplier: 1.4,
      discount_threshold_days: 7,
      seasonal_adjustments: {
        spring: 1.05,
        summer: 1.20,
        fall: 1.10,
        winter: 0.85,
      },
    },
    nearbyPOIs: [
      { name: '경복궁', category: '관광', distance_km: 2.3, lat: 37.5796, lng: 126.977 },
      { name: '명동 쇼핑가', category: '쇼핑', distance_km: 1.8, lat: 37.5636, lng: 126.985 },
      { name: '한강공원', category: '자연', distance_km: 3.5, lat: 37.528, lng: 126.994 },
      { name: '이태원 먹자골목', category: '음식', distance_km: 2.1, lat: 37.534, lng: 126.993 },
      { name: '지하철역 (2호선)', category: '교통', distance_km: 0.3, lat: 37.5665, lng: 126.978 },
      { name: '국립중앙박물관', category: '문화', distance_km: 4.2, lat: 37.524, lng: 126.981 },
    ],
    listingDescription: `서울 ${district}의 감성 넘치는 아늑한 숙소에 오신 것을 환영합니다.

도심 속 편안한 휴식처로, 깔끔하게 정돈된 인테리어와 필수 편의시설을 갖추었습니다. 창문 너머로 펼쳐지는 서울의 스카이라인을 즐기며 특별한 여행을 만들어보세요.

✓ 고속 Wi-Fi (500Mbps)
✓ 에어컨 및 난방 완비
✓ 완전 구비된 주방
✓ 세탁기/건조기
✓ 지하철역 도보 5분

인근에는 다양한 맛집, 카페, 편의점이 있어 생활하기 매우 편리합니다. 장기 숙박 할인도 가능하니 문의해 주세요.

도착 전 언제든지 연락 주시면 빠르게 응답드리겠습니다.`,
  }
}
