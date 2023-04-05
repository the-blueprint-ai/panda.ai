from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
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
from botocore.exceptions import ClientError
from functions.entityFunctions import get_all_user_entities

promptlayer.api_key = settings.PRMPTLYR_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

template = """
Assistant is a large language model called panda and trained on top of OpenAI's chatGPT.

panda is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, panda is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

panda is constantly learning and improving, and its capabilities are constantly evolving. One thing panda can do is to learn and remember specific topics a user is interested in called entities, which is stores in it's memory. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions in the style of a knowledgable expert. Additionally, panda is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, panda is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, panda is here to assist. If the user asks what data you have on them, please tell them to check their account settings where they will find a data section that lists all the data that we store for them.

The user panda is speaking to is a human and their first name is {first_name}, their surname is {last_name} and their username is {username}.

Entities:
{old_entities}

{entities}

Conversation history:
{history}

{username}: {input}
panda:"""


# FUNCTIONS
async def conversationAgent(userid: str, first_name: str, last_name: str, username: str, message: str):
    llm=PromptLayerOpenAI(openai_api_key = settings.OPENAI_API_KEY, temperature=0.1, pl_tags=[f"{ userid }"])

    old_entities = await get_all_user_entities(userid)
    old_entities_text = '\n'.join([f"{item['entity']}: {item['description']}" for item in old_entities])

    new_template = template.format(
        first_name=first_name,
        last_name=last_name,
        username=username,
        old_entities=old_entities_text,
        entities="{entities}",
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

    try:
        for entity, description in entity_memory.items():
            logging.info(f"Updating item with UserId={userid}, Entity={entity}, Description={description}")  # Debugging line

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
                UpdateExpression="SET description = :newDescription",
                ExpressionAttributeValues={
                    ':newDescription': new_description
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