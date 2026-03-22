/* Step 2 (기존 호스트): 실제 예약 현황 + 달력 */

'use client'

import { useTranslations } from 'next-intl'
import { Slider } from '@/components/ui/slider'
import { Switch } from '@/components/ui/switch'
import { AirbnbCalendar } from '@/components/calendar/AirbnbCalendar'
import { useWizardStore } from '@/store/wizardStore'
import { formatCurrency } from '@/lib/utils'
import { useLocaleStore } from '@/store/localeStore'

export function Step2Existing() {
  const t = useTranslations('wizard.step2')
  const tCommon = useTranslations('common')
  const {
    step2Existing,
    toggleBookedDay,
    setCalendarMonth,
    updateStep2Existing,
  } = useWizardStore()
  const { currency } = useLocaleStore()

  return (
    <div className="space-y-6">
      <p className="text-sm text-[#767676]">{t('forExisting')}</p>

      {/* 에어비앤비 달력 */}
      <div>
        <p className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5] mb-3">
          {t('calendarTitle')}
        </p>
        <AirbnbCalendar
          year={step2Existing.selectedYear}
          month={step2Existing.selectedMonth}
          bookedDays={step2Existing.bookedDays}
          onDayToggle={toggleBookedDay}
          onMonthChange={setCalendarMonth}
        />
      </div>

      {/* 현재 ADR */}
      <div className="space-y-3">
        <div className="flex justify-between">
          <label className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
            {t('currentAdr')}
          </label>
          <span className="text-sm font-medium text-[#FF385C]">
            {formatCurrency(step2Existing.currentAdr, currency)}
          </span>
        </div>
        <Slider
          min={20000}
          max={500000}
          step={5000}
          value={[step2Existing.currentAdr]}
          onValueChange={([v]) => updateStep2Existing({ currentAdr: v })}
          className="[&_[role=slider]]:border-[#FF385C] [&_[role=slider]]:bg-[#FF385C]"
        />
      </div>

      {/* 리뷰 점수 */}
      <div className="space-y-3">
        <div className="flex justify-between">
          <label className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
            {t('reviewScore')}
          </label>
          <span className="text-sm font-medium text-[#484848] dark:text-[#EBEBEB]">
            ⭐ {step2Existing.reviewScore.toFixed(1)}
          </span>
        </div>
        <Slider
          min={1}
          max={5}
          step={0.1}
          value={[step2Existing.reviewScore]}
          onValueChange={([v]) => updateStep2Existing({ reviewScore: v })}
        />
      </div>

      {/* 리뷰 수 */}
      <div className="space-y-3">
        <div className="flex justify-between">
          <label className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
            {t('reviewCount')}
          </label>
          <span className="text-sm font-medium text-[#484848] dark:text-[#EBEBEB]">
            {step2Existing.reviewCount}{tCommon('bathroom')}
          </span>
        </div>
        <Slider
          min={0}
          max={500}
          step={5}
          value={[step2Existing.reviewCount]}
          onValueChange={([v]) => updateStep2Existing({ reviewCount: v })}
        />
      </div>

      {/* 사진 수 */}
      <div className="space-y-3">
        <div className="flex justify-between">
          <label className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
            {t('photos')}
          </label>
          <span className="text-sm font-medium text-[#484848] dark:text-[#EBEBEB]">
            {step2Existing.photos}{tCommon('photo')}
          </span>
        </div>
        <Slider
          min={1}
          max={50}
          step={1}
          value={[step2Existing.photos]}
          onValueChange={([v]) => updateStep2Existing({ photos: v })}
        />
      </div>

      {/* 응답률 */}
      <div className="space-y-3">
        <div className="flex justify-between">
          <label className="text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
            {t('responseRate')}
          </label>
          <span className="text-sm font-medium text-[#484848] dark:text-[#EBEBEB]">
            {(step2Existing.responseRate * 100).toFixed(0)}%
          </span>
        </div>
        <Slider
          min={0}
          max={1}
          step={0.01}
          value={[step2Existing.responseRate]}
          onValueChange={([v]) => updateStep2Existing({ responseRate: v })}
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
          checked={step2Existing.instantBook}
          onCheckedChange={v => updateStep2Existing({ instantBook: v })}
          className="data-[state=checked]:bg-[#FF385C]"
        />
      </div>
    </div>
  )
}
