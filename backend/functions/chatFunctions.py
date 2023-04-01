from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.llms import PromptLayerOpenAI
from langchain.agents import Tool
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
import promptlayer
from config import settings
import os

promptlayer.api_key = settings.PRMPTLYR_API_KEY


template = """Assistant is a large language model called panda and trained on top of OpenAI's chatGPT.

panda is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, panda is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

panda is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions in the style of a knowledgable expert. Additionally, panda is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, panda is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, panda is here to assist.

{history}
user: {input}
panda:"""

prompt = PromptTemplate(
    input_variables=["history", "input"], 
    template=template
)

# FUNCTIONS
async def conversationAgent(userid: str, message: str):
    chatgpt_chain = LLMChain(
        llm=PromptLayerOpenAI(openai_api_key = settings.OPENAI_API_KEY, temperature=0, pl_tags=[f"{ userid }"]),
        prompt=prompt, 
        verbose=True, 
        memory=ConversationBufferWindowMemory(k=2),
    )

    response = chatgpt_chain.predict(input=f"{ message }")

    if response:
        return JSONResponse(content={"response": response})
    else:
        raise HTTPException(status_code=400, detail="An error occurred while processing the request.")