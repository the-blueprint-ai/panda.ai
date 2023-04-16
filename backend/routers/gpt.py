from fastapi import APIRouter, Depends
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
import logging
from functions.chatFunctions import pandaChatAgent

# CONFIG
router = APIRouter(
    prefix="/gpt",
    tags=["gpt"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ROUTERS
@router.get("/chat")
async def send_gpt_request(userid: str, first_name: str, last_name: str, username: str, message: str, session: SessionContainer = Depends(verify_session())):
    result = await pandaChatAgent(userid, first_name, last_name, username, message)
    return result
