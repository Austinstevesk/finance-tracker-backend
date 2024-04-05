from .crud_base import CRUDBase
from ..db.mongodb import asset_collection

assets_crud = CRUDBase(asset_collection, "Asset")
