from fastapi import APIRouter, HTTPException, Depends
from dependencies import database
from event_utils import register_events
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from config import settings
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet
from pydantic import Json, BaseModel, ValidationError
import logging
import json
from typing import Any

# CONFIG
router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)

register_events(router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SaveUserChatHistoryRequest(BaseModel):
    user_id: str
    chat_script: Json[Any]

class UpdateUserChatHistoryRequest(BaseModel):
    chat_id: int
    chat_script: Json[Any]


# ROUTERS
@router.get("/get")
async def get_user_chat_history_route(user_id: str, session: SessionContainer = Depends(verify_session())):
    try:
        data = await get_user_chat_history(user_id)
        if data:
            return data
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except ValidationError as e:
        logger.error(f"ValidationError in get_user_chat_history_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in get_user_chat_history_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/save")
async def save_user_chat_history_route(data: SaveUserChatHistoryRequest, session: SessionContainer = Depends(verify_session())):
    try:
        response = await save_user_chat_history(data.user_id, data.chat_script)
        return response
    except ValidationError as e:
        logger.error(f"ValidationError in save_user_chat_history_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in save_user_chat_history_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/update")
async def update_user_chat_history_route(data: UpdateUserChatHistoryRequest, session: SessionContainer = Depends(verify_session())):
    try:
        response = await update_user_chat_history(data.chat_id, data.chat_script)
        return response
    except ValidationError as e:
        logger.error(f"ValidationError in update_user_chat_history_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in update_user_chat_history_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

# FUNCTIONS
async def get_user_chat_history(user_id: str):
    query = "SELECT user_id, created_at, chat_script FROM panda_ai_user_chat_history WHERE user_id = :user_id ORDER BY created_at DESC"
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
        INSERT INTO panda_ai_user_chat_history (user_id, chat_script)
        VALUES (:user_id, :chat_script)
        RETURNING chat_id
    """
    values = {
        "user_id": user_id,
        "chat_script": json.dumps(chat_script)  # Convert the list of dictionaries to a JSON string
    }
    chat_id = await database.execute(query=query, values=values)
    print("Data saved successfully")
    return {"message": "Data saved successfully", "chat_id": chat_id}

async def update_user_chat_history(chat_id: int, chat_script: Json[Any]):
    query = """
        UPDATE panda_ai_user_chat_history
        SET chat_script = :chat_script
        WHERE chat_id = :chat_id
    """
    values = {
        "chat_id": chat_id,
        "chat_script": json.dumps(chat_script)  # Convert the list of dictionaries to a JSON string
    }
    await database.execute(query=query, values=values)
    return {"message": "Chat history updated successfully"}
