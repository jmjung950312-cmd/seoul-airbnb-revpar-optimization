/* Step 1: 기본 정보 입력 */

'use client'

import { useTranslations, useLocale } from 'next-intl'
import { Minus, Plus } from 'lucide-react'
import { HostTypeSelector } from './HostTypeSelector'
import { useWizardStore } from '@/store/wizardStore'
import { DISTRICTS_KR, ROOM_TYPES, AMENITIES } from '@/lib/constants'
import { cn } from '@/lib/utils'
import type { HostType, RoomType } from '@/types/wizard'

export function Step1BasicInfo() {
  const t = useTranslations('wizard.step1')
  const tCommon = useTranslations('common')
  const locale = useLocale()
  const {
    step1,
    setHostType,
    setDistrict,
    setRoomType,
    setAccommodates,
    setBedrooms,
    setBathrooms,
    setAmenities,
  } = useWizardStore()

  const toggleAmenity = (value: string) => {
    const current = step1.amenities
    const updated = current.includes(value)
      ? current.filter(a => a !== value)
      : [...current, value]
    setAmenities(updated)
  }

  /* CJK 언어(한/일/중) 여부 확인 */
  const isCjk = ['ko', 'ja', 'zh'].includes(locale)

  return (
    <div className="space-y-8">
      {/* 호스트 유형 선택 */}
      <HostTypeSelector
        value={step1.hostType}
        onChange={(type: HostType) => setHostType(type)}
      />

      {/* 자치구 선택 */}
      <div className="space-y-2">
        <label className="block text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
          {t('district')}
        </label>
        <select
          value={step1.district}
          onChange={e => setDistrict(e.target.value)}
          className="w-full h-12 px-3 border border-[#DDDDDD] dark:border-[#3A3A3C] rounded-lg bg-white dark:bg-[#2C2C2E] text-[#222222] dark:text-[#F5F5F5] focus:outline-none focus:ring-2 focus:ring-[#FF385C] focus:border-transparent text-sm"
        >
          <option value="">{t('districtPlaceholder')}</option>
          {Object.entries(DISTRICTS_KR).map(([en, ko]) => (
            <option key={en} value={en}>
              {ko} ({en})
            </option>
          ))}
        </select>
      </div>

      {/* 숙소 유형 */}
      <div className="space-y-2">
        <label className="block text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
          {t('roomType')}
        </label>
        <div className="grid grid-cols-2 gap-2">
          {ROOM_TYPES.map(rt => (
            <button
              key={rt.value}
              type="button"
              onClick={() => setRoomType(rt.value as RoomType)}
              className={cn(
                'py-2.5 px-3 rounded-lg border text-sm font-medium transition-all text-left',
                step1.roomType === rt.value
                  ? 'border-[#222222] dark:border-white bg-[#F7F7F7] dark:bg-[#3A3A3C] text-[#222222] dark:text-white'
                  : 'border-[#DDDDDD] dark:border-[#3A3A3C] hover:border-[#767676] text-[#484848] dark:text-[#EBEBEB]',
              )}
            >
              {locale === 'ko' ? rt.labelKo : rt.labelEn}
            </button>
          ))}
        </div>
      </div>

      {/* 인원 / 침실 / 화장실 */}
      <div className="space-y-4">
        <CounterField
          label={t('accommodates')}
          value={step1.accommodates}
          min={1}
          max={16}
          onChange={setAccommodates}
          unit={isCjk ? tCommon('person') : ''}
        />
        <CounterField
          label={t('bedrooms')}
          value={step1.bedrooms}
          min={0}
          max={10}
          onChange={setBedrooms}
          unit={isCjk ? tCommon('room') : ''}
        />
        <CounterField
          label={t('bathrooms')}
          value={step1.bathrooms}
          min={1}
          max={8}
          onChange={setBathrooms}
          unit={tCommon('bathroom')}
          step={0.5}
        />
      </div>

      {/* 편의시설 */}
      <div className="space-y-2">
        <label className="block text-sm font-semibold text-[#222222] dark:text-[#F5F5F5]">
          {t('amenities')}
        </label>
        <div className="flex flex-wrap gap-2">
          {AMENITIES.map(amenity => {
            const selected = step1.amenities.includes(amenity.value)
            return (
              <button
                key={amenity.value}
                type="button"
                onClick={() => toggleAmenity(amenity.value)}
                className={cn(
                  'px-3 py-1.5 rounded-full border text-xs font-medium transition-all',
                  selected
                    ? 'border-[#222222] dark:border-white bg-[#222222] dark:bg-white text-white dark:text-[#222222]'
                    : 'border-[#DDDDDD] dark:border-[#3A3A3C] hover:border-[#767676] text-[#484848] dark:text-[#EBEBEB]',
                )}
              >
                {locale === 'ko' ? amenity.labelKo : amenity.labelEn}
              </button>
            )
          })}
        </div>
      </div>
    </div>
  )
}

/* ============================================
   카운터 필드 (에어비앤비 스타일 +/- 버튼)
   ============================================ */
function CounterField({
  label,
  value,
  min,
  max,
  onChange,
  unit,
  step = 1,
}: {
  label: string
  value: number
  min: number
  max: number
  onChange: (n: number) => void
  unit: string
  step?: number
}) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-[#EBEBEB] dark:border-[#3A3A3C]">
      <span className="text-sm font-medium text-[#222222] dark:text-[#F5F5F5]">{label}</span>
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={() => onChange(Math.max(min, value - step))}
          disabled={value <= min}
          className="w-8 h-8 rounded-full border border-[#DDDDDD] dark:border-[#3A3A3C] flex items-center justify-center hover:border-[#222222] dark:hover:border-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          <Minus size={14} />
        </button>
        <span className="w-10 text-center text-sm font-medium">
          {value}{unit}
        </span>
        <button
          type="button"
          onClick={() => onChange(Math.min(max, value + step))}
          disabled={value >= max}
          className="w-8 h-8 rounded-full border border-[#DDDDDD] dark:border-[#3A3A3C] flex items-center justify-center hover:border-[#222222] dark:hover:border-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          <Plus size={14} />
        </button>
      </div>
    </div>
  )
}
