from fastapi import Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from sentence_transformers import SentenceTransformer
import pinecone
from config import settings
from cryptography.fernet import Fernet
from typing import Optional, List
import logging
from pydantic import BaseModel
from datetime import datetime
import boto3
import spacy
from heapq import nlargest
import numpy as np
from boto3.dynamodb.conditions import Key, Attr

nlp = spacy.load("en_core_web_md")

# DATABASES
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)
model = SentenceTransformer('all-MiniLM-L6-v2')
pinecone.init(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT_NAME)
index = pinecone.Index(index_name="panda-ai-user-entities")

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

async def get_all_user_entities(user_id: str):
    table = dynamodb.Table('panda-ai-entities')
    response = table.query(
        KeyConditionExpression=Key('userId').eq(user_id)
    )
    items = response.get('Items', [])

    return items


async def get_most_relevant_entities(user_id: str, message: str, top_n: int = 3):
    try:
        message_vector = model.encode([message])[0]

        # Query Pinecone for most similar entities
        query_results = index.query(queries=[message_vector], top_k=top_n, filter={"user_id": user_id}, namespace='panda-ai-entities')

        # Extract the unique ids of the most similar entities
        unique_ids = query_results.results[0].ids

        # Query DynamoDB to get descriptions for these entities
        table = dynamodb.Table('panda-ai-entities')
        most_relevant_entities = []
        for uid in unique_ids:
            response = table.get_item(Key={'userId': uid.split('/')[0], 'entity': uid.split('/')[1]})
            description = response['Item']['description']
            score = query_results.results[0].scores[unique_ids.index(uid)]
            most_relevant_entities.append({
                'entity': uid.split('/')[1],  # Extract entity from unique id
                'description': description,
                'weight': float(score)
            })

        return most_relevant_entities

    except Exception as e:
        print("Error occurred:", e)
        return []

async def get_all_entities(session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-entities')
    response = table.scan()
    items = response.get('Items', [])

    return items

async def delete_entity(user_id: str, entity: Optional[str] = None, session: SessionContainer = Depends(verify_session())):
    table = dynamodb.Table('panda-ai-entities')
    pinecone_ids_to_delete = []  # List of ids to delete in Pinecone
    
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
                pinecone_ids_to_delete.append(item['userId'] + "/" + item['entity'])  # Add to list of Pinecone ids to delete
        
    else:
        # Delete the specific entity for the user
        response = table.delete_item(
            Key={
                'userId': user_id,
                'entity': entity
            }
        )
        pinecone_ids_to_delete.append(user_id + "/" + entity)  # Add to list of Pinecone ids to delete

    # Delete in Pinecone
    delete_response = index.delete(ids=pinecone_ids_to_delete, namespace='panda-ai-entities')
    pinecone_success = delete_response == {}  # Checks if the response is an empty dict

    if response['ResponseMetadata']['HTTPStatusCode'] == 200 and pinecone_success:
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error deleting entity from the databases")


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

    # Compute embedding for the description and add it to Pinecone
    embedding = model.encode([item.description])[0]
    unique_id = item.userId + "/" + item.entity
    metadata = {
        "user_id": item.userId
    }
    pinecone_response = index.upsert(vectors=[(unique_id, embedding, metadata)])
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200 and pinecone_response.upserted_count == 1:
        return {"message": "Entity added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error adding entity to the databases")
    
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
    
    # Compute new embedding for the description and update it in Pinecone
    embedding = model.encode([entity_update.description])[0]
    unique_id = entity_update.userId + "/" + entity_update.entity
    metadata = {
        "user_id": entity_update.userId
    }
    pinecone_response = index.upsert(vectors=[(unique_id, embedding, metadata)])

    # Check if both updates were successful
    if response['ResponseMetadata']['HTTPStatusCode'] == 200 and pinecone_response.upserted_count == 1:
        return {"message": "Entity description updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error updating entity in the databases.")

# Compute cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))