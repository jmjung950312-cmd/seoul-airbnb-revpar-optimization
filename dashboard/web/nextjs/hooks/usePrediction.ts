/* 예측 API 호출 훅 — FastAPI /analyze 연동 (Mock 폴백 포함) */

'use client'

import { useCallback } from 'react'
import { useWizardStore } from '@/store/wizardStore'
import { useResultsStore } from '@/store/resultsStore'
import { getMockResults } from '@/lib/apiClient'
import { calcOccupancyRate } from '@/lib/utils'
import { API_BASE_URL } from '@/lib/constants'
import type { DashboardResults } from '@/types/api'

/* FastAPI room_type 변환 */
function toApiRoomType(roomType: string): string {
  const map: Record<string, string> = {
    'Entire home/apt': 'entire_home',
    'Private room':   'private_room',
    'Shared room':    'shared_room',
    'Hotel room':     'hotel_room',
  }
  return map[roomType] ?? 'entire_home'
}

export function usePrediction() {
  const { step1, step2Existing, step2New, step3, step4 } = useWizardStore()
  const { setResults, setLoading, setError, setActiveSection } = useResultsStore()

  const runPrediction = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const isExisting = step1.hostType === 'existing'
      const bookedDays = isExisting ? step2Existing.bookedDays.size : undefined
      const rating = isExisting ? step2Existing.reviewScore : step2New.reviewScore
      const reviewCount = isExisting ? step2Existing.reviewCount : 0
      const photos = isExisting ? step2Existing.photos : step2New.photos
      const responseRate = isExisting ? step2Existing.responseRate : step2New.responseRate
      const instantBook = isExisting ? step2Existing.instantBook : step2New.instantBook

      /* 월 운영비 합산 */
      const opexMonthly =
        step3.utilityMonthly +
        step3.mortgageMonthly +
        step3.managementFee +
        step3.otherOpEx

      const body = {
        district: step1.district,
        room_type: toApiRoomType(step1.roomType),
        accommodates: step1.accommodates,
        bedrooms: step1.bedrooms,
        bathrooms: step1.bathrooms,
        review_scores_rating: rating,
        review_count: reviewCount,
        photos,
        response_rate: responseRate,
        instant_bookable: instantBook,
        min_nights: step4.minNights,
        host_type: step1.hostType ?? 'new',
        booked_days_count: bookedDays ?? null,
        opex_monthly: opexMonthly,
        cleaning_fee_per_stay: step3.cleaningFee,
        platform_fee_rate: step3.platformFee,
        superhost: false,
        target_adr: isExisting ? step2Existing.currentAdr : step2New.targetAdr,
      }

      let data: DashboardResults

      try {
        /* FastAPI 실제 호출 */
        const res = await fetch(`${API_BASE_URL}/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
          signal: AbortSignal.timeout(15000),
        })

        if (!res.ok) throw new Error(`API ${res.status}`)

        const raw = await res.json()

        /* FastAPI 응답 → DashboardResults 형식 변환 */
        data = {
          predict:            raw.predict,
          healthScore:        raw.health_score,
          benchmark:          raw.benchmark,
          pricingRec:         raw.pricing_rec,
          nearbyPOIs:         raw.nearby_pois,
          listingDescription: raw.listing_description,
        }
      } catch {
        /* API 연결 실패 시 Mock 폴백 */
        console.warn('[usePrediction] FastAPI 연결 실패 → Mock 데이터 사용')
        await new Promise(resolve => setTimeout(resolve, 800))
        data = getMockResults(step1.district)
      }

      setResults(data)
      setActiveSection('revenue')
    } catch (err) {
      const message = err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다'
      setError(message)
    }
  }, [step1, step2Existing, step2New, step3, step4, setResults, setLoading, setError, setActiveSection])

  return { runPrediction }
}
