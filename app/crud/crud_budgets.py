from app.crud.crud_base import CRUDBase
from app.db.mongodb import budget_collection

budgets_crud = CRUDBase(budget_collection, "Budget")
