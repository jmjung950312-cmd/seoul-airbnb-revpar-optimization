/* 에어비앤비 스타일 필터 칩 */

'use client'

import { cn } from '@/lib/utils'

interface FilterChipProps {
  label: string
  icon?: React.ReactNode
  active?: boolean
  onClick?: () => void
  className?: string
}

export function FilterChip({ label, icon, active, onClick, className }: FilterChipProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        'filter-chip transition-all',
        active && 'filter-chip-active',
        className,
      )}
    >
      {icon && <span className="flex-shrink-0">{icon}</span>}
      <span>{label}</span>
    </button>
  )
}
