from .echo import echo_router
from .user import user_router
from .admin.menu import admin_router
from .groups import group_router

__all__ = [
    "echo_router",
    "user_router",
    "admin_router",
    "group_router"
]
