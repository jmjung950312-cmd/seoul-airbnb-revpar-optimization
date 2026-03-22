/* 대시보드 메인 페이지 */

'use client'

import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { StatsRow } from '@/components/dashboard/StatsRow'
import { WizardContainer } from '@/components/wizard/WizardContainer'
import { RevenueSummarySection } from '@/components/dashboard/RevenueSummarySection'
import { PricingStrategySection } from '@/components/dashboard/PricingStrategySection'
import { MarketDiagnosisSection } from '@/components/dashboard/MarketDiagnosisSection'
import { HealthScoreSection } from '@/components/dashboard/HealthScoreSection'
import { NearbyPOISection } from '@/components/dashboard/NearbyPOISection'
import { ListingDescSection } from '@/components/dashboard/ListingDescSection'
import { useResultsStore } from '@/store/resultsStore'
import { Loader2 } from 'lucide-react'

/* 섹션 ID → 렌더링할 컴포넌트 매핑 */
const SECTION_MAP: Record<string, React.ReactNode> = {
  revenue: <RevenueSummarySection />,
  pricing: <PricingStrategySection />,
  market: <><MarketDiagnosisSection /><NearbyPOISection /></>,
  'market-diagnosis': <MarketDiagnosisSection />,
  poi: <NearbyPOISection />,
  health: <HealthScoreSection />,
  description: <ListingDescSection />,
}

export default function DashboardPage() {
  const { results, isLoading, error, activeSection } = useResultsStore()

  /* 결과가 없거나 wizard 탭이면 마법사 표시 */
  const showWizard = !results || activeSection === 'wizard'

  return (
    <DashboardLayout>
      {/* KPI 행 (결과 있을 때만) */}
      <StatsRow />

      {/* 메인 콘텐츠 */}
      <div className="p-4">
        {/* 로딩 상태 */}
        {isLoading && (
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <Loader2 size={40} className="animate-spin text-[#FF385C]" />
            <p className="text-sm text-[#767676]">AI가 분석 중입니다...</p>
          </div>
        )}

        {/* 오류 상태 */}
        {error && !isLoading && (
          <div className="bg-[#FFF1F2] dark:bg-[#3A1A1E] border border-[#FF385C]/20 rounded-xl p-5">
            <p className="text-sm font-semibold text-[#FF385C]">분석 오류</p>
            <p className="text-sm text-[#767676] mt-1">{error}</p>
          </div>
        )}

        {/* 마법사: 결과 없거나 wizard 탭일 때만 표시 */}
        {!isLoading && showWizard && <WizardContainer />}

        {/* 결과 섹션: 탭 기반 단일 섹션 렌더링 */}
        {results && !isLoading && !showWizard && (
          SECTION_MAP[activeSection] ?? <RevenueSummarySection />
        )}
      </div>
    </DashboardLayout>
  )
}
