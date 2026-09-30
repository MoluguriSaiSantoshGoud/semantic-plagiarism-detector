from app.routers.auth import auth_router
from app.routers.documents import documents_router
from app.routers.comparisons import comparisons_router
from app.routers.reports import reports_router
from app.routers.dashboard import dashboard_router

__all__ = ["auth_router", "documents_router", "comparisons_router", "reports_router", "dashboard_router"]
