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
from boto3.dynamodb.conditions import Key, Attr


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
    created_at: datetime
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


async def get_all_entities(session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-entities')
    response = table.scan()
    items = response.get('Items', [])

    return items


async def delete_entity(user_id: str, entity: Optional[str] = None, session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-entities')
    
    if entity is None:
        # Delete all entities for the user
        response = table.scan(
            FilterExpression=Attr('userId').eq(user_id)
        )
        
        with table.batch_writer() as batch:
            for item in response['Items']:
                batch.delete_item(
                    Key={
                        'userId': item['userId'],
                        'entity': item['entity']
                    }
                )
        
    else:
        # Delete the specific entity for the user
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
        UpdateExpression="SET description = :desc, created_at = :created_at, updated = :updated ",
        ExpressionAttributeValues={
            ':desc': item.description,
            ':created_at': timestamp,
            ':updated': timestamp
        },
        ReturnValues="UPDATED_NEW"
    )
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return {"message": "Item added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error adding item to the table")
    
async def update_entity(entity_update: EntityItem, session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-entities')
    timestamp = datetime.utcnow().isoformat()

    # Update the entity description in the database
    response = table.update_item(
        Key={
            'userId': entity_update.userId,
            'entity': entity_update.entity
        },
        UpdateExpression="SET description = :desc, updated = :updated",
        ExpressionAttributeValues={
            ':desc': entity_update.description,
            ':updated': timestamp
        },
        ReturnValues="UPDATED_NEW"
    )
    
    # Check if the update was successful
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise HTTPException(status_code=500, detail="Error updating Entity data.")
    
    # Return a success message
    return {"message": "Description updated successfully"}