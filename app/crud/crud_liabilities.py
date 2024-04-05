from app.crud.crud_base import CRUDBase
from app.db.mongodb import liability_collection

liabilities_crud = CRUDBase(liability_collection, "Liability")
