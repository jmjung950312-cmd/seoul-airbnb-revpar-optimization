/* 에어비앤비 Performance Stats 스타일 KPI 카드 */

'use client'

import { cn } from '@/lib/utils'

interface KpiStatProps {
  label: string
  value: string
  subValue?: string
  trend?: number
  highlight?: boolean
  className?: string
}

export function KpiStat({ label, value, subValue, trend, highlight, className }: KpiStatProps) {
  return (
    <div className={cn('flex flex-col gap-1', className)}>
      <span className="kpi-label">{label}</span>
      <div className="flex items-baseline gap-2">
        <span
          className={cn('kpi-value', highlight && 'text-[#FF385C]')}
        >
          {value}
        </span>
        {trend !== undefined && (
          <span
            className={cn(
              'text-sm font-medium',
              trend >= 0 ? 'text-[#00A699]' : 'text-[#FF385C]',
            )}
          >
            {trend >= 0 ? '▲' : '▼'} {Math.abs(trend).toFixed(1)}%
          </span>
        )}
      </div>
      {subValue && (
        <span className="text-xs text-[var(--color-foggy)]">{subValue}</span>
      )}
    </div>
  )
}
