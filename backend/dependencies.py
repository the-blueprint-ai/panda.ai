from fastapi import Depends
from databases import Database
from config import settings

DATABASE_URL = settings.PSQL_DATABASE_URL
database = Database(DATABASE_URL)

async def connect_db():
    if not database.is_connected:
        await database.connect()
    return database

async def disconnect_db(db: Database = Depends(connect_db)):
    if db.is_connected:
        await db.disconnect()