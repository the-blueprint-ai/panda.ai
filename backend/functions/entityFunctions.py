from fastapi import Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from config import settings
from cryptography.fernet import Fernet
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

key = settings.FERNET_KEY
if not key:
    raise ValueError("FERNET_KEY environment variable not set")
cipher_suite = Fernet(key.encode())

class EntityItem(BaseModel):
    userId: str
    entity: str
    description: str
    updated: datetime


# FUNCTIONS
async def get_user_entities(user_id: str, entity: str, session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-entities')
    response = table.get_item(Key={'userId': user_id, 'entity': entity})
    item = response.get('Item', None)
    
    if item:
        entity_description = item.get('description', None)
        entity_updated = item.get('updated', None)
        if entity_description:
            return {"entity": entity, "description": entity_description, "updated": entity_updated}
        else:
            return {"error": "Description not found in the item"}
    else:
        return {"error": "Item not found"}


async def get_all_user_entities(user_id: str, session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-entities')
    response = table.query(
        KeyConditionExpression=Key('userId').eq(user_id)
    )
    items = response.get('Items', [])

    return items


async def delete_entity(user_id: str, entity: str, session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-entities')
    response = table.delete_item(
        Key={
            'userId': user_id,
            'entity': entity
        }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error deleting item from the table")


async def add_entity(item: EntityItem, session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-entities')
    timestamp = datetime.utcnow().isoformat()
    
    response = table.update_item(
        Key={
            'userId': item.userId,
            'entity': item.entity
        },
        UpdateExpression="SET description = :desc, #ts = :ts",
        ExpressionAttributeValues={
            ':desc': item.description,
            ':ts': timestamp
        },
            ExpressionAttributeNames={
                "#ts": "updated"
        },
        ReturnValues="UPDATED_NEW"
    )
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {"message": "Item added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error adding item to the table")