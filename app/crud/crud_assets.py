from app.crud.crud_base import CRUDBase
from app.db.mongodb import asset_collection

assets_crud = CRUDBase(asset_collection, "Asset")
