from wheke import Pod, ServiceConfig

from wheke_auth.cli import cli
from wheke_auth.routes import router
from wheke_auth.security import get_current_active_user
from wheke_auth.service import AuthService, auth_service_factory

auth_pod = Pod(
    "auth",
    router=router,
    services=[ServiceConfig(AuthService, auth_service_factory)],
    cli=cli,
)

__all__ = [
    "auth_pod",
    "get_current_active_user",
]
