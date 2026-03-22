/* 에어비앤비 스타일 앱 헤더: 로고 + 언어/통화 버튼 */

'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { Globe, Moon, Sun } from 'lucide-react'
import { LanguageCurrencyModal } from '@/components/header/LanguageCurrencyModal'
import { useLocaleStore } from '@/store/localeStore'
import { useTheme } from '@/hooks/useTheme'
import { SUPPORTED_LANGUAGES } from '@/lib/constants'

export function AppHeader() {
  const t = useTranslations('header')
  const { language } = useLocaleStore()
  const [modalOpen, setModalOpen] = useState(false)
  const { isDark, toggleTheme } = useTheme()

  const currentLang = SUPPORTED_LANGUAGES.find(l => l.code === language)

  return (
    <>
      <header className="sticky top-0 z-50 bg-white dark:bg-[#1C1C1E] border-b border-[#DDDDDD] dark:border-[#3A3A3C]">
        <div className="flex items-center justify-between px-4 sm:px-6 h-16">
          {/* 에어비앤비 로고 */}
          <div className="flex items-center gap-2 sm:gap-3">
            <svg
              viewBox="0 0 32 32"
              className="w-7 h-7 sm:w-8 sm:h-8 text-[#FF385C] fill-current flex-shrink-0"
              aria-label="Airbnb"
            >
              <path d="M16 1C7.163 1 0 8.163 0 17c0 5.411 2.617 10.222 6.676 13.26L16 31l9.324-0.74C29.383 27.222 32 22.411 32 17 32 8.163 24.837 1 16 1zm0 28.5c-6.904 0-12.5-5.596-12.5-12.5S9.096 4.5 16 4.5 28.5 10.096 28.5 17 22.904 29.5 16 29.5z" />
              <path d="M16 8c-2.761 0-5 2.239-5 5 0 1.933 1.097 3.614 2.7 4.47L16 24l2.3-6.53C19.903 16.614 21 14.933 21 13c0-2.761-2.239-5-5-5zm0 7.5c-1.381 0-2.5-1.119-2.5-2.5S14.619 10.5 16 10.5s2.5 1.119 2.5 2.5-1.119 2.5-2.5 2.5z" />
            </svg>
            <span className="text-[#FF385C] font-bold text-base sm:text-lg tracking-tight hidden sm:block">
              {t('title')}
            </span>
          </div>

          {/* 우측 버튼 그룹 */}
          <div className="flex items-center gap-2">
            {/* 다크모드 토글 */}
            <button
              type="button"
              onClick={toggleTheme}
              className="p-2 rounded-full border border-[#DDDDDD] dark:border-[#3A3A3C] hover:border-[#222222] dark:hover:border-white transition-colors"
              aria-label={isDark ? '라이트 모드로 전환' : '다크 모드로 전환'}
            >
              {isDark
                ? <Sun size={15} className="text-[#EBEBEB]" />
                : <Moon size={15} className="text-[#484848]" />
              }
            </button>

            {/* 언어/통화 버튼 */}
            <button
              type="button"
              onClick={() => setModalOpen(true)}
              className="flex items-center gap-1.5 sm:gap-2 px-2.5 sm:px-3 py-2 rounded-full border border-[#DDDDDD] dark:border-[#3A3A3C] hover:border-[#222222] dark:hover:border-white transition-colors text-sm font-medium"
              aria-label="언어 및 통화 선택"
            >
              <Globe size={15} className="text-[#484848] dark:text-[#EBEBEB]" />
              <span className="text-[#484848] dark:text-[#EBEBEB] hidden sm:block">
                {currentLang?.flag} {currentLang?.label}
              </span>
            </button>
          </div>
        </div>
      </header>

      <LanguageCurrencyModal open={modalOpen} onOpenChange={setModalOpen} />
    </>
  )
}
