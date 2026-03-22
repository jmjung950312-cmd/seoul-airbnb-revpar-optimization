/* Step 3: 운영비 입력 */

'use client'

import { useTranslations } from 'next-intl'
import { Input } from '@/components/ui/input'
import { useWizardStore } from '@/store/wizardStore'
import { useLocaleStore } from '@/store/localeStore'
import { cn } from '@/lib/utils'

export function Step3OpEx() {
  const t = useTranslations('wizard.step3')
  const { step3, updateStep3 } = useWizardStore()
  const { currency } = useLocaleStore()

  const currencySymbol = currency === 'KRW' ? '₩' : currency === 'USD' ? '$' : currency

  return (
    <div className="grid grid-cols-2 gap-4">
      <CostField
        label={t('cleaningFee')}
        value={step3.cleaningFee}
        prefix={currencySymbol}
        onChange={v => updateStep3({ cleaningFee: v })}
        hint={t('cleaningFeeHint')}
      />

      <CostField
        label={t('platformFee')}
        value={step3.platformFee * 100}
        suffix="%"
        onChange={v => updateStep3({ platformFee: v / 100 })}
        hint={t('platformFeeHint')}
        step={0.5}
        min={0}
        max={20}
      />

      <CostField
        label={t('utilityMonthly')}
        value={step3.utilityMonthly}
        prefix={currencySymbol}
        onChange={v => updateStep3({ utilityMonthly: v })}
        hint={t('utilityHint')}
      />

      <CostField
        label={t('mortgageMonthly')}
        value={step3.mortgageMonthly}
        prefix={currencySymbol}
        onChange={v => updateStep3({ mortgageMonthly: v })}
        hint={t('mortgageHint')}
      />

      <CostField
        label={t('managementFee')}
        value={step3.managementFee}
        prefix={currencySymbol}
        onChange={v => updateStep3({ managementFee: v })}
        hint={t('managementHint')}
      />

      <CostField
        label={t('otherOpEx')}
        value={step3.otherOpEx}
        prefix={currencySymbol}
        onChange={v => updateStep3({ otherOpEx: v })}
        hint={t('otherHint')}
      />

      {/* 월 총 고정비 미리보기 */}
      <div className="col-span-2 mt-2 p-4 bg-[#F7F7F7] dark:bg-[#2C2C2E] rounded-xl border border-[#EBEBEB] dark:border-[#3A3A3C]">
        <p className="text-xs font-semibold text-[#767676] uppercase tracking-wide mb-2">
          {t('monthlyTotal')}
        </p>
        <p className="text-xl font-bold text-[#222222] dark:text-[#F5F5F5]">
          {currencySymbol}
          {(
            step3.utilityMonthly +
            step3.mortgageMonthly +
            step3.managementFee +
            step3.otherOpEx
          ).toLocaleString()}
        </p>
      </div>
    </div>
  )
}

/* ============================================
   비용 입력 필드
   ============================================ */
function CostField({
  label,
  value,
  prefix,
  suffix,
  onChange,
  hint,
  step = 1000,
  min = 0,
  max = 10000000,
}: {
  label: string
  value: number
  prefix?: string
  suffix?: string
  onChange: (v: number) => void
  hint?: string
  step?: number
  min?: number
  max?: number
}) {
  return (
    <div className="space-y-1.5">
      <label className="block text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
        {label}
      </label>
      {hint && <p className="text-xs text-[#767676]">{hint}</p>}
      <div className="relative">
        {prefix && (
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-sm text-[#767676] font-medium">
            {prefix}
          </span>
        )}
        <input
          type="number"
          value={value}
          min={min}
          max={max}
          step={step}
          onChange={e => onChange(Number(e.target.value))}
          className={cn(
            'w-full h-12 border border-[#DDDDDD] dark:border-[#3A3A3C] rounded-lg bg-white dark:bg-[#2C2C2E]',
            'text-[#222222] dark:text-[#F5F5F5] focus:outline-none focus:ring-2 focus:ring-[#FF385C] focus:border-transparent text-sm',
            prefix ? 'pl-8 pr-3' : suffix ? 'pl-3 pr-8' : 'px-3',
          )}
        />
        {suffix && (
          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-[#767676] font-medium">
            {suffix}
          </span>
        )}
      </div>
    </div>
  )
}
