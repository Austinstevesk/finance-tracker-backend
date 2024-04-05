from .crud_base import CRUDBase
from ..db.mongodb import goal_collection

goals_crud = CRUDBase(goal_collection, "Goal")
