from fastapi import APIRouter, Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.asyncio import delete_user
from config import settings
from cryptography.fernet import Fernet
import logging
from pydantic import BaseModel
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key

from functions.entityFunctions import get_user_entities, get_all_user_entities, delete_entity, add_entity


# CONFIG
router = APIRouter(
    prefix="/entities",
    tags=["entities"],
)

class EntityItem(BaseModel):
    userId: str
    entity: str
    description: str
    updated: datetime


# ROUTERS
@router.get("/get")
async def fetch_user_entities(user_id: str, entity: str, session: SessionContainer = Depends(verify_session())):
    result = await get_user_entities(user_id, entity, session)
    return result

@router.get("/get-all")
async def fetch_all_user_entities(user_id: str, session: SessionContainer = Depends(verify_session())):
    result = await get_all_user_entities(user_id, session)
    return result

@router.get("/delete")
async def delete_user_entity(user_id: str, entity: str, session: SessionContainer = Depends(verify_session())):
    result = await delete_entity(user_id, entity, session)
    return result


@router.post("/save")
async def add_user_entity(item: EntityItem, session: SessionContainer = Depends(verify_session())):
    result = await add_entity(item, session)
    return result