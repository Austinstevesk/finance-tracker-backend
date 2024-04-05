from .crud_base import CRUDBase
from ..db.mongodb import account_collection

accounts_crud = CRUDBase(account_collection, "Account")
