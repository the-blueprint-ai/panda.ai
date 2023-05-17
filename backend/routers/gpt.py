from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from pydantic import BaseModel, ValidationError
import logging
from functions.chatFunctions import pandaChatAgent, rate_message, feedback_message

# CONFIG
router = APIRouter(
    prefix="/gpt",
    tags=["gpt"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Rating(BaseModel):
    user_id: str
    message: str
    rating: str

class Feedback(BaseModel):
    user_id: str
    message: str
    rating: str
    feedback: str

# ROUTERS
@router.get("/chat")
async def send_gpt_request(user_id: str, first_name: str, last_name: str, username: str, message: str, session: SessionContainer = Depends(verify_session())):
    try:
        result = await pandaChatAgent(user_id, first_name, last_name, username, message)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Message not sent")
    except ValidationError as e:
        logger.error(f"ValidationError in send_gpt_request: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in send_gpt_request: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.put("/message-rating")
async def rate_message_route(rating_data: Rating, session: SessionContainer = Depends(verify_session())):
    try:
        result = await rate_message(rating_data.user_id, rating_data.message, rating_data.rating)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Message not rated")
    except ValidationError as e:
        logger.error(f"ValidationError in rate_message_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in rate_message_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.put("/message-feedback")
async def feedback_message_route(feedback_data: Feedback, session: SessionContainer = Depends(verify_session())):
    try:
        result = await feedback_message(feedback_data.user_id, feedback_data.message, feedback_data.rating, feedback_data.feedback)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Message not rated")
    except ValidationError as e:
        logger.error(f"ValidationError in feedback_message_route: {e}, details: {e.errors()}")
        return JSONResponse(content={"error": "Validation error", "details": e.errors()}, status_code=400)
    except Exception as e:
        logger.error(f"Error in feedback_message_route: {e}, type: {type(e)}, args: {e.args}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
