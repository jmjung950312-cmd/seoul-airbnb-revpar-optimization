/* 분석 결과 캐시 전역 상태 */

'use client'

import { create } from 'zustand'
import type { DashboardResults } from '@/types/api'

interface ResultsState {
  results: DashboardResults | null
  isLoading: boolean
  error: string | null
  activeSection: string
  setResults: (results: DashboardResults) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  setActiveSection: (section: string) => void
  clearResults: () => void
}

export const useResultsStore = create<ResultsState>()((set) => ({
  results: null,
  isLoading: false,
  error: null,
  activeSection: 'revenue',

  setResults: (results) => set({ results, isLoading: false, error: null }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error, isLoading: false }),
  setActiveSection: (activeSection) => set({ activeSection }),
  clearResults: () => set({ results: null, error: null }),
}))
