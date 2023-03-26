from fastapi import APIRouter, HTTPException, Depends
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from config import settings
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet
from databases import Database
from pydantic import Json
import logging
import json
from typing import Any

# CONFIG
router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)

DATABASE_URL = settings.PSQL_DATABASE_URL
database = Database(DATABASE_URL)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect/Disconnect from Aurora
@router.on_event("startup")
async def startup():
    await database.connect()

@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# ROUTERS
@router.get("/get")
async def get_user_chat_history_route(user_id: str, session: SessionContainer = Depends(verify_session())):
    try:
        data = await get_user_chat_history(user_id)
        if data:
            return data
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"Error in get_user_chat_history_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/save")
async def save_user_chat_history_route(user_id: str, chat_script: str, session: SessionContainer = Depends(verify_session())):
    try:
        response = await save_user_chat_history(user_id, chat_script)
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        return {"message": "Data saved successfully"}
    except Exception as e:
        logger.error(f"Error in save_user_chat_history_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

# FUNCTIONS
async def get_user_chat_history(user_id: str):
    query = "SELECT user_id, created_at, chat_script FROM panda_ai_chat_history WHERE user_id = :user_id"
    values = {"user_id": user_id}
    results = await database.fetch_all(query=query, values=values)

    if results:
        chat_history = []
        for result in results:
            user_id = result["user_id"]
            created_at = result["created_at"]
            chat_script = json.loads(result["chat_script"]) # Convert the JSON string back to a list of dictionaries

            chat_history.append({
                "user_id": user_id,
                "created_at": created_at,
                "chat_script": chat_script,
            })

        return chat_history
    else:
        return None

async def save_user_chat_history(user_id: str, chat_script: Json[Any]):
    query = """
        INSERT INTO panda_ai_chat_history (user_id, chat_script)
        VALUES (:user_id, :chat_script)
    """
    values = {
        "user_id": user_id,
        "chat_script": json.dumps(chat_script)  # Convert the list of dictionaries to a JSON string
    }
    await database.execute(query=query, values=values)