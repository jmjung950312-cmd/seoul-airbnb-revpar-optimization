/* 수익 요약 섹션 */

'use client'

import { useTranslations } from 'next-intl'
import { SectionCard } from '@/components/common/SectionCard'
import { OccupancyLineChart } from '@/components/charts/OccupancyLineChart'
import { useResultsStore } from '@/store/resultsStore'
import { useLocaleStore } from '@/store/localeStore'
import { formatCurrency } from '@/lib/utils'

export function RevenueSummarySection() {
  const t = useTranslations('dashboard.revenueSummary')
  const tCal = useTranslations('calendar')
  const { results } = useResultsStore()
  const { currency } = useLocaleStore()

  if (!results) return null

  const { predict, benchmark } = results

  /* 로케일에 맞는 월 이름 배열 */
  const months = Array.from({ length: 12 }, (_, i) => tCal(`months.${i}`))

  /* 월별 차트 데이터 (예측 기반 시뮬레이션) */
  const chartData = months.map((month, idx) => {
    /* 계절성 패턴 적용 */
    const seasonalFactor = [0.75, 0.78, 0.85, 0.90, 0.92, 0.95, 1.0, 1.05, 0.95, 0.90, 0.82, 0.88][idx]
    return {
      month,
      myOccupancy: predict.occ_pred * seasonalFactor,
      marketMedian: benchmark.occ_median * seasonalFactor * 0.95,
    }
  })

  /* 비교 데이터 */
  const comparisonItems = [
    {
      label: t('adr'),
      mine: formatCurrency(predict.adr_pred, currency),
      median: formatCurrency(benchmark.adr_median, currency),
      top25: formatCurrency(benchmark.adr_p75, currency),
    },
    {
      label: t('occupancy'),
      mine: `${(predict.occ_pred * 100).toFixed(1)}%`,
      median: `${(benchmark.occ_median * 100).toFixed(1)}%`,
      top25: `${(benchmark.occ_p75 * 100).toFixed(1)}%`,
    },
    {
      label: t('revpar'),
      mine: formatCurrency(predict.revpar_pred, currency),
      median: formatCurrency(benchmark.revpar_median, currency),
      top25: formatCurrency(benchmark.revpar_median * 1.35, currency),
    },
  ]

  return (
    <SectionCard id="revenue" title={t('title')}>
      {/* 상단 주요 지표 */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <MetricBox
          label={t('monthlyRevenue')}
          value={formatCurrency(predict.monthly_revenue, currency)}
          color="rausch"
        />
        <MetricBox
          label={t('monthlyNetProfit')}
          value={formatCurrency(predict.monthly_net_profit, currency)}
          color="babu"
        />
        <MetricBox
          label={t('annualRevenue')}
          value={formatCurrency(predict.monthly_revenue * 12, currency, true)}
          color="default"
        />
      </div>

      {/* 예약률 라인 차트 */}
      <div className="mb-8">
        <p className="text-sm font-medium text-[#484848] dark:text-[#EBEBEB] mb-4">
          {t('monthlyOccupancyTrend')}
        </p>
        <OccupancyLineChart data={chartData} />
      </div>

      {/* 유사 숙소 비교 테이블 */}
      <div>
        <p className="text-sm font-semibold text-[#484848] dark:text-[#EBEBEB] mb-3">
          {t('comparisonTitle')}
        </p>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-[#EBEBEB] dark:border-[#3A3A3C]">
                <th className="text-left py-2 text-xs text-[#767676] font-medium">{t('metric')}</th>
                <th className="text-right py-2 text-xs text-[#767676] font-medium">{t('yourProperty')}</th>
                <th className="text-right py-2 text-xs text-[#767676] font-medium">{t('median')}</th>
                <th className="text-right py-2 text-xs text-[#767676] font-medium">{t('top25')}</th>
              </tr>
            </thead>
            <tbody>
              {comparisonItems.map(item => (
                <tr key={item.label} className="border-b border-[#EBEBEB] dark:border-[#3A3A3C] last:border-0">
                  <td className="py-3 text-[#484848] dark:text-[#EBEBEB]">{item.label}</td>
                  <td className="py-3 text-right font-semibold text-[#FF385C]">{item.mine}</td>
                  <td className="py-3 text-right text-[#484848] dark:text-[#EBEBEB]">{item.median}</td>
                  <td className="py-3 text-right text-[#00A699]">{item.top25}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </SectionCard>
  )
}

/* ============================================
   지표 박스
   ============================================ */
function MetricBox({
  label,
  value,
  color,
}: {
  label: string
  value: string
  color: 'rausch' | 'babu' | 'default'
}) {
  const colorMap = {
    rausch: 'text-[#FF385C]',
    babu: 'text-[#00A699]',
    default: 'text-[#222222] dark:text-[#F5F5F5]',
  }

  return (
    <div className="bg-[#F7F7F7] dark:bg-[#3A3A3C] rounded-xl p-4">
      <p className="text-xs text-[#767676] mb-1">{label}</p>
      <p className={`text-xl font-bold ${colorMap[color]}`}>{value}</p>
    </div>
  )
}
