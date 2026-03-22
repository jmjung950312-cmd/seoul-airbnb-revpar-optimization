/* next-intl 프록시: 로케일 라우팅 처리 */

import createMiddleware from 'next-intl/middleware'
import { routing } from './i18n/routing'

export default createMiddleware(routing)

export const config = {
  matcher: [
    /* API 라우트 및 정적 파일 제외 */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\\..*).*)' ,
  ],
}
