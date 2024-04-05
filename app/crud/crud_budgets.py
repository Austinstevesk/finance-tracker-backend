from .crud_base import CRUDBase
from ..db.mongodb import budget_collection

budgets_crud = CRUDBase(budget_collection, "Budget")
