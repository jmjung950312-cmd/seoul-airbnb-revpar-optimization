/* 호스트 유형 선택 카드 - 카드 전체가 클릭 영역 */

'use client'

import { useTranslations } from 'next-intl'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { HostType } from '@/types/wizard'

interface HostTypeSelectorProps {
  value: HostType | null
  onChange: (type: HostType) => void
}

export function HostTypeSelector({ value, onChange }: HostTypeSelectorProps) {
  const t = useTranslations('wizard.hostType')

  return (
    <div className="space-y-4">
      <div className="text-center mb-6">
        <h2 className="text-xl font-semibold text-[#222222] dark:text-[#F5F5F5]">
          {t('question')}
        </h2>
        <p className="text-sm text-[#767676] mt-1">{t('subtitle')}</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <HostTypeCard
          type="new"
          label={t('new.title')}
          description={t('new.desc')}
          emoji="🌱"
          selected={value === 'new'}
          onSelect={() => onChange('new')}
        />
        <HostTypeCard
          type="existing"
          label={t('existing.title')}
          description={t('existing.desc')}
          emoji="🏅"
          selected={value === 'existing'}
          onSelect={() => onChange('existing')}
        />
      </div>
    </div>
  )
}

/* ============================================
   호스트 타입 카드
   ============================================ */
function HostTypeCard({
  type,
  label,
  description,
  emoji,
  selected,
  onSelect,
}: {
  type: HostType
  label: string
  description: string
  emoji: string
  selected: boolean
  onSelect: () => void
}) {
  return (
    <button
      type="button"
      role="button"
      onClick={onSelect}
      aria-pressed={selected}
      className={cn(
        'relative flex flex-col items-center text-center gap-3 p-6 rounded-xl border-2 transition-all cursor-pointer',
        'hover:bg-[#F7F7F7] dark:hover:bg-[#2C2C2E]',
        selected
          ? 'border-[#FF385C] bg-[#FFF1F2] dark:bg-[#3A1A1E]'
          : 'border-[#DDDDDD] dark:border-[#3A3A3C] bg-white dark:bg-[#2C2C2E]',
      )}
    >
      {/* 선택 체크 아이콘 (우상단) */}
      {selected && (
        <div className="absolute top-3 right-3 w-5 h-5 rounded-full bg-[#FF385C] flex items-center justify-center">
          <Check size={12} className="text-white" />
        </div>
      )}

      {/* 이모지 */}
      <span className="text-4xl">{emoji}</span>

      {/* 제목 */}
      <span
        className={cn(
          'text-base font-semibold',
          selected ? 'text-[#FF385C]' : 'text-[#222222] dark:text-[#F5F5F5]',
        )}
      >
        {label}
      </span>

      {/* 설명 */}
      <span className="text-sm text-[#767676] leading-relaxed">{description}</span>
    </button>
  )
}
