/* 헬스 스코어 섹션 */

'use client'

import { useTranslations } from 'next-intl'
import { SectionCard } from '@/components/common/SectionCard'
import { HealthScoreRadar } from '@/components/charts/HealthScoreRadar'
import { useResultsStore } from '@/store/resultsStore'
import { cn } from '@/lib/utils'

const GRADE_CONFIG = {
  A: { color: 'text-[#00A699]', bg: 'bg-[#F0FBF9]', border: 'border-[#00A699]/30' },
  B: { color: 'text-[#3B82F6]', bg: 'bg-[#EFF6FF]', border: 'border-[#3B82F6]/30' },
  C: { color: 'text-[#F59E0B]', bg: 'bg-[#FFFBEB]', border: 'border-[#F59E0B]/30' },
  D: { color: 'text-[#EF4444]', bg: 'bg-[#FEF2F2]', border: 'border-[#EF4444]/30' },
}

export function HealthScoreSection() {
  const t = useTranslations('dashboard.healthScore')
  const { results } = useResultsStore()

  if (!results) return null

  const { healthScore } = results
  const gradeConfig = GRADE_CONFIG[healthScore.grade]

  return (
    <SectionCard id="health" title={t('title')}>
      <div className="flex flex-col lg:flex-row gap-8">
        {/* 좌측: 종합 점수 + 등급 */}
        <div className="flex flex-col items-center lg:w-64">
          <div
            className={cn(
              'w-32 h-32 rounded-full flex flex-col items-center justify-center border-4 mb-4',
              gradeConfig.bg,
              gradeConfig.border,
            )}
          >
            <span className={cn('text-4xl font-bold', gradeConfig.color)}>
              {healthScore.grade}
            </span>
            <span className="text-sm text-[#767676] mt-0.5">{t('grade')}</span>
          </div>

          <p className="text-3xl font-bold text-[#222222] dark:text-[#F5F5F5] mb-1">
            {healthScore.composite}점
          </p>
          <p className="text-sm text-[#767676]">{t('composite')} / 100</p>

          {/* 개선 액션 */}
          {healthScore.top_actions.length > 0 && (
            <div className="mt-6 w-full">
              <p className="text-sm font-semibold text-[#484848] dark:text-[#EBEBEB] mb-2">
                {t('topActions')}
              </p>
              <div className="space-y-2">
                {healthScore.top_actions.slice(0, 3).map((action, idx) => (
                  <div
                    key={idx}
                    className="flex items-start gap-2 text-xs text-[#484848] dark:text-[#EBEBEB] bg-[#F7F7F7] dark:bg-[#3A3A3C] rounded-lg p-2.5"
                  >
                    <span className="text-[#FF385C] font-bold mt-0.5 flex-shrink-0">
                      {idx + 1}.
                    </span>
                    <span>{action}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* 우측: 레이더 차트 + 항목별 점수 */}
        <div className="flex-1">
          <p className="text-sm font-medium text-[#484848] dark:text-[#EBEBEB] mb-3">
            {t('components')}
          </p>
          <HealthScoreRadar data={healthScore.components} />

          {/* 항목별 바 */}
          <div className="mt-4 space-y-3">
            {healthScore.components.map(comp => {
              const pct = Math.round((comp.score / comp.max_score) * 100)
              const barColor = pct >= 80 ? '#00A699' : pct >= 60 ? '#3B82F6' : pct >= 40 ? '#F59E0B' : '#EF4444'

              return (
                <div key={comp.name}>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-[#484848] dark:text-[#EBEBEB]">{comp.name}</span>
                    <span className="font-medium" style={{ color: barColor }}>
                      {comp.score}/{comp.max_score}점
                    </span>
                  </div>
                  <div className="h-1.5 bg-[#EBEBEB] dark:bg-[#3A3A3C] rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{ width: `${pct}%`, backgroundColor: barColor }}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </SectionCard>
  )
}
