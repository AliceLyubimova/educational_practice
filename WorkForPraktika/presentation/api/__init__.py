"""
API роуты
Каждый модуль — отдельная группа эндпоинтов.
"""

from presentation.api.auth_routes import router as auth_router
from presentation.api.user_routes import router as user_router
from presentation.api.ahp_routes import router as ahp_router
from presentation.api.compatibility_routes import router as compatibility_router
from presentation.api.like_routes import router as like_router
from presentation.api.photo_routes import router as photo_router
from presentation.api.comment_routes import router as comment_router

__all__ = [
    "auth_router",
    "user_router",
    "ahp_router",
    "compatibility_router",
    "like_router",
    "photo_router",
    "comment_router",
]
