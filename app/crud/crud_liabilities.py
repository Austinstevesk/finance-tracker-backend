from .crud_base import CRUDBase
from ..db.mongodb import liability_collection

liabilities_crud = CRUDBase(liability_collection, "Liability")
