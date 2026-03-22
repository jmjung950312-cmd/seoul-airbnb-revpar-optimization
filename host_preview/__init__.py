"""
host_preview
============
호스트 진단 프리뷰 이메일 자동 생성 패키지.

리드 제너레이션 목적 — 호스트가 자기 숙소의 수익 진단을 간략히 확인하고
전체 대시보드로 유입되도록 유도합니다.

빠른 시작
---------
  from host_preview.hooks import run_preview_scan
  run_preview_scan()
"""

from .analyzer import build_preview_report
from .email_builder import build_host_email, send_demo_emails

__all__ = ['build_preview_report', 'build_host_email', 'send_demo_emails']
