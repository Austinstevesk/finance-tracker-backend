from app.crud.crud_base import CRUDBase
from app.db.mongodb import income_collection

income_crud = CRUDBase(income_collection, "Income")
