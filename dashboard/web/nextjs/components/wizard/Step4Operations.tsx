/* Step 4: 운영 현황 설정 */

'use client'

import { useTranslations } from 'next-intl'
import { Minus, Plus } from 'lucide-react'
import { Switch } from '@/components/ui/switch'
import { useWizardStore } from '@/store/wizardStore'
import { cn } from '@/lib/utils'

export function Step4Operations() {
  const t = useTranslations('wizard.step4')
  const tCommon = useTranslations('common')
  const { step4, updateStep4 } = useWizardStore()

  /* 체크인 옵션 (시간대는 언어 무관, 마지막 옵션만 번역) */
  const checkInOptions = [
    { value: '13:00-20:00', label: '13:00 ~ 20:00' },
    { value: '15:00-22:00', label: '15:00 ~ 22:00' },
    { value: '16:00-23:00', label: '16:00 ~ 23:00' },
    { value: '자유', label: t('checkInFlexible') },
  ]

  return (
    <div className="space-y-6">
      {/* 최소/최대 숙박일 */}
      <div className="space-y-4">
        <NightCounter
          label={t('minNights')}
          value={step4.minNights}
          min={1}
          max={step4.maxNights}
          onChange={v => updateStep4({ minNights: v })}
          nightUnit={tCommon('night')}
        />
        <NightCounter
          label={t('maxNights')}
          value={step4.maxNights}
          min={step4.minNights}
          max={365}
          onChange={v => updateStep4({ maxNights: v })}
          nightUnit={tCommon('night')}
        />
      </div>

      {/* 체크인 시간 */}
      <div className="space-y-2">
        <label className="block text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
          {t('checkIn')}
        </label>
        <div className="grid grid-cols-2 gap-2">
          {checkInOptions.map(opt => (
            <button
              key={opt.value}
              type="button"
              onClick={() => updateStep4({ checkInWindow: opt.value })}
              className={cn(
                'py-2.5 px-3 rounded-lg border text-sm font-medium transition-all',
                step4.checkInWindow === opt.value
                  ? 'border-[#222222] dark:border-white bg-[#F7F7F7] dark:bg-[#3A3A3C]'
                  : 'border-[#DDDDDD] dark:border-[#3A3A3C] hover:border-[#767676]',
              )}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      {/* 토글 설정들 */}
      <div className="space-y-1 divide-y divide-[#EBEBEB] dark:divide-[#3A3A3C]">
        <ToggleRow
          label={t('selfCheckIn')}
          hint={t('selfCheckInHint')}
          checked={step4.selfCheckIn}
          onChange={v => updateStep4({ selfCheckIn: v })}
        />
        <ToggleRow
          label={t('petFriendly')}
          hint={t('petFriendlyHint')}
          checked={step4.petFriendly}
          onChange={v => updateStep4({ petFriendly: v })}
        />
        <ToggleRow
          label={t('smokingAllowed')}
          hint={t('smokingHint')}
          checked={step4.smokingAllowed}
          onChange={v => updateStep4({ smokingAllowed: v })}
        />
        <ToggleRow
          label={t('partiesAllowed')}
          hint={t('partiesHint')}
          checked={step4.partiesAllowed}
          onChange={v => updateStep4({ partiesAllowed: v })}
        />
      </div>
    </div>
  )
}

/* ============================================
   숙박일 카운터
   ============================================ */
function NightCounter({
  label,
  value,
  min,
  max,
  onChange,
  nightUnit,
}: {
  label: string
  value: number
  min: number
  max: number
  onChange: (v: number) => void
  nightUnit: string
}) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-[#EBEBEB] dark:border-[#3A3A3C]">
      <span className="text-sm font-medium text-[#222222] dark:text-[#F5F5F5]">{label}</span>
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={() => onChange(Math.max(min, value - 1))}
          disabled={value <= min}
          className="w-8 h-8 rounded-full border border-[#DDDDDD] dark:border-[#3A3A3C] flex items-center justify-center hover:border-[#222222] dark:hover:border-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          <Minus size={14} />
        </button>
        <span className="w-14 text-center text-sm font-medium">{value}{nightUnit}</span>
        <button
          type="button"
          onClick={() => onChange(Math.min(max, value + 1))}
          disabled={value >= max}
          className="w-8 h-8 rounded-full border border-[#DDDDDD] dark:border-[#3A3A3C] flex items-center justify-center hover:border-[#222222] dark:hover:border-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          <Plus size={14} />
        </button>
      </div>
    </div>
  )
}

/* ============================================
   토글 행
   ============================================ */
function ToggleRow({
  label,
  hint,
  checked,
  onChange,
}: {
  label: string
  hint?: string
  checked: boolean
  onChange: (v: boolean) => void
}) {
  return (
    <div className="flex items-center justify-between py-3">
      <div>
        <p className="text-sm font-medium text-[#222222] dark:text-[#F5F5F5]">{label}</p>
        {hint && <p className="text-xs text-[#767676] mt-0.5">{hint}</p>}
      </div>
      <Switch
        checked={checked}
        onCheckedChange={onChange}
        className="data-[state=checked]:bg-[#FF385C]"
      />
    </div>
  )
}
