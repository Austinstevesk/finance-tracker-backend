from app.crud.crud_base import CRUDBase
from app.db.mongodb import goal_collection

goals_crud = CRUDBase(goal_collection, "Goal")
