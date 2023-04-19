from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from fastapi import APIRouter, Depends
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
async def send_email(from_email: str, to_emails: str, subject: str, html_content: str, session: SessionContainer = Depends(verify_session())):
    result = await email_send(from_email, to_emails, subject, html_content)
    return result

@router.post("/support")
async def send_email(from_email: str, to_emails: str, subject: str, html_content: str):
    result = await email_send(from_email, to_emails, subject, html_content)
    return result