from fastapi import APIRouter, Depends
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from config import settings
import os
import openai
import logging
import httpx

# CONFIG
router = APIRouter(
    prefix="/gpt",
    tags=["gpt"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ROUTERS
@router.get("/chat")
async def send_gpt_request(userid: str, message: str, session: SessionContainer = Depends(verify_session())):
    

    return response.json()

@router.get("/gpt-chat")
async def send_gpt_request(message: str, session: SessionContainer = Depends(verify_session())):
    OPENAI_API_KEY = settings.OPENAI_API_KEY
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.7,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            json=data,
            headers=headers,
        )

    return response.json()