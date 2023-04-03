from fastapi import APIRouter, HTTPException, Depends
from dependencies import database
from event_utils import register_events
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import logging

# CONFIG
router = APIRouter(
    prefix="/roadmap",
    tags=["roadmap"],
)

register_events(router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ROUTERS
@router.get("/get")
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
    
@router.put("/upvote")
async def upvote_item_route(id: int):
    try:
        updated_item = await upvote_item(id)
        if updated_item:
            return updated_item
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except ValidationError as e:
        logger.error(f"ValidationError in upvote_item_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in upvote_item_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.put("/add-idea")
async def add_item_route(idea: str):
    try:
        updated_item = await add_item(idea)
        if updated_item:
            return updated_item
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except ValidationError as e:
        logger.error(f"ValidationError in add_item_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in add_item_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.put("/add-email")
async def add_email_route(id: int, email: str):
    try:
        updated_email = await add_email(id, email)
        if updated_email:
            return updated_email
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except ValidationError as e:
        logger.error(f"ValidationError in add_email_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in add_email_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


# FUNCTIONS
async def get_roadmap():
    query = "SELECT roadmap_id, created_at, name, description, tags, votes, reviewed, email FROM panda_ai_roadmap WHERE reviewed = true ORDER BY roadmap_id;"
    results = await database.fetch_all(query=query)

    if results:
        return results
    else:
        return None
    
async def upvote_item(id: int):
    # Check if the item exists in the database
    query = "SELECT votes FROM panda_ai_roadmap WHERE roadmap_id = :id"
    result = await database.fetch_one(query=query, values={"id": id})

    if not result:
        raise HTTPException(status_code=404, detail="Item not found")

    # Increment the vote count
    new_votes = result["votes"] + 1

    # Update the vote count in the database
    query = "UPDATE panda_ai_roadmap SET votes = :new_votes WHERE roadmap_id = :id"
    await database.execute(query=query, values={"id": id, "new_votes": new_votes})

    # Fetch the updated item from the database
    query = "SELECT roadmap_id, name, description, tags, votes FROM panda_ai_roadmap WHERE roadmap_id = :id"
    updated_item = await database.fetch_one(query=query, values={"id": id})

    return updated_item

async def add_item(idea: str):

    # Insert new idea into the database
    query = """
        INSERT INTO panda_ai_roadmap (name, description, tags, votes, reviewed, email)
        VALUES ('TBC', :idea, '["newly added"]'::jsonb, 0, false, 'admin@mypanda.ai');"""
    await database.execute(query=query, values={"idea": idea})

    # Get the ID of the newly inserted item
    query = """
        SELECT roadmap_id FROM panda_ai_roadmap
        WHERE description = :idea
        ORDER BY roadmap_id DESC
        LIMIT 1;"""
    result = await database.fetch_one(query=query, values={"idea": idea})

    return {"message": "User idea successfully added to database", "roadmap_id": result["roadmap_id"]}

async def add_email(id: int, email: str):

    # Update database with email
    query = "UPDATE panda_ai_roadmap SET email = :email WHERE roadmap_id = :id"
    await database.execute(query=query, values={"id": id, "email": email})

    return {"message": "User email successfully added to database"}