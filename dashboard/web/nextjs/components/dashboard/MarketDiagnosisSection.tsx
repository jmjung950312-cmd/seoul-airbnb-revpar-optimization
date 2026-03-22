/* 지역 진단 섹션 */

'use client'

import { useTranslations } from 'next-intl'
import { SectionCard } from '@/components/common/SectionCard'
import { useResultsStore } from '@/store/resultsStore'
import { useLocaleStore } from '@/store/localeStore'
import { formatCurrency } from '@/lib/utils'
import { DISTRICTS_KR } from '@/lib/constants'
import { useWizardStore } from '@/store/wizardStore'

export function MarketDiagnosisSection() {
  const t = useTranslations('dashboard.marketDiagnosis')
  const { results } = useResultsStore()
  const { currency } = useLocaleStore()
  const { step1 } = useWizardStore()

  if (!results) return null

  const { predict, benchmark } = results
  const districtKo = DISTRICTS_KR[step1.district] ?? step1.district

  /* 경쟁 수준 (퍼센타일 기반) */
  const competitionLevel =
    predict.percentile_rank > 75 ? '높음' :
    predict.percentile_rank > 50 ? '보통' :
    predict.percentile_rank > 25 ? '낮음' : '매우 낮음'

  const competitionColor =
    predict.percentile_rank > 75 ? 'text-[#EF4444]' :
    predict.percentile_rank > 50 ? 'text-[#F59E0B]' :
    'text-[#00A699]'

  /* 클러스터 라벨 */
  const clusterLabel = predict.cluster_label || `클러스터 ${predict.cluster_id}`

  return (
    <SectionCard id="market" title={t('title')}>
      {/* 자치구 + 클러스터 정보 */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <InfoBox
          label="분석 자치구"
          value={districtKo}
          sub={step1.district}
        />
        <InfoBox
          label={t('clusterInfo')}
          value={clusterLabel}
          sub={`클러스터 ID: ${predict.cluster_id}`}
        />
      </div>

      {/* 시장 지표 */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
        <MarketMetric
          label={t('avgAdr')}
          value={formatCurrency(benchmark.adr_median, currency)}
        />
        <MarketMetric
          label={t('avgOccupancy')}
          value={`${(benchmark.occ_median * 100).toFixed(1)}%`}
        />
        <MarketMetric
          label={t('competitionLevel')}
          value={competitionLevel}
          valueClass={competitionColor}
        />
        <MarketMetric
          label="내 퍼센타일"
          value={`상위 ${predict.percentile_rank.toFixed(0)}%`}
          valueClass="text-[#FF385C]"
        />
      </div>

      {/* 샘플 규모 */}
      <div className="bg-[#F7F7F7] dark:bg-[#3A3A3C] rounded-xl p-4 text-sm text-[#767676]">
        <span className="font-medium text-[#484848] dark:text-[#EBEBEB]">{districtKo}</span> 내
        유사 숙소 <span className="font-semibold text-[#222222] dark:text-[#F5F5F5]">{benchmark.sample_size.toLocaleString()}</span>개 기준 분석
      </div>
    </SectionCard>
  )
}

function InfoBox({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="bg-[#F7F7F7] dark:bg-[#3A3A3C] rounded-xl p-4">
      <p className="text-xs text-[#767676] mb-1">{label}</p>
      <p className="text-base font-semibold text-[#222222] dark:text-[#F5F5F5]">{value}</p>
      {sub && <p className="text-xs text-[#767676] mt-0.5">{sub}</p>}
    </div>
  )
}

function MarketMetric({
  label,
  value,
  valueClass,
}: {
  label: string
  value: string
  valueClass?: string
}) {
  return (
    <div className="text-center">
      <p className="text-xs text-[#767676] mb-1">{label}</p>
      <p className={`text-lg font-bold ${valueClass ?? 'text-[#222222] dark:text-[#F5F5F5]'}`}>
        {value}
      </p>
    </div>
  )
}
