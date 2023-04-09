from fastapi import APIRouter, Depends
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from pydantic import BaseModel
from datetime import datetime
import logging

from functions.faqFunctions import get_faqs, update_faqs_on_db, add_faq_to_db


# CONFIG
router = APIRouter(
    prefix="/faqs",
    tags=["faqs"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FAQsItem(BaseModel):
    title: str
    question: str
    answer: str
    visible: bool


# ROUTERS
@router.get("/get")
async def fetch_faqs(session: SessionContainer = Depends(verify_session())):
    result = await get_faqs(session)
    return result

@router.get("/delete")
async def delete_faqs(item: FAQsItem, session: SessionContainer = Depends(verify_session())):
    result = await delete_faqs_from_db(item, session)
    return result

@router.post("/add")
async def add_faqs(item: FAQsItem, session: SessionContainer = Depends(verify_session())):
    result = await add_faq_to_db(item, session)
    return result

@router.post("/update")
async def update_faqs(item: FAQsItem, session: SessionContainer = Depends(verify_session())):
    logging.info(f"Received payload: {item}")
    result = await update_faqs_on_db(item, session)
    return result