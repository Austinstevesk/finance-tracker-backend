from pydantic import BaseModel
from app.schemas.base import PyObjectId
from app.schemas.users import (
    ExtendedUserInSignup,
    LoginData,
    UserInDB,
    UserInLogin,
    UserInSignUp,
    UserInResponse,
    UserInUpdate
)

from app.schemas.accounts import (
    Account,
    AccountCreate,
    AccountInResponse,
    AccountInUpdate,
)

from app.schemas.budgets import (
    BudgetCreate,
    BudgetInResponse,
    BudgetInUpdate,
    ExtendedBudgetCreate,
)

from app.schemas.assets import(
    AssetCreate,
    AssetInResponse,
    AssetInUpdate,
    ExtendedAssetCreate,
)

from app.schemas.expenses import(
    ExpenseCreate,
    ExpenseInResponse,
    ExpenseInUpdate,
    ExtendedExpenseCreate,
)

from app.schemas.goals import (
    ExtendedGoalCreate,
    GoalCreate,
    GoalInResponse,
    GoalInUpdate,
)

from app.schemas.income import (
    ExtendedIncomeCreate,
    IncomeCreate,
    IncomeInResponse,
    IncomeInUpdate,
)

from app.schemas.liabilities import (
    ExtendedLiabilityCreate,
    LiabilityCreate,
    LiabilityInResponse,
    LiabilityInUpdate,
)

class TotalDisplay(BaseModel):
    total: int