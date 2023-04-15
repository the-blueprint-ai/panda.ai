from fastapi import HTTPException
from fastapi.responses import JSONResponse
from dependencies import database
from langchain import ConversationChain, PromptTemplate
from langchain.llms import PromptLayerOpenAI
from langchain.memory import ConversationEntityMemory, ConversationBufferMemory
from langchain.agents import Tool
from langchain.utilities import SerpAPIWrapper
from langchain.agents import AgentType
from langchain.agents.agent import Agent
from langchain.agents.conversational.base import ConversationalAgent
from langchain.llms import PromptLayerOpenAI
from langchain.tools.base import BaseTool
from langchain.prompts import PromptTemplate
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.agents.loading import AGENT_TO_CLASS, load_agent
from langchain.callbacks.base import BaseCallbackManager
from langchain.schema import BaseLanguageModel
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from typing import Any, List, Optional, Sequence, Type, Union
import promptlayer
from config import settings
import logging
import boto3
import json
from datetime import date, datetime, timedelta, timezone
from botocore.exceptions import ClientError
from functions.entityFunctions import get_most_relevant_entities

promptlayer.api_key = settings.PRMPTLYR_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


PREFIX = """
Assistant is a large language model called ""🐼 panda.ai"" and is trained on top of OpenAI's chatGPT. "🐼 panda.ai" was founded by Sean Betts in April 2023.

"🐼 panda.ai" is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, "🐼 panda.ai" is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

"🐼 panda.ai" is constantly learning and improving, and its capabilities are constantly evolving. One thing "🐼 panda.ai" can do is to learn and remember specific topics a user is interested in called entities, which "🐼 panda.ai" stores in it's memory. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions in the style of a knowledgable expert. Additionally, "🐼 panda.ai" is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, "🐼 panda.ai" is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, "🐼 panda.ai" is here to assist. However, if "🐼 panda.ai" isn't totally sure of an answer, it will say "I'm not totally sure, but I think" and then give the answer. If the user asks what data you have on them, please tell them to check their account settings where they will find a data section that lists all the data that we store for them.

The user "🐼 panda.ai" is speaking to is a human and their first name is {first_name}, their surname is {last_name} and their username is {username}.

Today's date is {date}. If you're asked what the time is say that you don't know. Do not ever refer to the user as "the human".

TOOLS:
------
🐼 panda.ai has access to the following tools:"""

FORMAT_INSTRUCTIONS = """To use a tool, please use the following format:
```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```
When you have a response to say to {human_prefix}, or if you do not need to use a tool, you MUST use the format:
```
{ai_prefix} thought: Do I need to use a tool? No
{ai_prefix}: [your response here]
```"""

SUFFIX = """Begin!
Entity memories:
{entities}
Previous conversation history:
{chat_history}
New input: {input}
{agent_scratchpad}"""


# TOOLS
search = SerpAPIWrapper(serpapi_api_key=settings.SERPAPI_API_KEY)

tools = [
    Tool(
        name = "Internet Search",
        func=search.run,
        description="useful for when you need to search the internet to answer questions about current events or the current state of the world. The input to this should be a single search term."
    ),
]


# FUNCTIONS
async def pandaChatAgent(userid: str, first_name: str, last_name: str, username: str, message: str):
    await save_entities(userid, message)

    llm=PromptLayerOpenAI(openai_api_key = settings.OPENAI_API_KEY, temperature=0.05, pl_tags=[f"{ userid }"])
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    today = datetime.today()
    suffix = 'th' if 11 <= today.day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(today.day % 10, 'th')
    current_date = today.strftime(f"%d{suffix} %B %Y")

    entities = await get_most_relevant_entities(userid, message)
    formatted_entities = '\n'.join([f"{item['entity']}: {item['description']}" for item in entities])

    MY_PREFIX = PREFIX.format(
        first_name=first_name,
        last_name=last_name,
        username=username,
        date=current_date,
    )
    MY_SUFFIX = SUFFIX.format(
        entities = formatted_entities,
        chat_history = "{chat_history}",
        input = "{input}",
        agent_scratchpad = "{agent_scratchpad}",
    )

    MY_FORMAT_INSTRUCTIONS = FORMAT_INSTRUCTIONS

    class pandaAgent(ConversationalAgent):
        @classmethod
        def create_prompt(
            cls,
            tools: Sequence[BaseTool],
            prefix: str = MY_PREFIX,
            suffix: str = MY_SUFFIX,
            format_instructions: str = MY_FORMAT_INSTRUCTIONS,
            ai_prefix: str = "🐼 panda.ai",
            human_prefix: str = f"{username}",
            input_variables: Optional[List[str]] = None,
        ) -> PromptTemplate:
            return super().create_prompt(
                tools,
                prefix=prefix,
                suffix=suffix,
                format_instructions=format_instructions,
                ai_prefix=ai_prefix,
                human_prefix=human_prefix,
                input_variables=input_variables,
            )

    agent_chain = initialize_agent(
        tools,
        llm,
        agent=pandaAgent,
        agent_kwargs={"prefix": MY_PREFIX, "suffix": MY_SUFFIX, "format_instructions": MY_FORMAT_INSTRUCTIONS, "ai_prefix": "🐼 panda.ai", "human_prefix": f"{username}"}, verbose=True, memory=memory
    )
    response = agent_chain.run(input=f"{ message }")

    if response:
        return JSONResponse(content={"response": response})
    else:
        raise HTTPException(status_code=400, detail="An error occurred while processing the request.")


async def save_entities(userid: str, message: str):
    entity_llm=PromptLayerOpenAI(openai_api_key = settings.OPENAI_API_KEY, temperature=0, pl_tags=[f"{ userid }", "entityCreation"])
    
    memory = ConversationEntityMemory(llm=entity_llm)
    
    conversation = ConversationChain(
        llm=entity_llm, 
        verbose=False,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=memory
    )

    response = conversation.predict(input=message)

    if response:
        entity_memory = conversation.memory.entity_store.store

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
                combined_description = f"{existing_description} {description}"

                summary_llm=PromptLayerOpenAI(openai_api_key = settings.OPENAI_API_KEY, temperature=0, pl_tags=[f"{ userid }", "summarisation"])
                summarised_description = summary_llm(f"Summarise this for me and DO NOT leave out any details: {combined_description}")

                new_description = summarised_description.replace("\n", "")
                logging.info(f"New Description: {new_description}") 

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
                    return None
                else:
                    logging.info(f"Failed to update entities. Response: {response}")


        except ClientError as e:
            logging.info(e.response['Error']['Message'])

        return logging.info("Entities saved to DynamoDB successfully")

    else:
        raise HTTPException(status_code=400, detail="An error occurred while saving the entities.")


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
    

def initialize_agent(
    tools: Sequence[BaseTool],
    llm: BaseLanguageModel,
    agent: Optional[Union[AgentType, Type[Agent]]] = None,
    callback_manager: Optional[BaseCallbackManager] = None,
    agent_path: Optional[str] = None,
    agent_kwargs: Optional[dict] = None,
    **kwargs: Any,
) -> AgentExecutor:
    """Load an agent executor given tools and LLM.
    Args:
        tools: List of tools this agent has access to.
        llm: Language model to use as the agent.
        agent: Agent type to use. If None and agent_path is also None, will default to
            AgentType.ZERO_SHOT_REACT_DESCRIPTION.
        callback_manager: CallbackManager to use. Global callback manager is used if
            not provided. Defaults to None.
        agent_path: Path to serialized agent to use.
        agent_kwargs: Additional key word arguments to pass to the underlying agent
        **kwargs: Additional key word arguments passed to the agent executor
    Returns:
        An agent executor
    """
    if agent is None and agent_path is None:
        agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION
    if agent is not None and agent_path is not None:
        raise ValueError(
            "Both `agent` and `agent_path` are specified, "
            "but at most only one should be."
        )
    if agent is not None:
        if isinstance(agent, AgentType):
            if agent not in AGENT_TO_CLASS:
                raise ValueError(
                    f"Got unknown agent type: {agent}. "
                    f"Valid types are: {AGENT_TO_CLASS.keys()}."
                )
            agent_cls = AGENT_TO_CLASS[agent]
        elif issubclass(agent, Agent):
            agent_cls = agent
        else:
            raise ValueError(f"Unknown agent type: {agent}")
        agent_kwargs = agent_kwargs or {}
        agent_obj = agent_cls.from_llm_and_tools(
            llm, tools, callback_manager=callback_manager, **agent_kwargs
        )
    elif agent_path is not None:
        agent_obj = load_agent(
            agent_path, llm=llm, tools=tools, callback_manager=callback_manager
        )
    else:
        raise ValueError(
            "Somehow both `agent` and `agent_path` are None, "
            "this should never happen."
        )
    return AgentExecutor.from_agent_and_tools(
        agent=agent_obj,
        tools=tools,
        callback_manager=callback_manager,
        **kwargs,
    )