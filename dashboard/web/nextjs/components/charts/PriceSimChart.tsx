/* 요금 시뮬레이션 영역 차트 */

'use client'

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts'
import { formatCurrency } from '@/lib/utils'
import type { SupportedCurrency } from '@/types/locale'

interface PriceSimData {
  price: number
  revenue: number
  netProfit: number
}

interface PriceSimChartProps {
  data: PriceSimData[]
  currentPrice: number
  optimalPrice: number
  currency: SupportedCurrency
}

function CustomTooltip({
  active,
  payload,
  label,
  currency,
}: {
  active?: boolean
  payload?: ReadonlyArray<{ name: string; value: number; color: string }>
  label?: number
  currency: SupportedCurrency
}) {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-white dark:bg-[#2C2C2E] border border-[#DDDDDD] dark:border-[#3A3A3C] rounded-lg p-3 shadow-lg">
      <p className="text-xs font-semibold text-[#484848] dark:text-[#EBEBEB] mb-2">
        요금: {formatCurrency(label ?? 0, currency)}
      </p>
      {payload.map(entry => (
        <div key={entry.name} className="flex items-center gap-2 text-xs">
          <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }} />
          <span className="text-[#767676]">{entry.name}:</span>
          <span className="font-medium">
            {formatCurrency(entry.value, currency)}
          </span>
        </div>
      ))}
    </div>
  )
}

export function PriceSimChart({ data, currentPrice, optimalPrice, currency }: PriceSimChartProps) {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <AreaChart data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
        <defs>
          <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#FF385C" stopOpacity={0.15} />
            <stop offset="95%" stopColor="#FF385C" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="netProfitGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#00A699" stopOpacity={0.15} />
            <stop offset="95%" stopColor="#00A699" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#EBEBEB" vertical={false} />
        <XAxis
          dataKey="price"
          tickFormatter={v => `₩${(v / 10000).toFixed(0)}만`}
          tick={{ fontSize: 11, fill: '#767676' }}
          axisLine={false}
          tickLine={false}
        />
        <YAxis
          tickFormatter={v => `₩${(v / 10000).toFixed(0)}만`}
          tick={{ fontSize: 11, fill: '#767676' }}
          axisLine={false}
          tickLine={false}
          width={50}
        />
        <Tooltip content={(props) => <CustomTooltip {...props} label={props.label as number} currency={currency} />} />

        {/* 현재 요금 기준선 */}
        <ReferenceLine
          x={currentPrice}
          stroke="#767676"
          strokeDasharray="4 4"
          label={{ value: '현재', position: 'insideTopRight', fontSize: 10, fill: '#767676' }}
        />
        {/* 최적 요금 기준선 */}
        <ReferenceLine
          x={optimalPrice}
          stroke="#FF385C"
          strokeDasharray="4 4"
          label={{ value: '최적', position: 'insideTopRight', fontSize: 10, fill: '#FF385C' }}
        />

        <Area
          type="monotone"
          dataKey="revenue"
          name="월 예상 수입"
          stroke="#FF385C"
          strokeWidth={2}
          fill="url(#revenueGrad)"
        />
        <Area
          type="monotone"
          dataKey="netProfit"
          name="월 예상 순이익"
          stroke="#00A699"
          strokeWidth={2}
          fill="url(#netProfitGrad)"
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}
