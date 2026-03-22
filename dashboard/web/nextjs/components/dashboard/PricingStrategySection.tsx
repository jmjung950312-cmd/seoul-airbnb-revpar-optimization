/* 요금 전략 섹션 */

'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { SectionCard } from '@/components/common/SectionCard'
import { PriceSimChart } from '@/components/charts/PriceSimChart'
import { useResultsStore } from '@/store/resultsStore'
import { useLocaleStore } from '@/store/localeStore'
import { formatCurrency } from '@/lib/utils'

export function PricingStrategySection() {
  const t = useTranslations('dashboard.pricingStrategy')
  const { results } = useResultsStore()
  const { currency } = useLocaleStore()
  const [simPrice, setSimPrice] = useState<number | null>(null)

  if (!results) return null

  const { predict, pricingRec } = results
  const basePrice = predict.adr_pred

  /* 시뮬레이션 데이터 생성 */
  const priceRange = Array.from({ length: 20 }, (_, i) => {
    const price = basePrice * 0.5 + (basePrice * 1.5 * i) / 19
    /* 가격 탄력성 기반 수요 곡선 (단순화) */
    const demandFactor = Math.exp(-0.000003 * (price - basePrice))
    const occupancy = Math.min(0.99, predict.occ_pred * demandFactor)
    const revenue = price * occupancy * 30
    const fixedCosts = 200000 /* 월 고정비 가정 */
    const netProfit = revenue - fixedCosts - revenue * 0.03

    return { price: Math.round(price), revenue: Math.round(revenue), netProfit: Math.round(netProfit) }
  })

  const optimalPrice = pricingRec.weekday_price

  /* 계절별 조정 */
  const seasons = [
    { name: '봄 (3-5월)', factor: pricingRec.seasonal_adjustments['spring'] ?? 1.0 },
    { name: '여름 (6-8월)', factor: pricingRec.seasonal_adjustments['summer'] ?? 1.15 },
    { name: '가을 (9-11월)', factor: pricingRec.seasonal_adjustments['fall'] ?? 1.05 },
    { name: '겨울 (12-2월)', factor: pricingRec.seasonal_adjustments['winter'] ?? 0.85 },
  ]

  return (
    <SectionCard id="pricing" title={t('title')}>
      {/* 권장 요금 */}
      <div className="grid grid-cols-2 gap-4 mb-8">
        <div className="bg-[#FFF1F2] dark:bg-[#3A1A1E] rounded-xl p-4 border border-[#FF385C]/20">
          <p className="text-xs text-[#767676] mb-1">{t('weekdayPrice')}</p>
          <p className="text-2xl font-bold text-[#FF385C]">
            {formatCurrency(pricingRec.weekday_price, currency)}
          </p>
          <p className="text-xs text-[#767676] mt-1">시장 예측: {formatCurrency(basePrice, currency)}</p>
        </div>
        <div className="bg-[#F0FBF9] dark:bg-[#0D2B28] rounded-xl p-4 border border-[#00A699]/20">
          <p className="text-xs text-[#767676] mb-1">{t('weekendPrice')}</p>
          <p className="text-2xl font-bold text-[#00A699]">
            {formatCurrency(pricingRec.weekend_price, currency)}
          </p>
          <p className="text-xs text-[#767676] mt-1">
            성수기 x{pricingRec.peak_multiplier.toFixed(1)} 배율
          </p>
        </div>
      </div>

      {/* 요금 시뮬레이션 차트 */}
      <div className="mb-8">
        <p className="text-sm font-medium text-[#484848] dark:text-[#EBEBEB] mb-4">
          {t('simulationTitle')}
        </p>
        <PriceSimChart
          data={priceRange}
          currentPrice={basePrice}
          optimalPrice={optimalPrice}
          currency={currency}
        />
        <p className="text-xs text-[#767676] mt-2 text-center">
          ← 낮은 요금 · 붉은 점선: 최적 요금 · 회색 점선: 현재 요금 →
        </p>
      </div>

      {/* 계절별 조정 */}
      <div>
        <p className="text-sm font-semibold text-[#484848] dark:text-[#EBEBEB] mb-3">
          {t('seasonalAdjustment')}
        </p>
        <div className="space-y-2">
          {seasons.map(s => (
            <div key={s.name} className="flex items-center gap-3">
              <span className="text-sm text-[#484848] dark:text-[#EBEBEB] w-28 flex-shrink-0">
                {s.name}
              </span>
              <div className="flex-1 h-2 bg-[#EBEBEB] dark:bg-[#3A3A3C] rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all"
                  style={{
                    width: `${Math.min(100, s.factor * 80)}%`,
                    backgroundColor: s.factor >= 1 ? '#00A699' : '#FF385C',
                  }}
                />
              </div>
              <span
                className={`text-sm font-medium w-12 text-right ${s.factor >= 1 ? 'text-[#00A699]' : 'text-[#FF385C]'}`}
              >
                {s.factor >= 1 ? '+' : ''}{((s.factor - 1) * 100).toFixed(0)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </SectionCard>
  )
}
