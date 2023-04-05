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
from botocore.exceptions import ClientError


from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from langchain.memory.chat_memory import BaseChatMemory
from langchain.memory.prompt import (
    ENTITY_EXTRACTION_PROMPT,
    ENTITY_SUMMARIZATION_PROMPT,
)
from langchain.memory.utils import get_prompt_input_key
from langchain.prompts.base import BasePromptTemplate
from langchain.schema import BaseLanguageModel, BaseMessage, get_buffer_string




promptlayer.api_key = settings.PRMPTLYR_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

template = """
Assistant is a large language model called panda and trained on top of OpenAI's chatGPT.

panda is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, panda is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

panda is constantly learning and improving, and its capabilities are constantly evolving. One thing panda can do is to learn and remember specific topics a user is interested in called entities, which is stores in it's memory. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions in the style of a knowledgable expert. Additionally, panda is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, panda is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, panda is here to assist.

The user panda is speaking to is a human and their first name is {first_name}, their surname is {last_name} and their username is {username}.

Entities:
{entities}

Conversation history:
{history}

{username}: {input}
panda:"""


# FUNCTIONS
