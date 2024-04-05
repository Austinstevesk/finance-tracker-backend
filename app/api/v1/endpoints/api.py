from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as user_router
from .accounts import router as account_router
from .assets import router as asset_router
from .budgets import router as budget_router
from .expenses import router as expense_router
from .goals import router as goal_router
from .income import router as income_router
from .liabilities import router as liability_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(account_router)
router.include_router(income_router)
router.include_router(budget_router)
router.include_router(expense_router)
router.include_router(asset_router)
router.include_router(liability_router)
router.include_router(goal_router)
