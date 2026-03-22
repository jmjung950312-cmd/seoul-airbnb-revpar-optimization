/* 다크/라이트 테마 토글 훅 */

'use client'

import { useEffect, useState } from 'react'

type Theme = 'light' | 'dark' | 'system'

export function useTheme() {
  const [theme, setThemeState] = useState<Theme>('system')
  /* SSR-safe 초기값: false → useEffect에서 실제 값으로 업데이트 */
  const [isDark, setIsDark] = useState(false)

  const applyTheme = (t: Theme) => {
    const root = document.documentElement
    if (t === 'dark' || (t === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
  }

  /* 초기 로드: localStorage 또는 시스템 선호도 */
  useEffect(() => {
    const stored = localStorage.getItem('airbnb-theme') as Theme | null
    const resolved = stored ?? 'system'
    setThemeState(resolved)
    const dark = resolved === 'dark' || (resolved === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)
    setIsDark(dark)
    applyTheme(resolved)
  }, [])

  const setTheme = (t: Theme) => {
    setThemeState(t)
    localStorage.setItem('airbnb-theme', t)
    const dark = t === 'dark' || (t === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)
    setIsDark(dark)
    applyTheme(t)
  }

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark')
  }

  return { theme, isDark, setTheme, toggleTheme }
}
