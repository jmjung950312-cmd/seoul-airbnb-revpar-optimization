/* 숙소 설명 섹션 */

'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { Copy, Check, RefreshCw } from 'lucide-react'
import { SectionCard } from '@/components/common/SectionCard'
import { useResultsStore } from '@/store/resultsStore'

export function ListingDescSection() {
  const t = useTranslations('dashboard.listingDesc')
  const { results } = useResultsStore()
  const [copied, setCopied] = useState(false)

  if (!results?.listingDescription) return null

  const handleCopy = async () => {
    await navigator.clipboard.writeText(results.listingDescription)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <SectionCard
      id="description"
      title={t('title')}
      action={
        <div className="flex gap-2">
          <button
            type="button"
            onClick={handleCopy}
            className="flex items-center gap-1.5 text-xs font-medium text-[#484848] dark:text-[#EBEBEB] hover:text-[#222222] dark:hover:text-white px-3 py-1.5 rounded-lg border border-[#DDDDDD] dark:border-[#3A3A3C] hover:border-[#222222] dark:hover:border-white transition-all"
          >
            {copied ? <Check size={13} className="text-[#00A699]" /> : <Copy size={13} />}
            {copied ? '복사됨' : t('copy')}
          </button>
        </div>
      }
    >
      <div className="bg-[#F7F7F7] dark:bg-[#3A3A3C] rounded-xl p-5">
        <p className="text-xs font-semibold text-[#767676] uppercase tracking-wide mb-3">
          {t('generated')}
        </p>
        <p className="text-sm text-[#484848] dark:text-[#EBEBEB] leading-relaxed whitespace-pre-wrap">
          {results.listingDescription}
        </p>
      </div>
    </SectionCard>
  )
}
