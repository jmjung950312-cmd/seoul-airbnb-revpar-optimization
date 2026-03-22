/* 에어비앤비 스타일 상단 필터 바 */

'use client'

import { useTranslations } from 'next-intl'
import { FilterChip } from '@/components/common/FilterChip'
import { SlidersHorizontal } from 'lucide-react'
import { useState } from 'react'

export function FilterBar() {
  const t = useTranslations('filter')
  const [activeFilter, setActiveFilter] = useState<string | null>(null)

  const filters = [
    { id: 'district', label: t('district') },
    { id: 'dateRange', label: t('dateRange') },
    { id: 'roomType', label: t('roomType') },
    { id: 'priceRange', label: t('priceRange') },
    { id: 'guestCount', label: t('guestCount') },
  ]

  const toggleFilter = (id: string) => {
    setActiveFilter(prev => (prev === id ? null : id))
  }

  return (
    <div className="bg-white dark:bg-[#1C1C1E] border-b border-[#DDDDDD] dark:border-[#3A3A3C]">
      <div className="flex items-center gap-3 px-6 py-3 overflow-x-auto">
        <div className="flex items-center gap-2 flex-shrink-0">
          <SlidersHorizontal size={16} className="text-[#484848] dark:text-[#EBEBEB]" />
        </div>

        <div className="flex items-center gap-2 overflow-x-auto no-scrollbar">
          {filters.map(filter => (
            <FilterChip
              key={filter.id}
              label={filter.label}
              active={activeFilter === filter.id}
              onClick={() => toggleFilter(filter.id)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
