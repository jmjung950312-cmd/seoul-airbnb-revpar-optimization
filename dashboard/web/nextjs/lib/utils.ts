/* 유틸리티 함수 모음 */

import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { EXCHANGE_RATES, SUPPORTED_CURRENCIES } from './constants'
import type { SupportedCurrency } from '@/types/locale'

/* Tailwind 클래스 병합 헬퍼 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/* ============================================
   통화 포맷
   ============================================ */
export function formatCurrency(
  valueKRW: number,
  currencyCode: SupportedCurrency = 'KRW',
  compact = false,
): string {
  const rate = EXCHANGE_RATES[currencyCode] ?? 1
  const converted = valueKRW * rate

  const currencyInfo = SUPPORTED_CURRENCIES.find(c => c.code === currencyCode)
  const locale = currencyInfo?.locale ?? 'ko-KR'

  const options: Intl.NumberFormatOptions = {
    style: 'currency',
    currency: currencyCode,
    maximumFractionDigits: currencyCode === 'KRW' || currencyCode === 'JPY' ? 0 : 2,
  }

  if (compact && Math.abs(converted) >= 1_000_000) {
    options.notation = 'compact'
    options.maximumSignificantDigits = 3
  }

  return new Intl.NumberFormat(locale, options).format(converted)
}

/* ============================================
   숫자 포맷 (통화 기호 없이)
   ============================================ */
export function formatNumber(value: number, locale = 'ko-KR'): string {
  return new Intl.NumberFormat(locale).format(value)
}

/* ============================================
   퍼센트 포맷
   ============================================ */
export function formatPercent(value: number, decimals = 1): string {
  return `${(value * 100).toFixed(decimals)}%`
}

/* ============================================
   Haversine 거리 계산 (km)
   ============================================ */
export function haversineDistance(
  lat1: number,
  lng1: number,
  lat2: number,
  lng2: number,
): number {
  const R = 6371
  const dLat = ((lat2 - lat1) * Math.PI) / 180
  const dLng = ((lng2 - lng1) * Math.PI) / 180
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLng / 2) ** 2
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
}

/* ============================================
   사진 수 → 등급
   ============================================ */
export function getPhotosTier(photos: number): string {
  if (photos >= 30) return 'A'
  if (photos >= 20) return 'B'
  if (photos >= 10) return 'C'
  return 'D'
}

/* ============================================
   달력 날짜 배열 생성 (해당 월)
   null = 빈 셀 (앞쪽 패딩)
   ============================================ */
export function getCalendarDays(year: number, month: number): (number | null)[] {
  const firstDay = new Date(year, month - 1, 1).getDay()
  const daysInMonth = new Date(year, month, 0).getDate()
  const startPad = firstDay === 0 ? 0 : firstDay

  const cells: (number | null)[] = Array(startPad).fill(null)
  for (let d = 1; d <= daysInMonth; d++) cells.push(d)
  return cells
}

/* ============================================
   예약률 계산
   ============================================ */
export function calcOccupancyRate(bookedDays: Set<number>, year: number, month: number): number {
  const daysInMonth = new Date(year, month, 0).getDate()
  return bookedDays.size / daysInMonth
}

/* ============================================
   숫자 범위 클램프
   ============================================ */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max)
}

