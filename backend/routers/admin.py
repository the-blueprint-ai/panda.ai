from fastapi import APIRouter, HTTPException, Depends
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependencies import database
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from event_utils import register_events
import logging

# CONFIG
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

register_events(router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ROUTERS
@router.get("/check", response_model=bool)
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
