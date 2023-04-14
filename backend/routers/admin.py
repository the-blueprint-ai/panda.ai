from fastapi import APIRouter, HTTPException, Depends
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependencies import database
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from event_utils import register_events
from pydantic import ValidationError, BaseModel
import logging
from datetime import datetime
from typing import List

from functions.adminFunctions import get_roadmap, update_roadmap, add_roadmap_item, topline_user_stats, users_by_day_stats, topline_onboarding_stats, onboarding_by_day_stats, topline_chat_stats, chat_by_day_stats, topline_entity_stats, entity_by_day_stats

# CONFIG
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

register_events(router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Roadmap(BaseModel):
    roadmap_id: int
    created_at: datetime
    name: str
    description: str
    tags: List[str]
    votes: int
    reviewed: bool
    email: str

# ROUTERS
@router.get("/check-admin", response_model=bool)
async def check_admin_route(user_id: str, session: SessionContainer = Depends(verify_session())):
    try:
        query = "SELECT admin FROM panda_ai_users WHERE user_id = :user_id AND admin = true"
        values = {"user_id": user_id}
        response = await database.fetch_one(query=query, values=values)
        if response:
            return True
        else:
            return False
    except HTTPException as e:
        logger.error(f"HTTPException in check_admin_route: {e}, type: {type(e)}, args: {e.args}")
        raise e
    except Exception as e:
        logger.error(f"Error in check_admin_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.get("/roadmap")
async def get_roadmap_route(session: SessionContainer = Depends(verify_session())):
    try:
        data = await get_roadmap()
        if data:
            return data
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except ValidationError as e:
        logger.error(f"ValidationError in get_roadmap_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in get_roadmap_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.put("/update-roadmap")
async def update_roadmap_route(roadmap_id: int, roadmap: Roadmap, session: SessionContainer = Depends(verify_session())):
    try:
        response = await update_roadmap(roadmap_id, roadmap)
        if response:
            return response
        else:
            raise HTTPException(status_code=404, detail="Roadmap ID not found")
    except ValidationError as e:
        logger.error(f"ValidationError in update_roadmap_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.put("/add-roadmap-idea")
async def add_roadmap_idea_route(name: str, description: str, session: SessionContainer = Depends(verify_session())):
    try:
        updated_item = await add_roadmap_item(name, description)
        if updated_item:
            return updated_item
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except ValidationError as e:
        logger.error(f"ValidationError in add_roadmap_idea_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in add_roadmap_idea_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/user-stats")
async def get_user_stats_route(session: SessionContainer = Depends(verify_session())):
    try:
        topline_user = await topline_user_stats()
        daily_user = await users_by_day_stats()
        topline_onboarding = await topline_onboarding_stats()
        daily_onboarding = await onboarding_by_day_stats()
        topline_chats = await topline_chat_stats()
        daily_chats = await chat_by_day_stats()
        topline_entities = await topline_entity_stats()
        daily_entities = await entity_by_day_stats()

        if topline_user is not None and daily_user is not None and topline_onboarding is not None and daily_onboarding is not None and topline_chats is not None and daily_chats is not None and topline_entities is not None and daily_entities is not None:
            return {
                "topline_user_stats": topline_user,
                "users_by_day_stats": daily_user,
                "topline_onboarding_stats": topline_onboarding,
                "onboarding_by_day_stats": daily_onboarding,
                "topline_chat_stats": topline_chats,
                "chats_by_day_stats": daily_chats,
                "topline_entity_stats": topline_entities,
                "entities_created_by_day_stats": daily_entities
            }
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except ValidationError as e:
        logger.error(f"ValidationError in get_user_stats_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in get_user_stats_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)