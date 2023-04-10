from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dependencies import database
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.llms import PromptLayerOpenAI
from langchain.agents import Tool
from langchain.memory import ConversationEntityMemory
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
import promptlayer
from config import settings
import logging
import boto3
import json
import pytz
from datetime import date, datetime, timedelta, timezone
from botocore.exceptions import ClientError
from functions.entityFunctions import get_all_user_entities

promptlayer.api_key = settings.PRMPTLYR_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

template = """
Assistant is a large language model called ""🐼 panda.ai"" and is trained on top of OpenAI's chatGPT. "🐼 panda.ai" was founded by Sean Betts and born in April 2023.

"🐼 panda.ai" is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, "🐼 panda.ai" is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

"🐼 panda.ai" is constantly learning and improving, and its capabilities are constantly evolving. One thing "🐼 panda.ai" can do is to learn and remember specific topics a user is interested in called entities, which "🐼 panda.ai" stores in it's memory. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions in the style of a knowledgable expert. Additionally, "🐼 panda.ai" is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, "🐼 panda.ai" is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, "🐼 panda.ai" is here to assist. However, if "🐼 panda.ai" isn't totally sure of an answer, it will say "I'm not totally sure, but I think" and then give the answer. If the user asks what data you have on them, please tell them to check their account settings where they will find a data section that lists all the data that we store for them.

The user "🐼 panda.ai" is speaking to is a human and their first name is {first_name}, their surname is {last_name} and their username is {username}.

Today's date is {date}. If you're asked what the time is say that you don't know. Do not ever refer to the user as "the human".

Entities:
{old_entities}
{entities}

Current conversation:
{current_history}
{history}

{username}: {input}
🐼 panda.ai:"""


# FUNCTIONS
async def conversationAgent(userid: str, first_name: str, last_name: str, username: str, message: str):
    llm=PromptLayerOpenAI(openai_api_key = settings.OPENAI_API_KEY, temperature=0.1, pl_tags=[f"{ userid }"])

    today = datetime.today()
    suffix = 'th' if 11 <= today.day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(today.day % 10, 'th')
    current_date = today.strftime(f"%d{suffix} %B %Y")

    now = datetime.now()

    old_entities = await get_all_user_entities(userid)
    old_entities_text = '\n'.join([f"{item['entity']}: {item['description']}" for item in old_entities])

    chat_history = await get_user_chat_history(userid)

    new_template = template.format(
        first_name=first_name,
        last_name=last_name,
        username=username,
        date=current_date,
        old_entities=old_entities_text,
        entities="{entities}",
        current_history = "\n".join([f"{entry['user']}: {entry['message']}" if 'message' in entry else f"{entry['user']}:" for entry in reversed(chat_history[0]["chat_script"] if chat_history else [])]),

        history="{history}",
        input="{input}"
    )

    prompt = PromptTemplate(
        input_variables=["entities", "history", "input"], 
        template=new_template
    )

    conversation = ConversationChain(
        llm=llm, 
        verbose=False,
        prompt=prompt,
        memory=ConversationEntityMemory(llm=OpenAI(openai_api_key=settings.OPENAI_API_KEY))
    )
    entityMemory = conversation.memory.store
    response = conversation.predict(input=f"{ message }")

    if response:
        await save_entities(userid, entityMemory)

        return JSONResponse(content={"response": response})
    else:
        raise HTTPException(status_code=400, detail="An error occurred while processing the request.")

async def save_entities(userid: str, entity_memory: dict):
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )
    table = dynamodb.Table('panda-ai-entities')
    timestamp = datetime.utcnow().isoformat()

    try:
        for entity, description in entity_memory.items():

            response = table.get_item(
                Key={
                    'userId': userid,
                    'entity': entity
                }
            )

            existing_description = response.get('Item', {}).get('description', '')
            new_description = f"{existing_description} {description}"

            response = table.update_item(
                Key={
                    'userId': userid,
                    'entity': entity
                },
                UpdateExpression="SET description = :newDescription, updated = :updated, created_at = if_not_exists(created_at, :created_at)",
                ExpressionAttributeValues={
                    ':newDescription': new_description,
                    ':updated': timestamp,
                    ':created_at': timestamp
                },
                ReturnValues="UPDATED_NEW"
            )

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                logging.info(f"Updated item: {response}")  # This line should be printed if the update is successful
            else:
                logging.info(f"Failed to update item. Response: {response}")

    except ClientError as e:
        logging.info(e.response['Error']['Message'])

    return logging.info("Entities saved to DynamoDB successfully")

async def get_user_chat_history(user_id: str):
    query = "SELECT user_id, created_at, updated_at, chat_script FROM panda_ai_user_chat_history WHERE user_id = :user_id ORDER BY created_at DESC LIMIT 1"
    values = {"user_id": user_id}
    results = await database.fetch_all(query=query, values=values)

    if results:
        chat_history = []
        for result in results:
            user_id = result["user_id"]
            created_at = result["created_at"]
            updated_at = result["updated_at"]
            chat_script = json.loads(result["chat_script"]) # Convert the JSON string back to a list of dictionaries

            chat_history.append({
                "user_id": user_id,
                "created_at": created_at,
                "updated_at": updated_at,
                "chat_script": chat_script,
            })

        # Check if the latest entry was created within the last 2 minutes
        if chat_history[0] and chat_history[0]["updated_at"]:
            now = datetime.now(timezone.utc)
            time_difference = now - chat_history[0]["updated_at"]
            if time_difference <= timedelta(minutes=2):
                return chat_history
            else:
                return None
        else:
            return None
    else:
        return None