from pymongo import MongoClient
from ..core.settings.config import settings

client = MongoClient(settings.DB_URL)

database_name = settings.DATABASE_NAME

database = client[database_name]
user_collection = database.users
account_collection = database.accounts
asset_collection = database.assets
expense_collection = database.expenses
liability_collection = database.liabilities
goal_collection = database.goals