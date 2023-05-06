from fastapi import HTTPException
from fastapi.responses import JSONResponse
from dependencies import database
from langchain import ConversationChain, PromptTemplate
from langchain.llms import PromptLayerOpenAI
from langchain.memory import ConversationEntityMemory, ConversationBufferMemory
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.agents.agent import Agent
from langchain.agents.conversational.base import ConversationalAgent
from langchain.chat_models import PromptLayerChatOpenAI
from langchain.tools.base import BaseTool
from langchain.prompts import PromptTemplate
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.agents.loading import AGENT_TO_CLASS, load_agent
from langchain.callbacks.base import BaseCallbackManager
from langchain.base_language import BaseLanguageModel
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from typing import Any, List, Optional, Sequence, Type, Union, Dict
import promptlayer
from config import settings
import logging
import boto3
import json
import tiktoken
from urllib.parse import quote
from datetime import date, datetime, timedelta, timezone
from botocore.exceptions import ClientError
from functions.entityFunctions import get_most_relevant_entities
from functions.toolFunctions import NewsSearchTool, WikipediaSearchTool, YouTubeSearchTool, GoogleMapsSearchTool, GoogleImageSearchTool, GoogleSearchTool, SpotifySearchTool, TMDBSearchTool

promptlayer.api_key = settings.PRMPTLYR_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
            

search = GoogleSearchTool()
news = NewsSearchTool()
wikipedia = WikipediaSearchTool()
youtube = YouTubeSearchTool()
images = GoogleImageSearchTool()
maps = GoogleMapsSearchTool()
music = SpotifySearchTool()
movie = TMDBSearchTool()
wolfram = WolframAlphaAPIWrapper(wolfram_alpha_appid = settings.WOLFRAM_ALPHA_APPID)

tools = [
    Tool(
        name = "Internet Search",
        func=search.run,
        description="Use this when you want to search the internet to answer questions about things you have no knowledge of. The input to this should be a single search term.",
        return_direct=True
    ),
    Tool(
        name = "Maths",
        func=wolfram.run,
        description="Use this when you want need to do maths or make some calculations. Use this more than any other tool if the question is about maths or making calculations. The input to this should be numbers in a maths expression",
        return_direct=True
    ),
    Tool(
        name = "Latest News Search",
        func=news.run,
        description=" Use this when you want to get information about the latest news, top news headlines or current news stories. Use this more than Internet Search if the question is about News. The input should be a question in natural language that this API can answer.",
        return_direct=True
    ),
    Tool(
        name = "Wikipedia Search",
        func=wikipedia.run,
        description="Use this when you want to search wikipedia about things you have no knowledge of. Use this more than Internet Search if the question is about Wikipedia. The input to this should be a single search term.",
        return_direct=True
    ),
    Tool(
        name = "Video Search",
        func=youtube.run,
        description="Use this when you want to search for YouTube videos or movie trailers. Use this more than Internet Search if the question is about videos or trailers. The input to this should be a single search term.",
        return_direct=True
    ),
    Tool(
        name = "Image Search",
        func=images.run,
        description="Use this when you want to search for images. Use this more than any other tool if the question is about images. The input to this should be a single search term.",
        return_direct=True
    ),
    Tool(
        name = "Music Search",
        func= music.run,
        description="Use this when you want to search for music. Use this more than any other tool if the question is about music. The input to this should be a single search term.",
        return_direct=True
    ),
    Tool(
        name = "Movie & TV Search",
        func= movie.run,
        description="Use this when you want to search for a movie, tv show or actor. Use this more than any other tool if the question is about movies, tv shows or actors. The input to this should be a single search term.",
        return_direct=True
    ),
    Tool(
        name = "Map & Location Search",
        func=maps.run,
        description="Use this when you want to search for a map or get a location. Use this more than any other tool if the question is about locations or maps. The input to this should be a single search term.",
        return_direct=True
    )
]


# FUNCTIONS
async def pandaChatAgent(userid: str, first_name: str, last_name: str, username: str, message: str):
    # await save_entities(userid, message)

    llm=PromptLayerChatOpenAI(openai_api_key = settings.OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.05, pl_tags=[f"{ userid }"], return_pl_id=True)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    today = datetime.today()
    suffix = 'th' if 11 <= today.day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(today.day % 10, 'th')
    current_date = today.strftime(f"%d{suffix} %B %Y")

    entities = await get_most_relevant_entities(userid, message)
    formatted_entities = '\n'.join([f"{item['entity']}: {item['description']}" for item in entities])

    chat_history = await get_user_chat_history(userid)

    if chat_history is not None and chat_history[0].get("chat_id") is not None:
        chatid = chat_history[0]["chat_id"]
    else:
        chatid = 0

    prefix_dict = promptlayer.prompts.get("main_panda_chat_prefix")
    suffix_dict = promptlayer.prompts.get("main_panda_chat_suffix")
    format_dict = promptlayer.prompts.get("main_panda_chat_format_instructions")

    PREFIX = prefix_dict['template']
    SUFFIX = suffix_dict['template']
    FORMAT_INSTRUCTIONS =format_dict['template']

    MY_PREFIX = PREFIX.format(
        ai_prefix="🐼 panda.ai",
        first_name=first_name,
        last_name=last_name,
        username=username,
        current_date=current_date,
    )
    MY_SUFFIX = SUFFIX.format(
        entities = formatted_entities,
        current_history = "\n".join([f"{entry['user']}: {entry['message']}" if 'message' in entry else f"{entry['user']}:" for entry in reversed(chat_history[0]["chat_script"] if chat_history else [])]),
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
        # return_intermediate_steps=True,
        agent=pandaAgent,
        agent_kwargs={"prefix": MY_PREFIX, "suffix": MY_SUFFIX, "format_instructions": MY_FORMAT_INSTRUCTIONS, "ai_prefix": "🐼 panda.ai", "human_prefix": f"{username}"}, verbose=True, memory=memory
    )

    prompt_template = pandaAgent.create_prompt(
        tools,
        MY_PREFIX,
        MY_SUFFIX,
        MY_FORMAT_INSTRUCTIONS,
    )

    logging.info("Prompt Template: " + str(prompt_template.template))
    tokens = num_tokens_from_string(prompt_template.template, "cl100k_base")

    try:
        response = agent_chain.run(input=f"{ message }")
        await save_new_message(userid, chatid, message, response, tokens, True)
        return JSONResponse(content={"response": response})

    except Exception as e:
        logging.error(f"Error while running agent_chain: {e}")
        await save_new_message(userid, chatid, message, "Apologies! Something has gone wrong, please try again later", tokens, False)
        return JSONResponse(content={"response": "Apologies! Something has gone wrong, please try again later 🐼"})


async def save_entities(userid: str, message: str):
    entity_llm=PromptLayerChatOpenAI(openai_api_key = settings.OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0, pl_tags=[f"{ userid }", "entityCreation"])
    
    memory = ConversationEntityMemory(llm=entity_llm)
    
    conversation = ConversationChain(
        llm=entity_llm, 
        verbose=True,
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

                summary_llm=PromptLayerChatOpenAI(openai_api_key = settings.OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0, pl_tags=[f"{ userid }", "summarisation"])
                summarised_description = summary_llm(f"Summarise this for me and DO NOT leave out any details: {combined_description}")

                new_description = summarised_description.replace("\n", "")

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
    query = "SELECT chat_id, user_id, created_at, updated_at, chat_script FROM panda_ai_user_chat_history WHERE user_id = :user_id ORDER BY created_at DESC LIMIT 1"
    values = {"user_id": user_id}
    results = await database.fetch_all(query=query, values=values)

    if results:
        chat_history = []
        for result in results:
            chat_id = result["chat_id"]
            user_id = result["user_id"]
            created_at = result["created_at"]
            updated_at = result["updated_at"]
            chat_script = json.loads(result["chat_script"]) # Convert the JSON string back to a list of dictionaries

            # Check if chat_script contains </div>
            if "</div>" not in str(chat_script):
                chat_history.append({
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "chat_script": chat_script,
                })

        # Check if the latest entry was created within the last 5 minutes
        if chat_history and chat_history[0]["updated_at"]:
            now = datetime.now(timezone.utc)
            time_difference = now - chat_history[0]["updated_at"]
            if time_difference <= timedelta(minutes=5):
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


async def save_new_message(user_id: str, chat_id: int, message: str, message_response: str, tokens: int, success: bool):

    cost = round((tokens/1000) * 0.002, 6)  # Calculate the cost for GPT 3.5 TURBO

    values = {
        "user_id": user_id,
        "chat_id": chat_id,
        "message": message,
        "message_response": message_response,
        "tokens": tokens,
        "cost": cost,
        "success": success
    }

    query = """
        INSERT INTO panda_ai_messages (user_id, chat_id, message, message_response, tokens, cost, success)
        VALUES (:user_id, :chat_id, :message, :message_response, :tokens, :cost, :success)
    """

    await database.execute(query=query, values=values)
    return {"message": "User data inserted successfully"}


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens