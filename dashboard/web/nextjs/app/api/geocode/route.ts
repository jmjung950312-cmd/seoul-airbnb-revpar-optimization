/* Nominatim 지오코드 프록시 라우트 */

import { NextRequest, NextResponse } from 'next/server'

export async function GET(req: NextRequest) {
  const q = req.nextUrl.searchParams.get('q')

  if (!q) {
    return NextResponse.json({ error: '주소를 입력해주세요' }, { status: 400 })
  }

  const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(q)}&format=json&limit=1&accept-language=ko`

  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'SeoulAirbnbDashboard/1.0',
      },
      next: { revalidate: 3600 }, /* 1시간 캐시 */
    })

    const data = await res.json()

    if (!data.length) {
      return NextResponse.json({ error: '주소를 찾을 수 없습니다' }, { status: 404 })
    }

    const result = data[0]
    return NextResponse.json({
      lat: parseFloat(result.lat),
      lng: parseFloat(result.lon),
      display_name: result.display_name,
    })
  } catch {
    return NextResponse.json({ error: '지오코딩 실패' }, { status: 500 })
  }
}
