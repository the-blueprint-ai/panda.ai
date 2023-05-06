from config import settings
from databases import Database

# DATABASES
DATABASE_URL = settings.PSQL_DATABASE_URL
database = Database(DATABASE_URL)


# SUBSCRIPTION FUNCTIONS
async def get_user_messages_this_month(user_id: str):
    query = "SELECT COUNT(*) AS count FROM panda_ai_messages WHERE user_id = :user_id AND success = true AND EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM NOW()) AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM NOW())"
    values = {"user_id": user_id}
    result = await database.fetch_one(query=query, values=values)

    return result

async def get_user_messages_per_month(user_id: str):
    query = "SELECT messages_per_month FROM panda_ai_users WHERE user_id = :user_id"
    values = {"user_id": user_id}
    result = await database.fetch_one(query=query, values=values)

    return result