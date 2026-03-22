/* 서울 에어비앤비 대시보드 상수 정의 */

import type { LanguageOption, CurrencyOption } from '@/types/locale'

/* ============================================
   서울 25개 자치구
   ============================================ */
export const DISTRICTS_KR: Record<string, string> = {
  Gangnam: '강남구',
  Gangdong: '강동구',
  Gangbuk: '강북구',
  Gangseo: '강서구',
  Gwanak: '관악구',
  Gwangjin: '광진구',
  Guro: '구로구',
  Geumcheon: '금천구',
  Nowon: '노원구',
  Dobong: '도봉구',
  Dongdaemun: '동대문구',
  Dongjak: '동작구',
  Mapo: '마포구',
  Seodaemun: '서대문구',
  Seocho: '서초구',
  Seongdong: '성동구',
  Seongbuk: '성북구',
  Songpa: '송파구',
  Yangcheon: '양천구',
  Yeongdeungpo: '영등포구',
  Yongsan: '용산구',
  Eunpyeong: '은평구',
  Jongno: '종로구',
  Jung: '중구',
  Jungnang: '중랑구',
}

/* ============================================
   숙소 유형
   ============================================ */
export const ROOM_TYPES = [
  { value: 'Entire home/apt', labelKo: '집 전체', labelEn: 'Entire home/apt' },
  { value: 'Private room', labelKo: '개인실', labelEn: 'Private room' },
  { value: 'Shared room', labelKo: '공유실', labelEn: 'Shared room' },
  { value: 'Hotel room', labelKo: '호텔 객실', labelEn: 'Hotel room' },
] as const

/* ============================================
   2025년 대한민국 공휴일 (월별 날짜 Set)
   ============================================ */
export const HOLIDAYS_2025: Record<number, Set<number>> = {
  1: new Set([1]),      // 신정
  2: new Set([28, 29]), // 설날 연휴 (보완 필요 - 실제 날짜 기준)
  3: new Set([1]),      // 삼일절
  4: new Set([]),
  5: new Set([5, 6]),   // 어린이날, 대체공휴일
  6: new Set([6]),      // 현충일
  7: new Set([]),
  8: new Set([15]),     // 광복절
  9: new Set([18, 19, 22]), // 추석 연휴
  10: new Set([3, 9]),  // 개천절, 한글날
  11: new Set([]),
  12: new Set([25]),    // 크리스마스
}

/* ============================================
   편의시설 목록
   ============================================ */
export const AMENITIES = [
  { value: 'wifi', labelKo: 'Wi-Fi', labelEn: 'Wi-Fi' },
  { value: 'kitchen', labelKo: '주방', labelEn: 'Kitchen' },
  { value: 'washer', labelKo: '세탁기', labelEn: 'Washer' },
  { value: 'dryer', labelKo: '건조기', labelEn: 'Dryer' },
  { value: 'air_conditioning', labelKo: '에어컨', labelEn: 'Air Conditioning' },
  { value: 'heating', labelKo: '난방', labelEn: 'Heating' },
  { value: 'parking', labelKo: '주차', labelEn: 'Parking' },
  { value: 'pool', labelKo: '수영장', labelEn: 'Pool' },
  { value: 'gym', labelKo: '헬스장', labelEn: 'Gym' },
  { value: 'tv', labelKo: 'TV', labelEn: 'TV' },
  { value: 'elevator', labelKo: '엘리베이터', labelEn: 'Elevator' },
  { value: 'hot_tub', labelKo: '욕조', labelEn: 'Hot Tub' },
  { value: 'bbq', labelKo: 'BBQ', labelEn: 'BBQ' },
  { value: 'balcony', labelKo: '발코니', labelEn: 'Balcony' },
  { value: 'workspace', labelKo: '작업 공간', labelEn: 'Workspace' },
] as const

/* ============================================
   지원 언어
   ============================================ */
export const SUPPORTED_LANGUAGES: LanguageOption[] = [
  { code: 'ko', label: '한국어', region: '대한민국', flag: '🇰🇷' },
  { code: 'en', label: 'English', region: 'United States', flag: '🇺🇸' },
  { code: 'ja', label: '日本語', region: '日本', flag: '🇯🇵' },
  { code: 'zh', label: '中文', region: '中国大陆', flag: '🇨🇳' },
  { code: 'es', label: 'Español', region: 'España', flag: '🇪🇸' },
  { code: 'de', label: 'Deutsch', region: 'Deutschland', flag: '🇩🇪' },
  { code: 'fr', label: 'Français', region: 'France', flag: '🇫🇷' },
]

/* ============================================
   지원 통화
   ============================================ */
export const SUPPORTED_CURRENCIES: CurrencyOption[] = [
  { code: 'KRW', symbol: '₩', name: '대한민국 원', locale: 'ko-KR' },
  { code: 'USD', symbol: '$', name: '미국 달러', locale: 'en-US' },
  { code: 'EUR', symbol: '€', name: '유로', locale: 'de-DE' },
  { code: 'JPY', symbol: '¥', name: '일본 엔', locale: 'ja-JP' },
  { code: 'CNY', symbol: '¥', name: '중국 위안', locale: 'zh-CN' },
  { code: 'GBP', symbol: '£', name: '영국 파운드', locale: 'en-GB' },
  { code: 'SGD', symbol: 'S$', name: '싱가포르 달러', locale: 'en-SG' },
  { code: 'AUD', symbol: 'A$', name: '호주 달러', locale: 'en-AU' },
]

/* ============================================
   환율 기준 (KRW 기준 대략적 환산)
   실제 서비스에서는 실시간 API 사용 권장
   ============================================ */
export const EXCHANGE_RATES: Record<string, number> = {
  KRW: 1,
  USD: 0.00074,
  EUR: 0.00068,
  JPY: 0.11,
  CNY: 0.0054,
  GBP: 0.00058,
  SGD: 0.00099,
  AUD: 0.00113,
}

/* ============================================
   사이드바 네비게이션 항목
   ============================================ */
export const NAV_SECTIONS = [
  { id: 'wizard', labelKey: 'sidebar.inputSettings', icon: 'Settings' },
  { id: 'revenue', labelKey: 'sidebar.revenueSummary', icon: 'TrendingUp' },
  { id: 'pricing', labelKey: 'sidebar.pricingStrategy', icon: 'DollarSign' },
  { id: 'market', labelKey: 'sidebar.marketDiagnosis', icon: 'Map' },
  { id: 'health', labelKey: 'sidebar.healthScore', icon: 'Activity' },
  { id: 'poi', labelKey: 'sidebar.nearbyPOI', icon: 'MapPin' },
  { id: 'description', labelKey: 'sidebar.listingDesc', icon: 'FileText' },
] as const

/* ============================================
   마법사 단계 정의
   ============================================ */
export const WIZARD_STEPS = [
  { step: 1, labelKey: 'wizard.step1.title', icon: 'Home' },
  { step: 2, labelKey: 'wizard.step2.title', icon: 'Calendar' },
  { step: 3, labelKey: 'wizard.step3.title', icon: 'Receipt' },
  { step: 4, labelKey: 'wizard.step4.title', icon: 'Settings2' },
] as const

/* ============================================
   API 엔드포인트
   ============================================ */
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'
