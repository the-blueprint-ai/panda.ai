from databases import Database
from config import settings

database = Database(settings.PSQL_DATABASE_URL)

async def get_psql_database():
    await database.connect()
    try:
        yield database
    finally:
        await database.disconnect()