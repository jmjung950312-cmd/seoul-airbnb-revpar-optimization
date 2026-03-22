/* next-intl 라우팅 설정 */

import { defineRouting } from 'next-intl/routing'

export const routing = defineRouting({
  locales: ['ko', 'en', 'ja', 'zh', 'es', 'de', 'fr'],
  defaultLocale: 'ko',
})
