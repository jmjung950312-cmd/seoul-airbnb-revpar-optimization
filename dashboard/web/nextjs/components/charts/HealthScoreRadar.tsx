/* 헬스 스코어 레이더/바 차트 */

'use client'

import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
} from 'recharts'

interface HealthScoreData {
  name: string
  score: number
  max_score: number
}

interface HealthScoreRadarProps {
  data: HealthScoreData[]
}

export function HealthScoreRadar({ data }: HealthScoreRadarProps) {
  const normalized = data.map(d => ({
    subject: d.name,
    value: Math.round((d.score / d.max_score) * 100),
    fullMark: 100,
  }))

  return (
    <ResponsiveContainer width="100%" height={280}>
      <RadarChart data={normalized} margin={{ top: 10, right: 30, bottom: 10, left: 30 }}>
        <PolarGrid stroke="#EBEBEB" />
        <PolarAngleAxis
          dataKey="subject"
          tick={{ fontSize: 12, fill: '#767676' }}
        />
        <PolarRadiusAxis
          angle={90}
          domain={[0, 100]}
          tick={{ fontSize: 10, fill: '#767676' }}
          tickCount={4}
        />
        <Tooltip
          formatter={(value: number | undefined) => [`${value ?? 0}점`, '점수']}
          contentStyle={{
            border: '1px solid #DDDDDD',
            borderRadius: '8px',
            fontSize: '12px',
          }}
        />
        <Radar
          name="헬스 스코어"
          dataKey="value"
          stroke="#FF385C"
          fill="#FF385C"
          fillOpacity={0.15}
          strokeWidth={2}
        />
      </RadarChart>
    </ResponsiveContainer>
  )
}
