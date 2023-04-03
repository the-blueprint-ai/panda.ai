from fastapi import APIRouter, HTTPException, Depends
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependencies import database
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from event_utils import register_events
from pydantic import ValidationError, BaseModel
import logging
import json
from datetime import datetime
from typing import List

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
async def get_roadmap_route():
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
async def update_roadmap_route(roadmap_id: int, roadmap: Roadmap):
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

# FUNCTIONS
async def get_roadmap():
    query = "SELECT roadmap_id, created_at, name, description, tags, votes, reviewed, email FROM panda_ai_roadmap ORDER BY roadmap_id;"
    results = await database.fetch_all(query=query)

    if results:
        return results
    else:
        return None

async def update_roadmap(roadmap_id: int, roadmap: Roadmap):
    query = """
        UPDATE panda_ai_roadmap
        SET name = :name, description = :description, tags = :tags, votes = :votes, reviewed = :reviewed, email = :email
        WHERE roadmap_id = :roadmap_id
    """
    values = {
        "roadmap_id": roadmap_id,
        "name": roadmap.name,
        "description": roadmap.description,
        "tags": json.dumps(roadmap.tags), # convert tags list to JSON string
        "votes": roadmap.votes,
        "reviewed": roadmap.reviewed,
        "email": roadmap.email,
    }
    try:
        await database.execute(query=query, values=values)
        return {"message": "Roadmap updated successfully"}
    except Exception as e:
        logger.error(f"Error in update_roadmap: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")