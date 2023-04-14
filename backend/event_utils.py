from fastapi import APIRouter
from dependencies import database

async def on_startup():
    await database.connect()

async def on_shutdown():
    await database.disconnect()

def register_events(router: APIRouter):
    router.add_event_handler("startup", on_startup)
    router.add_event_handler("shutdown", on_shutdown)