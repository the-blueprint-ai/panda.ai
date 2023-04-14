from fastapi import Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from config import settings
import logging
from pydantic import BaseModel
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
    title: str
    question: str
    answer: str
    visible: bool


# FUNCTIONS
async def get_faqs():
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

async def update_faqs_on_db(faq: FAQsItem, session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-faqs')
    
    # Update the FAQ record in the table
    response = table.update_item(
        Key={
            'title': faq.title,
            'question': faq.question,
        },
        UpdateExpression='SET answer = :answer, visible = :visible',
        ExpressionAttributeValues={
            ':answer': faq.answer,
            ':visible': faq.visible,
        },
    )
    
    # Check if the update was successful
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise HTTPException(status_code=500, detail="Error updating FAQ data.")
    
    # Return a success message
    return {"message": "FAQ data updated successfully."}

async def add_faq_to_db(faq: FAQsItem, session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-faqs')
    
    # Add the FAQ to the table
    response = table.put_item(
        Item={
            'title': faq.title,
            'question': faq.question,
            'answer': faq.answer,
            'visible': faq.visible,
        }
    )
    
    # Check if the update was successful
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise HTTPException(status_code=500, detail="Error updating FAQ data.")
    
    # Return a success message
    return {"message": "FAQ added successfully."}
