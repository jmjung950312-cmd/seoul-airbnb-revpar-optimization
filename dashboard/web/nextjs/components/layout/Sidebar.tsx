/* 에어비앤비 스타일 좌측 사이드바 네비게이션 */

'use client'

import { useTranslations } from 'next-intl'
import {
  TrendingUp,
  DollarSign,
  Map,
  Activity,
  MapPin,
  FileText,
  Settings,
  ChevronDown,
  ChevronRight,
  BarChart2,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useResultsStore } from '@/store/resultsStore'
import { useState } from 'react'

interface NavItem {
  id: string
  labelKey: string
  icon: React.ReactNode
  children?: NavItem[]
}

const ICON_SIZE = 18

function buildNavItems(t: ReturnType<typeof useTranslations<'sidebar'>>): NavItem[] {
  return [
    {
      id: 'wizard',
      labelKey: 'inputSettings',
      icon: <Settings size={ICON_SIZE} />,
      children: [
        { id: 'wizard-step1', labelKey: 'basicInfo', icon: null },
        { id: 'wizard-step2', labelKey: 'propertySettings', icon: null },
        { id: 'wizard-step3', labelKey: 'opexInput', icon: null },
        { id: 'wizard-step4', labelKey: 'operations', icon: null },
      ],
    },
    { id: 'revenue', labelKey: 'revenueSummary', icon: <TrendingUp size={ICON_SIZE} /> },
    { id: 'pricing', labelKey: 'pricingStrategy', icon: <DollarSign size={ICON_SIZE} /> },
    {
      id: 'market',
      labelKey: 'marketDiagnosis',
      icon: <Map size={ICON_SIZE} />,
      children: [
        { id: 'market-diagnosis', labelKey: 'marketDiagnosis', icon: null },
        { id: 'poi', labelKey: 'nearbyPOI', icon: null },
      ],
    },
    { id: 'health', labelKey: 'healthScore', icon: <Activity size={ICON_SIZE} /> },
    { id: 'description', labelKey: 'listingDesc', icon: <FileText size={ICON_SIZE} /> },
  ] as NavItem[]
}

interface SidebarProps {
  className?: string
}

export function Sidebar({ className }: SidebarProps) {
  const t = useTranslations('sidebar')
  const { activeSection, setActiveSection, results } = useResultsStore()
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set(['wizard']))

  const navItems = buildNavItems(t)

  const toggleExpand = (id: string) => {
    setExpandedItems(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const handleNavClick = (id: string) => {
    setActiveSection(id)
  }

  return (
    <aside
      className={cn(
        'w-60 flex-shrink-0 bg-white dark:bg-[#1C1C1E] border-r border-[#EBEBEB] dark:border-[#3A3A3C] flex flex-col',
        className,
      )}
    >
      {/* 대시보드 제목 */}
      <div className="px-4 py-3 border-b border-[#EBEBEB] dark:border-[#3A3A3C]">
        <div className="flex items-center gap-2">
          <BarChart2 size={20} className="text-[#FF385C]" />
          <span className="font-bold text-base text-[#222222] dark:text-[#F5F5F5]">
            {t('performance')}
          </span>
        </div>
      </div>

      {/* 네비게이션 */}
      <nav className="flex-1 overflow-y-auto px-2 py-3 space-y-0.5">
        {navItems.map(item => (
          <NavGroup
            key={item.id}
            item={item}
            activeSection={activeSection}
            expanded={expandedItems.has(item.id)}
            onToggleExpand={() => toggleExpand(item.id)}
            onNavClick={handleNavClick}
            t={t}
            hasResults={!!results}
          />
        ))}
      </nav>

      {/* 하단 분석 시작 버튼 */}
      {!results && (
        <div className="px-4 py-4 border-t border-[#EBEBEB] dark:border-[#3A3A3C]">
          <button
            type="button"
            onClick={() => handleNavClick('wizard')}
            className="w-full py-2.5 rounded-lg bg-[#FF385C] text-white text-sm font-semibold hover:bg-[#E31C5F] transition-colors"
          >
            {t('startAnalysis')}
          </button>
        </div>
      )}
    </aside>
  )
}

/* ============================================
   네비게이션 그룹 (부모 + 자식 아이템)
   ============================================ */
function NavGroup({
  item,
  activeSection,
  expanded,
  onToggleExpand,
  onNavClick,
  t,
  hasResults,
}: {
  item: NavItem
  activeSection: string
  expanded: boolean
  onToggleExpand: () => void
  onNavClick: (id: string) => void
  t: ReturnType<typeof useTranslations<'sidebar'>>
  hasResults: boolean
}) {
  const isActive = activeSection === item.id
  const hasChildren = item.children && item.children.length > 0

  /* 결과가 없으면 결과 섹션 비활성화 */
  const isDisabled =
    !hasResults && !['wizard', 'wizard-step1', 'wizard-step2', 'wizard-step3', 'wizard-step4'].includes(item.id)

  return (
    <div>
      <button
        type="button"
        onClick={hasChildren ? onToggleExpand : () => onNavClick(item.id)}
        disabled={isDisabled}
        className={cn(
          'nav-item w-full',
          isActive && 'active',
          isDisabled && 'opacity-40 cursor-not-allowed',
        )}
      >
        {item.icon && (
          <span className={cn('flex-shrink-0', isActive && 'text-[#FF385C]')}>
            {item.icon}
          </span>
        )}
        <span className="flex-1 text-left text-sm">
          {t(item.labelKey as Parameters<typeof t>[0])}
        </span>
        {hasChildren && (
          <span className="flex-shrink-0 text-[#767676]">
            {expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          </span>
        )}
      </button>

      {/* 자식 아이템 */}
      {hasChildren && expanded && (
        <div className="ml-7 mt-0.5 space-y-0.5">
          {item.children!.map(child => (
            <button
              key={child.id}
              type="button"
              onClick={() => onNavClick(child.id)}
              className={cn(
                'nav-item w-full text-sm pl-3',
                activeSection === child.id && 'active',
              )}
            >
              {t(child.labelKey as Parameters<typeof t>[0])}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
