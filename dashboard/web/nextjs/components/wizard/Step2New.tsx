/* Step 2 (신규 호스트): 목표 설정 */

'use client'

import { useTranslations } from 'next-intl'
import { Slider } from '@/components/ui/slider'
import { Switch } from '@/components/ui/switch'
import { useWizardStore } from '@/store/wizardStore'
import { formatCurrency } from '@/lib/utils'
import { useLocaleStore } from '@/store/localeStore'

export function Step2New() {
  const t = useTranslations('wizard.step2')
  const tCommon = useTranslations('common')
  const { step2New, updateStep2New } = useWizardStore()
  const { currency } = useLocaleStore()

  return (
    <div className="space-y-6">
      <p className="text-sm text-[#767676]">{t('forNew')}</p>

      {/* 목표 ADR */}
      <div className="space-y-3">
        <div className="flex justify-between">
          <label className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
            {t('targetAdr')}
          </label>
          <span className="text-sm font-medium text-[#FF385C]">
            {formatCurrency(step2New.targetAdr, currency)}
          </span>
        </div>
        <Slider
          min={20000}
          max={500000}
          step={5000}
          value={[step2New.targetAdr]}
          onValueChange={([v]) => updateStep2New({ targetAdr: v })}
          className="[&_[role=slider]]:border-[#FF385C] [&_[role=slider]]:bg-[#FF385C]"
        />
        <div className="flex justify-between text-xs text-[#767676]">
          <span>{formatCurrency(20000, currency)}</span>
          <span>{formatCurrency(500000, currency)}</span>
        </div>
      </div>

      {/* 목표 예약률 */}
      <div className="space-y-3">
        <div className="flex justify-between">
          <label className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
            {t('targetOccupancy')}
          </label>
          <span className="text-sm font-medium text-[#FF385C]">
            {(step2New.targetOccupancy * 100).toFixed(0)}%
          </span>
        </div>
        <Slider
          min={0.1}
          max={1}
          step={0.01}
          value={[step2New.targetOccupancy]}
          onValueChange={([v]) => updateStep2New({ targetOccupancy: v })}
          className="[&_[role=slider]]:border-[#FF385C] [&_[role=slider]]:bg-[#FF385C]"
        />
        <div className="flex justify-between text-xs text-[#767676]">
          <span>10%</span>
          <span>100%</span>
        </div>
      </div>

      {/* 사진 수 */}
      <div className="space-y-3">
        <div className="flex justify-between">
          <label className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
            {t('photos')}
          </label>
          <span className="text-sm font-medium text-[#484848] dark:text-[#EBEBEB]">
            {step2New.photos}{tCommon('photo')}
          </span>
        </div>
        <Slider
          min={1}
          max={50}
          step={1}
          value={[step2New.photos]}
          onValueChange={([v]) => updateStep2New({ photos: v })}
        />
      </div>

      {/* 리뷰 점수 */}
      <div className="space-y-3">
        <div className="flex justify-between">
          <label className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
            {t('reviewScore')}
          </label>
          <span className="text-sm font-medium text-[#484848] dark:text-[#EBEBEB]">
            ⭐ {step2New.reviewScore.toFixed(1)}
          </span>
        </div>
        <Slider
          min={1}
          max={5}
          step={0.1}
          value={[step2New.reviewScore]}
          onValueChange={([v]) => updateStep2New({ reviewScore: v })}
        />
      </div>

      {/* 응답률 */}
      <div className="space-y-3">
        <div className="flex justify-between">
          <label className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
            {t('responseRate')}
          </label>
          <span className="text-sm font-medium text-[#484848] dark:text-[#EBEBEB]">
            {(step2New.responseRate * 100).toFixed(0)}%
          </span>
        </div>
        <Slider
          min={0}
          max={1}
          step={0.01}
          value={[step2New.responseRate]}
          onValueChange={([v]) => updateStep2New({ responseRate: v })}
        />
      </div>

      {/* 즉시 예약 */}
      <div className="flex items-center justify-between py-3 border-t border-[#EBEBEB] dark:border-[#3A3A3C]">
        <div>
          <p className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
            {t('instantBook')}
          </p>
          <p className="text-xs text-[#767676] mt-0.5">{tCommon('instantBookHint')}</p>
        </div>
        <Switch
          checked={step2New.instantBook}
          onCheckedChange={v => updateStep2New({ instantBook: v })}
          className="data-[state=checked]:bg-[#FF385C]"
        />
      </div>
    </div>
  )
}
