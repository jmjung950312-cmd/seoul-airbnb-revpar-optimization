/* 주변 관광지 섹션 */

'use client'

import { useTranslations } from 'next-intl'
import { MapPin } from 'lucide-react'
import { SectionCard } from '@/components/common/SectionCard'
import { useResultsStore } from '@/store/resultsStore'

const CATEGORY_COLORS: Record<string, string> = {
  관광: '#FF385C',
  음식: '#FC642D',
  교통: '#3B82F6',
  쇼핑: '#8B5CF6',
  문화: '#00A699',
  자연: '#10B981',
}

export function NearbyPOISection() {
  const t = useTranslations('dashboard.nearbyPOI')
  const { results } = useResultsStore()

  if (!results) return null

  const { nearbyPOIs } = results

  if (!nearbyPOIs?.length) return null

  return (
    <SectionCard id="poi" title={t('title')}>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {nearbyPOIs.map((poi, idx) => {
          const color = CATEGORY_COLORS[poi.category] ?? '#767676'
          return (
            <div
              key={idx}
              className="flex items-center gap-3 p-3 rounded-xl bg-[#F7F7F7] dark:bg-[#3A3A3C] hover:bg-[#EBEBEB] dark:hover:bg-[#444444] transition-colors"
            >
              <div
                className="w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0"
                style={{ backgroundColor: `${color}20` }}
              >
                <MapPin size={16} style={{ color }} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-[#222222] dark:text-[#F5F5F5] truncate">
                  {poi.name}
                </p>
                <div className="flex items-center gap-2 mt-0.5">
                  <span
                    className="text-xs font-medium px-1.5 py-0.5 rounded-full"
                    style={{ color, backgroundColor: `${color}15` }}
                  >
                    {poi.category}
                  </span>
                  <span className="text-xs text-[#767676]">{poi.distance_km.toFixed(1)}km</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </SectionCard>
  )
}
