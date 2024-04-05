from .crud_base import CRUDBase
from ..db.mongodb import expense_collection

expenses_crud = CRUDBase(expense_collection, "Expense")
