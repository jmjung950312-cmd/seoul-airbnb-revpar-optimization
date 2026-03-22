/* FastAPI 응답 관련 타입 정의 */

export interface PredictRequest {
  district: string
  room_type: string
  accommodates: number
  bedrooms: number
  bathrooms: number
  review_scores_rating: number
  review_count: number
  photos: number
  response_rate: number
  instant_bookable: boolean
  min_nights: number
  host_type: 'new' | 'existing'
  booked_days_count?: number
}

export interface PredictResponse {
  adr_pred: number
  occ_pred: number
  revpar_pred: number
  monthly_revenue: number
  monthly_net_profit: number
  bep_rate: number
  weekday_occ: number
  weekend_occ: number
  cluster_id: number
  cluster_label: string
  percentile_rank: number
}

export interface HealthScoreComponent {
  name: string
  score: number
  max_score: number
  weight: number
  actions: string[]
}

export interface HealthScoreResponse {
  composite: number
  grade: 'A' | 'B' | 'C' | 'D'
  components: HealthScoreComponent[]
  top_actions: string[]
}

export interface BenchmarkResponse {
  adr_p25: number
  adr_median: number
  adr_p75: number
  occ_p25: number
  occ_median: number
  occ_p75: number
  revpar_median: number
  sample_size: number
}

export interface GeocodeResponse {
  lat: number
  lng: number
  display_name: string
}

export interface NearbyPOI {
  name: string
  category: string
  distance_km: number
  lat: number
  lng: number
}

export interface PricingRecommendation {
  weekday_price: number
  weekend_price: number
  peak_multiplier: number
  discount_threshold_days: number
  seasonal_adjustments: Record<string, number>
}

export interface DashboardResults {
  predict: PredictResponse
  healthScore: HealthScoreResponse
  benchmark: BenchmarkResponse
  pricingRec: PricingRecommendation
  nearbyPOIs: NearbyPOI[]
  listingDescription: string
}
