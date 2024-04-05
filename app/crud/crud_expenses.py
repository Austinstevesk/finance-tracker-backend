from app.crud.crud_base import CRUDBase
from app.db.mongodb import expense_collection

expenses_crud = CRUDBase(expense_collection, "Expense")
