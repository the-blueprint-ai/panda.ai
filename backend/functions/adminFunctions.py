from fastapi import HTTPException
from pydantic import BaseModel
from config import settings
from dependencies import database
import logging
import boto3
import json
import pytz
from datetime import datetime, time, timedelta, timezone
from typing import List
from collections import defaultdict


# DATABASES
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Roadmap(BaseModel):
    roadmap_id: int
    created_at: datetime
    name: str
    description: str
    tags: List[str]
    votes: int
    reviewed: bool
    email: str


# FUNCTIONS
async def get_roadmap():
    query = "SELECT roadmap_id, created_at, name, description, tags, votes, reviewed, email FROM panda_ai_roadmap ORDER BY roadmap_id;"
    results = await database.fetch_all(query=query)

    if results:
        return results
    else:
        return None

async def update_roadmap(roadmap_id: int, roadmap: Roadmap):
    query = """
        UPDATE panda_ai_roadmap
        SET name = :name, description = :description, tags = :tags, votes = :votes, reviewed = :reviewed, email = :email
        WHERE roadmap_id = :roadmap_id
    """
    values = {
        "roadmap_id": roadmap_id,
        "name": roadmap.name,
        "description": roadmap.description,
        "tags": json.dumps(roadmap.tags), # convert tags list to JSON string
        "votes": roadmap.votes,
        "reviewed": roadmap.reviewed,
        "email": roadmap.email,
    }
    try:
        await database.execute(query=query, values=values)
        return {"message": "Roadmap updated successfully"}
    except Exception as e:
        logger.error(f"Error in update_roadmap: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def add_roadmap_item(name: str, description: str):

    # Insert new idea into the database
    query = """
        INSERT INTO panda_ai_roadmap (name, description, tags, votes, reviewed, email)
        VALUES (:name, :description, '["newly added"]'::jsonb, 0, false, 'admin@mypanda.ai');"""
    await database.execute(query=query, values={"name": name, "description": description})

    # Get the ID of the newly inserted item
    query = """
        SELECT roadmap_id FROM panda_ai_roadmap
        WHERE description = :description
        ORDER BY roadmap_id DESC
        LIMIT 1;"""
    result = await database.fetch_one(query=query, values={"description": description})

    return {"message": "Roadmap item successfully added to database", "roadmap_id": result["roadmap_id"]}

async def topline_user_stats():
    query = "SELECT COUNT(*) AS total_users, COUNT(*) FILTER (WHERE created_at::date = CURRENT_DATE) AS users_today, SUM(CASE WHEN created_at >= NOW() - INTERVAL '1 week' THEN 1 ELSE 0 END) AS users_last_week, SUM(CASE WHEN created_at >= NOW() - INTERVAL '1 month' THEN 1 ELSE 0 END) AS users_last_month FROM panda_ai_users;"
    results = await database.fetch_all(query=query)

    if results:
        return results
    else:
        return None
    
async def users_by_day_stats():
    query = "SELECT DATE_TRUNC('day', created_at) AS date, COUNT(*) AS volume FROM panda_ai_users GROUP BY DATE_TRUNC('day', created_at) ORDER BY date;"
    results = await database.fetch_all(query=query)

    if results:
        return results
    else:
        return None
    
async def topline_onboarding_stats():
    query = "SELECT COUNT(*) AS total_users, COUNT(*) FILTER (WHERE onboarded_at::date = CURRENT_DATE) AS users_today, SUM(CASE WHEN onboarded_at >= NOW() - INTERVAL '1 week' THEN 1 ELSE 0 END) AS users_last_week, SUM(CASE WHEN onboarded_at >= NOW() - INTERVAL '1 month' THEN 1 ELSE 0 END) AS users_last_month FROM panda_ai_users WHERE onboarded = true;"
    results = await database.fetch_all(query=query)

    if results:
        return results
    else:
        return None
    
async def onboarding_by_day_stats():
    query = "SELECT DATE_TRUNC('day', onboarded_at) AS date, COUNT(*) AS volume FROM panda_ai_users WHERE onboarded = true GROUP BY DATE_TRUNC('day', onboarded_at) ORDER BY date;"
    results = await database.fetch_all(query=query)

    if results:
        return results
    else:
        return None
    
async def topline_chat_stats():
    query = "SELECT COUNT(*) AS total_chats, COUNT(*) FILTER (WHERE created_at::date = CURRENT_DATE) AS chats_today, SUM(CASE WHEN created_at >= NOW() - INTERVAL '1 week' THEN 1 ELSE 0 END) AS chats_last_week, SUM(CASE WHEN created_at >= NOW() - INTERVAL '1 month' THEN 1 ELSE 0 END) AS chats_last_month FROM panda_ai_user_chat_history;"
    results = await database.fetch_all(query=query)

    if results:
        return results
    else:
        return None
    
async def chat_by_day_stats():
    query = "SELECT DATE_TRUNC('day', created_at) AS date, COUNT(*) AS volume FROM panda_ai_user_chat_history GROUP BY DATE_TRUNC('day', created_at) ORDER BY date;"
    results = await database.fetch_all(query=query)

    if results:
        return results
    else:
        return None

async def topline_entity_stats():
    table = dynamodb.Table('panda-ai-entities')

    # Scan the table
    response = table.scan()
    items = response.get('Items', [])

    # Calculate statistics
    total_entities = 0
    entities_today = 0
    entities_last_week = 0
    entities_last_month = 0

    now = datetime.now(timezone.utc)
    today = now.date()
    last_week = now - timedelta(weeks=1)
    last_month = now - timedelta(days=30)

    for item in items:
        created_at = datetime.fromisoformat(item['created_at']).replace(tzinfo=pytz.UTC)
        total_entities += 1

        if created_at.date() == today:
            entities_today += 1

        if created_at >= last_week:
            entities_last_week += 1

        if created_at >= last_month:
            entities_last_month += 1

    topline_entity_stats = {
        'total_entities': total_entities,
        'entities_created_today': entities_today,
        'entities_created_last_week': entities_last_week,
        'entities_created_last_30_days': entities_last_month
    }

    return topline_entity_stats

async def entity_by_day_stats():
    table = dynamodb.Table('panda-ai-entities')

    # Scan the table
    response = table.scan()
    items = response.get('Items', [])

    # Group items by date and count chats
    daily_entities = defaultdict(int)

    for item in items:
        created_at = datetime.fromisoformat(item['created_at']).replace(tzinfo=pytz.UTC)
        date_only = created_at.date()
        daily_entities[date_only] += 1

    # Convert the defaultdict to a sorted list of dictionaries with date and volume keys
    entity_by_day_stats = sorted(
        [
            {
                "date": datetime.combine(k, time(0, 0, 0, tzinfo=timezone.utc)).isoformat(),
                "volume": v
            }
            for k, v in daily_entities.items()
        ],
        key=lambda x: x["date"],
    )

    return entity_by_day_stats