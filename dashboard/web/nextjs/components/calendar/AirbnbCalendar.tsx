/* 에어비앤비 스타일 달력 컴포넌트 */

'use client'

import { useTranslations } from 'next-intl'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { getCalendarDays, calcOccupancyRate } from '@/lib/utils'
import { HOLIDAYS_2025 } from '@/lib/constants'
import { cn } from '@/lib/utils'

interface AirbnbCalendarProps {
  year: number
  month: number
  bookedDays: Set<number>
  onDayToggle: (day: number) => void
  onMonthChange: (year: number, month: number) => void
}

const WEEKDAY_KEYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'] as const

export function AirbnbCalendar({
  year,
  month,
  bookedDays,
  onDayToggle,
  onMonthChange,
}: AirbnbCalendarProps) {
  const t = useTranslations('calendar')

  const today = new Date()
  const isCurrentMonth = today.getFullYear() === year && today.getMonth() + 1 === month

  const days = getCalendarDays(year, month)
  const holidays = HOLIDAYS_2025[month] ?? new Set<number>()

  const occupancyRate = calcOccupancyRate(bookedDays, year, month)
  const daysInMonth = new Date(year, month, 0).getDate()

  /* 이전/다음 달 이동 */
  const handlePrevMonth = () => {
    if (month === 1) onMonthChange(year - 1, 12)
    else onMonthChange(year, month - 1)
  }

  const handleNextMonth = () => {
    if (month === 12) onMonthChange(year + 1, 1)
    else onMonthChange(year, month + 1)
  }

  return (
    <div className="bg-white dark:bg-[#2C2C2E] rounded-xl border border-[#DDDDDD] dark:border-[#3A3A3C] p-5 select-none">
      {/* 달력 헤더: 월 이동 */}
      <div className="flex items-center justify-between mb-5">
        <button
          type="button"
          onClick={handlePrevMonth}
          aria-label={t('prevMonth')}
          className="p-2 rounded-full hover:bg-[#F7F7F7] dark:hover:bg-[#3A3A3C] transition-colors"
        >
          <ChevronLeft size={18} />
        </button>

        <div className="text-center">
          <p className="font-semibold text-base">
            {year}년 {month}월
          </p>
          <p className="text-xs text-[#767676] mt-0.5">
            {t('bookedDays')}: {bookedDays.size}일 · 예약률 {(occupancyRate * 100).toFixed(0)}%
          </p>
        </div>

        <button
          type="button"
          onClick={handleNextMonth}
          aria-label={t('nextMonth')}
          className="p-2 rounded-full hover:bg-[#F7F7F7] dark:hover:bg-[#3A3A3C] transition-colors"
        >
          <ChevronRight size={18} />
        </button>
      </div>

      {/* 요일 헤더 */}
      <div className="grid grid-cols-7 mb-2">
        {WEEKDAY_KEYS.map(day => (
          <div
            key={day}
            className="text-center text-xs font-medium text-[#767676] py-1"
          >
            {t(day)}
          </div>
        ))}
      </div>

      {/* 날짜 그리드 */}
      <div className="grid grid-cols-7 gap-y-1">
        {days.map((day, idx) => {
          if (day === null) {
            return <div key={`empty-${idx}`} />
          }

          const isBooked = bookedDays.has(day)
          const isToday = isCurrentMonth && today.getDate() === day
          const isHoliday = holidays.has(day)
          const isSunday = (idx % 7) === 0

          return (
            <div key={day} className="flex justify-center">
              <button
                type="button"
                onClick={() => onDayToggle(day)}
                aria-label={`${month}월 ${day}일${isBooked ? ' (예약됨)' : ''}`}
                aria-pressed={isBooked}
                className={cn(
                  'calendar-day',
                  isBooked && 'calendar-day-booked',
                  !isBooked && isToday && 'calendar-day-today',
                  !isBooked && isHoliday && 'calendar-day-holiday',
                  !isBooked && isSunday && !isHoliday && 'text-[#FF385C]',
                )}
              >
                {day}
              </button>
            </div>
          )
        })}
      </div>

      {/* 예약률 바 */}
      <div className="mt-5 pt-4 border-t border-[#EBEBEB] dark:border-[#3A3A3C]">
        <div className="flex justify-between text-xs text-[#767676] mb-1.5">
          <span>이번 달 예약률</span>
          <span className="font-medium text-[#222222] dark:text-[#F5F5F5]">
            {(occupancyRate * 100).toFixed(0)}% ({bookedDays.size}/{daysInMonth}일)
          </span>
        </div>
        <div className="h-1.5 bg-[#EBEBEB] dark:bg-[#3A3A3C] rounded-full overflow-hidden">
          <div
            className="h-full bg-[#FF385C] rounded-full transition-all duration-300"
            style={{ width: `${occupancyRate * 100}%` }}
          />
        </div>
      </div>

      {/* 범례 */}
      <div className="flex items-center gap-4 mt-3 text-xs text-[#767676]">
        <div className="flex items-center gap-1.5">
          <div className="w-4 h-4 rounded-full bg-[#FF385C]" />
          <span>{t('bookedDays')}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-4 h-4 rounded-full border-2 border-current" />
          <span>{t('today')}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-[#FF385C] font-medium">31</span>
          <span>{t('holiday')}</span>
        </div>
      </div>
    </div>
  )
}
