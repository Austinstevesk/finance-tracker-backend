from app.crud.crud_base import CRUDBase
from app.db.mongodb import account_collection

accounts_crud = CRUDBase(account_collection, "Account")
