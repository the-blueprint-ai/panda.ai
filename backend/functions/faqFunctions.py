from fastapi import Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from config import settings
from cryptography.fernet import Fernet
from typing import Optional
import logging
from pydantic import BaseModel
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key


# DATABASES
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FAQsItem(BaseModel):
    userId: str
    entity: str
    description: str
    updated: datetime


# FUNCTIONS
async def get_faqs(session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-faqs')
    response = table.scan()
    items = response.get('Items', [])

    if not items:
        return {"message": "No FAQs available"}

    faqs = []
    for item in items:
        faq = {
            "title": item.get("title", ""),
            "question": item.get("question", ""),
            "answer": item.get("answer", ""),
            "visible": item.get("visible", "")
        }
        faqs.append(faq)

    return faqs
