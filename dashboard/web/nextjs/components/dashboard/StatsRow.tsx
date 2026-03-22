/* 에어비앤비 Performance 상단 KPI 행 */

'use client'

import { useTranslations } from 'next-intl'
import { KpiStat } from '@/components/common/KpiStat'
import { useResultsStore } from '@/store/resultsStore'
import { useLocaleStore } from '@/store/localeStore'
import { formatCurrency } from '@/lib/utils'

export function StatsRow() {
  const t = useTranslations('stats')
  const { results } = useResultsStore()
  const { currency } = useLocaleStore()

  if (!results) return null

  const { predict } = results

  return (
    <div className="bg-white dark:bg-[#1C1C1E] border-b border-[#DDDDDD] dark:border-[#3A3A3C] px-4 sm:px-6 py-4 sm:py-5 overflow-x-auto">
      <div className="flex items-start gap-0 min-w-[560px] sm:min-w-0 sm:grid sm:grid-cols-3 lg:grid-cols-5">
        {[
          { label: t('dailyRevPAR'), value: formatCurrency(predict.revpar_pred, currency), highlight: true },
          { label: t('monthlyNetProfit'), value: formatCurrency(predict.monthly_net_profit, currency), trend: 5.2 },
          { label: t('bepRate'), value: formatCurrency(predict.bep_rate, currency) },
          { label: t('weekdayOcc'), value: `${(predict.weekday_occ * 100).toFixed(1)}%` },
          { label: t('weekendOcc'), value: `${(predict.weekend_occ * 100).toFixed(1)}%` },
        ].map((item, idx) => (
          <div
            key={item.label}
            className={`flex-1 px-4 sm:px-5 ${idx > 0 ? 'border-l border-[#DDDDDD] dark:border-[#3A3A3C]' : ''}`}
          >
            <KpiStat
              label={item.label}
              value={item.value}
              highlight={item.highlight}
              trend={item.trend}
            />
          </div>
        ))}
      </div>
    </div>
  )
}
