/* 전체 대시보드 레이아웃: Header + Sidebar + Content */

'use client'

import { AppHeader } from './AppHeader'
import { Sidebar } from './Sidebar'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Menu } from 'lucide-react'
import { useState } from 'react'

interface DashboardLayoutProps {
  children: React.ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-[#F7F7F7] dark:bg-[#1C1C1E] flex flex-col">
      {/* 헤더 */}
      <AppHeader />

      <div className="flex flex-1 overflow-hidden">
        {/* 데스크톱 사이드바 */}
        <Sidebar className="hidden md:flex h-full overflow-y-auto" />

        {/* 콘텐츠 영역 */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* 모바일 사이드바 버튼 */}
          <div className="md:hidden flex items-center px-4 py-2 border-b border-[#DDDDDD] dark:border-[#3A3A3C] bg-white dark:bg-[#1C1C1E]">
            <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
              <SheetTrigger asChild>
                <button
                  type="button"
                  className="flex items-center gap-2 text-sm font-medium text-[#484848] dark:text-[#EBEBEB]"
                >
                  <Menu size={20} />
                  <span>메뉴</span>
                </button>
              </SheetTrigger>
              <SheetContent side="left" className="p-0 w-64">
                <Sidebar className="flex h-full" />
              </SheetContent>
            </Sheet>
          </div>

          {/* 메인 콘텐츠 */}
          <main className="flex-1 overflow-y-auto">
            {children}
          </main>
        </div>
      </div>
    </div>
  )
}
