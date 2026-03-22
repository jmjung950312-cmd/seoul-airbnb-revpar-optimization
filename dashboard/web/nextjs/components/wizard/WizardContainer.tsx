/* 마법사 전체 컨테이너: 단계별 렌더링 + 네비게이션 버튼 */

'use client'

import { useTranslations } from 'next-intl'
import { Loader2 } from 'lucide-react'
import { WizardStepper } from './WizardStepper'
import { Step1BasicInfo } from './Step1BasicInfo'
import { Step2New } from './Step2New'
import { Step2Existing } from './Step2Existing'
import { Step3OpEx } from './Step3OpEx'
import { Step4Operations } from './Step4Operations'
import { useWizardStore } from '@/store/wizardStore'
import { useResultsStore } from '@/store/resultsStore'
import { usePrediction } from '@/hooks/usePrediction'
import { SectionCard } from '@/components/common/SectionCard'
import { cn } from '@/lib/utils'

export function WizardContainer() {
  const t = useTranslations('wizard')
  const { currentStep, step1, setCurrentStep } = useWizardStore()
  const { isLoading } = useResultsStore()
  const { runPrediction } = usePrediction()

  const isExisting = step1.hostType === 'existing'

  /* 현재 단계의 유효성 검사 */
  const canProceed = () => {
    if (currentStep === 1) {
      return step1.hostType !== null && step1.district !== ''
    }
    return true
  }

  const handleNext = () => {
    if (currentStep < 4) setCurrentStep(currentStep + 1)
  }

  const handlePrev = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1)
  }

  const handleAnalyze = () => {
    runPrediction()
  }

  return (
    <SectionCard
      id="wizard"
      title={t('title')}
      className="w-full"
    >
      {/* 스텝퍼 */}
      <WizardStepper currentStep={currentStep} />

      {/* 단계별 컨텐츠 */}
      <div className="min-h-[400px]">
        {currentStep === 1 && <Step1BasicInfo />}
        {currentStep === 2 && (isExisting ? <Step2Existing /> : <Step2New />)}
        {currentStep === 3 && <Step3OpEx />}
        {currentStep === 4 && <Step4Operations />}
      </div>

      {/* 네비게이션 버튼 */}
      <div className="flex justify-between mt-8 pt-5 border-t border-[#EBEBEB] dark:border-[#3A3A3C]">
        <button
          type="button"
          onClick={handlePrev}
          disabled={currentStep === 1}
          className="px-5 py-2.5 rounded-lg border border-[#DDDDDD] dark:border-[#3A3A3C] text-sm font-medium text-[#484848] dark:text-[#EBEBEB] hover:border-[#222222] dark:hover:border-white disabled:opacity-40 disabled:cursor-not-allowed transition-all"
        >
          {t('prev')}
        </button>

        {currentStep < 4 ? (
          <button
            type="button"
            onClick={handleNext}
            disabled={!canProceed()}
            className={cn(
              'px-6 py-2.5 rounded-lg text-sm font-semibold transition-all',
              canProceed()
                ? 'bg-[#FF385C] text-white hover:bg-[#E31C5F] active:scale-95'
                : 'bg-[#DDDDDD] text-[#767676] cursor-not-allowed',
            )}
          >
            {t('next')}
          </button>
        ) : (
          <button
            type="button"
            onClick={handleAnalyze}
            disabled={isLoading}
            className="flex items-center gap-2 px-6 py-2.5 rounded-lg bg-[#FF385C] text-white text-sm font-semibold hover:bg-[#E31C5F] active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed transition-all"
          >
            {isLoading && <Loader2 size={16} className="animate-spin" />}
            {isLoading ? t('analyzing') : t('analyze')}
          </button>
        )}
      </div>
    </SectionCard>
  )
}
