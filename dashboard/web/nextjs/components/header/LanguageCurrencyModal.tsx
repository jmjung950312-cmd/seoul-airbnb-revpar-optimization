/* 에어비앤비 스타일 언어/통화 선택 모달 */

'use client'

import { useState } from 'react'
import { useTranslations } from 'next-intl'
import { useRouter, usePathname } from '@/i18n/navigation'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { Switch } from '@/components/ui/switch'
import { useLocaleStore } from '@/store/localeStore'
import { SUPPORTED_LANGUAGES, SUPPORTED_CURRENCIES } from '@/lib/constants'
import { cn } from '@/lib/utils'
import type { SupportedLocale, SupportedCurrency } from '@/types/locale'

interface LanguageCurrencyModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

/* 추천 언어 (상단 2개) */
const RECOMMENDED_LANGS: SupportedLocale[] = ['ko', 'en']
/* 추천 통화 (상단 4개) */
const RECOMMENDED_CURRENCIES: SupportedCurrency[] = ['KRW', 'USD', 'EUR', 'JPY']

export function LanguageCurrencyModal({ open, onOpenChange }: LanguageCurrencyModalProps) {
  const t = useTranslations('header')
  const { language, currency, setLanguage, setCurrency } = useLocaleStore()
  const [translationEnabled, setTranslationEnabled] = useState(true)
  const router = useRouter()
  const pathname = usePathname()

  const handleLanguageSelect = (code: SupportedLocale) => {
    setLanguage(code)
    router.replace(pathname, { locale: code })
    onOpenChange(false)
  }

  const handleCurrencySelect = (code: SupportedCurrency) => {
    setCurrency(code)
  }

  const recommendedLangs = SUPPORTED_LANGUAGES.filter(l => RECOMMENDED_LANGS.includes(l.code))
  const otherLangs = SUPPORTED_LANGUAGES.filter(l => !RECOMMENDED_LANGS.includes(l.code))

  const recommendedCurrs = SUPPORTED_CURRENCIES.filter(c => RECOMMENDED_CURRENCIES.includes(c.code))
  const otherCurrs = SUPPORTED_CURRENCIES.filter(c => !RECOMMENDED_CURRENCIES.includes(c.code))

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg max-h-[80vh] overflow-y-auto p-0 gap-0">
        <DialogHeader className="px-6 pt-6 pb-0">
          <DialogTitle className="text-lg font-semibold">{t('languageAndRegion')}</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="language" className="w-full">
          {/* 탭 헤더 */}
          <div className="px-6 pt-4 border-b border-[#DDDDDD] dark:border-[#3A3A3C]">
            <TabsList className="bg-transparent p-0 h-auto gap-6">
              <TabsTrigger
                value="language"
                className="bg-transparent px-0 pb-3 rounded-none border-b-2 border-transparent data-[state=active]:border-[#222222] data-[state=active]:text-[#222222] dark:data-[state=active]:border-white dark:data-[state=active]:text-white font-medium text-[#767676] data-[state=active]:bg-transparent data-[state=active]:shadow-none"
              >
                {t('languageAndRegion')}
              </TabsTrigger>
              <TabsTrigger
                value="currency"
                className="bg-transparent px-0 pb-3 rounded-none border-b-2 border-transparent data-[state=active]:border-[#222222] data-[state=active]:text-[#222222] dark:data-[state=active]:border-white dark:data-[state=active]:text-white font-medium text-[#767676] data-[state=active]:bg-transparent data-[state=active]:shadow-none"
              >
                {t('currency')}
              </TabsTrigger>
            </TabsList>
          </div>

          {/* 언어 탭 */}
          <TabsContent value="language" className="px-6 py-5 space-y-6 mt-0">
            {/* 번역 토글 */}
            <div className="flex items-center justify-between py-3 border-b border-[#DDDDDD] dark:border-[#3A3A3C]">
              <div>
                <p className="font-medium text-sm">{t('translation')}</p>
                <p className="text-xs text-[#767676] mt-0.5">{t('translationDesc')}</p>
              </div>
              <Switch
                checked={translationEnabled}
                onCheckedChange={setTranslationEnabled}
                className="data-[state=checked]:bg-[#222222]"
              />
            </div>

            {/* 추천 언어 */}
            <div>
              <p className="text-xs font-semibold text-[#767676] uppercase tracking-wide mb-3">
                {t('recommendedLanguages')}
              </p>
              <div className="grid grid-cols-2 gap-2">
                {recommendedLangs.map(lang => (
                  <LanguageCard
                    key={lang.code}
                    lang={lang}
                    selected={language === lang.code}
                    onSelect={() => handleLanguageSelect(lang.code)}
                  />
                ))}
              </div>
            </div>

            {/* 전체 언어 */}
            <div>
              <p className="text-xs font-semibold text-[#767676] uppercase tracking-wide mb-3">
                {t('allLanguages')}
              </p>
              <div className="grid grid-cols-2 gap-2">
                {otherLangs.map(lang => (
                  <LanguageCard
                    key={lang.code}
                    lang={lang}
                    selected={language === lang.code}
                    onSelect={() => handleLanguageSelect(lang.code)}
                  />
                ))}
              </div>
            </div>
          </TabsContent>

          {/* 통화 탭 */}
          <TabsContent value="currency" className="px-6 py-5 space-y-6 mt-0">
            {/* 추천 통화 */}
            <div>
              <p className="text-xs font-semibold text-[#767676] uppercase tracking-wide mb-3">
                {t('recommendedCurrencies')}
              </p>
              <div className="grid grid-cols-2 gap-2">
                {recommendedCurrs.map(curr => (
                  <CurrencyCard
                    key={curr.code}
                    curr={curr}
                    selected={currency === curr.code}
                    onSelect={() => handleCurrencySelect(curr.code)}
                  />
                ))}
              </div>
            </div>

            {/* 전체 통화 */}
            <div>
              <p className="text-xs font-semibold text-[#767676] uppercase tracking-wide mb-3">
                {t('allCurrencies')}
              </p>
              <div className="grid grid-cols-2 gap-2">
                {otherCurrs.map(curr => (
                  <CurrencyCard
                    key={curr.code}
                    curr={curr}
                    selected={currency === curr.code}
                    onSelect={() => handleCurrencySelect(curr.code)}
                  />
                ))}
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  )
}

/* ============================================
   언어 카드
   ============================================ */
function LanguageCard({
  lang,
  selected,
  onSelect,
}: {
  lang: (typeof SUPPORTED_LANGUAGES)[0]
  selected: boolean
  onSelect: () => void
}) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className={cn(
        'flex items-start gap-3 p-3 rounded-lg border text-left transition-all',
        selected
          ? 'border-[#222222] dark:border-white bg-[#F7F7F7] dark:bg-[#3A3A3C]'
          : 'border-[#DDDDDD] dark:border-[#3A3A3C] hover:bg-[#F7F7F7] dark:hover:bg-[#2C2C2E]',
      )}
    >
      <span className="text-xl leading-none">{lang.flag}</span>
      <div>
        <p className="text-sm font-medium leading-tight">{lang.label}</p>
        <p className="text-xs text-[#767676] mt-0.5">{lang.region}</p>
      </div>
      {selected && (
        <span className="ml-auto text-[#222222] dark:text-white">✓</span>
      )}
    </button>
  )
}

/* ============================================
   통화 카드
   ============================================ */
function CurrencyCard({
  curr,
  selected,
  onSelect,
}: {
  curr: (typeof SUPPORTED_CURRENCIES)[0]
  selected: boolean
  onSelect: () => void
}) {
  return (
    <button
      type="button"
      onClick={onSelect}
      className={cn(
        'flex items-center justify-between p-3 rounded-lg border text-left transition-all',
        selected
          ? 'border-[#222222] dark:border-white bg-[#F7F7F7] dark:bg-[#3A3A3C]'
          : 'border-[#DDDDDD] dark:border-[#3A3A3C] hover:bg-[#F7F7F7] dark:hover:bg-[#2C2C2E]',
      )}
    >
      <div>
        <p className="text-sm font-medium">{curr.code} – {curr.symbol}</p>
        <p className="text-xs text-[#767676] mt-0.5">{curr.name}</p>
      </div>
      {selected && (
        <span className="text-[#222222] dark:text-white text-sm">✓</span>
      )}
    </button>
  )
}
