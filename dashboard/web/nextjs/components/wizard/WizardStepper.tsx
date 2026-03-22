/* 수직 스텝퍼 - 마법사 진행 단계 표시 */

'use client'

import { useTranslations } from 'next-intl'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

interface WizardStepperProps {
  currentStep: number
  totalSteps?: number
}

export function WizardStepper({ currentStep, totalSteps = 4 }: WizardStepperProps) {
  const t = useTranslations('wizard')

  const stepLabels = [
    t('step1.title'),
    t('step2.title'),
    t('step3.title'),
    t('step4.title'),
  ]

  return (
    <div className="flex items-center gap-2 mb-6">
      {Array.from({ length: totalSteps }, (_, i) => i + 1).map((step, idx) => {
        const isCompleted = step < currentStep
        const isCurrent = step === currentStep

        return (
          <div key={step} className="flex items-center gap-2">
            {/* 스텝 원 */}
            <div className="flex items-center gap-2">
              <div
                className={cn(
                  'w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold flex-shrink-0 transition-all',
                  isCompleted && 'bg-[#222222] dark:bg-white text-white dark:text-[#222222]',
                  isCurrent && 'bg-[#FF385C] text-white ring-4 ring-[#FF385C]/20',
                  !isCompleted && !isCurrent && 'bg-[#EBEBEB] dark:bg-[#3A3A3C] text-[#767676]',
                )}
              >
                {isCompleted ? <Check size={12} /> : step}
              </div>
              <span
                className={cn(
                  'text-sm hidden sm:block',
                  isCurrent && 'font-semibold text-[#222222] dark:text-[#F5F5F5]',
                  isCompleted && 'text-[#484848] dark:text-[#EBEBEB]',
                  !isCompleted && !isCurrent && 'text-[#767676]',
                )}
              >
                {stepLabels[idx]}
              </span>
            </div>

            {/* 연결선 */}
            {idx < totalSteps - 1 && (
              <div
                className={cn(
                  'h-0.5 w-8 sm:w-12 rounded-full transition-colors',
                  step < currentStep ? 'bg-[#222222] dark:bg-white' : 'bg-[#EBEBEB] dark:bg-[#3A3A3C]',
                )}
              />
            )}
          </div>
        )
      })}
    </div>
  )
}
