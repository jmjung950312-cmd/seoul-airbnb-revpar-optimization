"""
predict_utils.py — shared/predict_utils.py의 래퍼
==================================================
단일 소스: shared/predict_utils.py
이 파일은 기존 import 경로 호환성을 유지하기 위한 래퍼입니다.
"""

import sys
from pathlib import Path

# shared 패키지 경로를 sys.path에 추가
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# 모델 경로: 이 패키지(revpar_model_package) 내부의 models/ 폴더
_LOCAL_MODELS_DIR = Path(__file__).parent / "models"
if not _LOCAL_MODELS_DIR.exists():
    _LOCAL_MODELS_DIR = _PROJECT_ROOT / "models"

from shared.predict_utils import (  # noqa: E402, F401
    load_models,
    predict_revpar,
    compute_health_score,
    get_poi_dist_category,
)

# load_models의 기본 경로를 로컬 models/로 오버라이드하는 래퍼
_original_load_models = load_models

def load_models(models_dir=None):
    """로컬 models/ 폴더를 기본 경로로 사용"""
    return _original_load_models(models_dir or _LOCAL_MODELS_DIR)
