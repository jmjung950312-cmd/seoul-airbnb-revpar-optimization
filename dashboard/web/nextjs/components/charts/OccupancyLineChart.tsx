/* 예약률 라인 차트 - 실선(내 숙소) + 점선(비교군) */

'use client'

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

interface OccupancyData {
  month: string
  myOccupancy: number
  marketMedian: number
}

interface OccupancyLineChartProps {
  data: OccupancyData[]
}

/* 커스텀 툴팁 */
function CustomTooltip({
  active,
  payload,
  label,
}: {
  active?: boolean
  payload?: Array<{ name: string; value: number; color: string }>
  label?: string
}) {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-white dark:bg-[#2C2C2E] border border-[#DDDDDD] dark:border-[#3A3A3C] rounded-lg p-3 shadow-lg">
      <p className="text-xs font-semibold text-[#484848] dark:text-[#EBEBEB] mb-2">{label}</p>
      {payload.map(entry => (
        <div key={entry.name} className="flex items-center gap-2 text-xs">
          <span className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }} />
          <span className="text-[#767676]">{entry.name}:</span>
          <span className="font-medium text-[#222222] dark:text-[#F5F5F5]">
            {((entry.value ?? 0) * 100).toFixed(1)}%
          </span>
        </div>
      ))}
    </div>
  )
}

export function OccupancyLineChart({ data }: OccupancyLineChartProps) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid
          strokeDasharray="3 3"
          stroke="#EBEBEB"
          vertical={false}
        />
        <XAxis
          dataKey="month"
          tick={{ fontSize: 12, fill: '#767676' }}
          axisLine={false}
          tickLine={false}
        />
        <YAxis
          tickFormatter={v => `${(v * 100).toFixed(0)}%`}
          tick={{ fontSize: 12, fill: '#767676' }}
          axisLine={false}
          tickLine={false}
          domain={[0, 1]}
          width={45}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend
          iconType="circle"
          iconSize={8}
          wrapperStyle={{ fontSize: '12px', paddingTop: '12px' }}
        />
        {/* 내 숙소: 실선 */}
        <Line
          type="monotone"
          dataKey="myOccupancy"
          name="내 숙소"
          stroke="#FF385C"
          strokeWidth={2.5}
          dot={{ fill: '#FF385C', r: 4, strokeWidth: 0 }}
          activeDot={{ r: 6, strokeWidth: 0 }}
        />
        {/* 시장 중앙값: 점선 */}
        <Line
          type="monotone"
          dataKey="marketMedian"
          name="시장 중앙값"
          stroke="#767676"
          strokeWidth={2}
          strokeDasharray="6 4"
          dot={false}
          activeDot={{ r: 4, strokeWidth: 0 }}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
