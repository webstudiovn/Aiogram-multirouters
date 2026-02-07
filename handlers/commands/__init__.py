__all__ = ("router",)

from aiogram import Router

from .base_commands import router as base_commands_router
from .user_commands import router as user_commands_router
from .admin_panel import router as admin_panel_router
from .acquaintances import router as acquaintances_router
from .handle_reactions import router as handle_reactions_router

router = Router(name=__name__)

router.include_routers(
    base_commands_router,
    user_commands_router,
    admin_panel_router,
    acquaintances_router,
    handle_reactions_router
)