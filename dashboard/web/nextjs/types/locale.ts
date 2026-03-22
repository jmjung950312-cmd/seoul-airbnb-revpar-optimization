/* 언어 및 통화 관련 타입 정의 */

export type SupportedLocale = 'ko' | 'en' | 'ja' | 'zh' | 'es' | 'de' | 'fr'

export type SupportedCurrency = 'KRW' | 'USD' | 'EUR' | 'JPY' | 'CNY' | 'GBP' | 'SGD' | 'AUD'

export interface LanguageOption {
  code: SupportedLocale
  label: string
  region: string
  flag: string
}

export interface CurrencyOption {
  code: SupportedCurrency
  symbol: string
  name: string
  locale: string
}
