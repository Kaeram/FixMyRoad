"""API package."""
from .reports import router as reports_router
from .admin import router as admin_router
from .public import router as public_router

__all__ = ["reports_router", "admin_router", "public_router"]
