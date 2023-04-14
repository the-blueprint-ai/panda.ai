from fastapi import APIRouter
import logging

from functions.emailFunctions import email_send


# CONFIG
router = APIRouter(
    prefix="/email",
    tags=["email"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ROUTERS
@router.post("/send")
async def send_email():
    result = await email_send()
    return result
