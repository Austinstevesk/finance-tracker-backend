from .crud_base import CRUDBase
from ..db.mongodb import income_collection

income_crud = CRUDBase(income_collection, "Income")
