/* 언어 및 통화 선택 전역 상태 (localStorage 영속) */

'use client'

import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { SupportedLocale, SupportedCurrency } from '@/types/locale'

interface LocaleState {
  language: SupportedLocale
  currency: SupportedCurrency
  setLanguage: (lang: SupportedLocale) => void
  setCurrency: (currency: SupportedCurrency) => void
}

export const useLocaleStore = create<LocaleState>()(
  persist(
    (set) => ({
      language: 'ko',
      currency: 'KRW',
      setLanguage: (language) => set({ language }),
      setCurrency: (currency) => set({ currency }),
    }),
    {
      name: 'airbnb-locale',
    },
  ),
)
