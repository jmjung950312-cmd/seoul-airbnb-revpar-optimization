/* 에어비앤비 스타일 섹션 카드 */

import { cn } from '@/lib/utils'

interface SectionCardProps {
  id?: string
  title?: string
  subtitle?: string
  action?: React.ReactNode
  children: React.ReactNode
  className?: string
}

export function SectionCard({ id, title, subtitle, action, children, className }: SectionCardProps) {
  return (
    <section
      id={id}
      className={cn(
        'bg-white dark:bg-[#2C2C2E] border border-[#DDDDDD] dark:border-[#3A3A3C] rounded-xl p-6',
        className,
      )}
    >
      {(title || action) && (
        <div className="flex items-start justify-between mb-5">
          <div>
            {title && (
              <h2 className="text-lg font-semibold text-[#222222] dark:text-[#F5F5F5]">{title}</h2>
            )}
            {subtitle && (
              <p className="text-sm text-[#767676] mt-0.5">{subtitle}</p>
            )}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      {children}
    </section>
  )
}
