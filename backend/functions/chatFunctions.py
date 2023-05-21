from fastapi import HTTPException
from fastapi.responses import JSONResponse
from dependencies import database
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationEntityMemory, ConversationBufferMemory
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.agents.agent import Agent
from langchain.schema import HumanMessage
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
from sentence_transformers import SentenceTransformer
import pinecone
from cryptography.fernet import Fernet, InvalidToken
from typing import Any, List, Optional, Sequence, Type, Union, Dict
from config import settings
import logging, re, asyncio, json, tiktoken, requests, boto3, promptlayer
from starlette import status
from urllib.parse import quote
from datetime import date, datetime, timedelta, timezone
from botocore.exceptions import ClientError
from functions.entityFunctions import get_most_relevant_entities
from functions.toolFunctions import NewsSearchTool, WikipediaSearchTool, YouTubeSearchTool, GoogleMapsSearchTool, GoogleImageSearchTool, GoogleSearchTool, SpotifySearchTool, TMDBSearchTool
from functions.emailFunctions import email_send

promptlayer.api_key = settings.PRMPTLYR_API_KEY

key = settings.FERNET_KEY
if not key:
    raise ValueError("FERNET_KEY environment variable not set")
cipher_suite = Fernet(key.encode())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')
pinecone.init(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT_NAME)
index = pinecone.Index("panda-ai-user-entities")
            
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
        name = "Maths",
        func=wolfram.run,
        description="Use this when you want need to do maths or make some calculations. Use this more than any other tool if the question is about maths or making calculations. The input to this should be numbers in a maths expression",
        return_direct=True
    ),
    Tool(
        name = "Video Search",
        func=youtube.run,
        description="Use this when you want to search for YouTube videos or movie trailers. Use this more than Internet Search if the question is about videos or trailers. The input to this should be a single search term.",
        return_direct=True
    ),
    Tool(
        name = "Map & Location Search",
        func=maps.run,
        description="Use this when you want to search for a map or get a location. Use this more than any other tool if the question is about locations or maps. The input to this should be a single search term.",
        return_direct=True
    ),
    Tool(
        name = "Image Search",
        func=images.run,
        description="Use this when you want to search for images. Use this more than any other tool if the question is about images. The input to this should be a single search term.",
        return_direct=True
    ),
    Tool(
        name = "Wikipedia Search",
        func=wikipedia.run,
        description="Use this when you want to search wikipedia about things you have no knowledge of. Use this more than Internet Search if the question is about Wikipedia. The input to this should be a single search term.",
        return_direct=True
    ),
    Tool(
        name = "Internet Search",
        func=search.run,
        description="Use this when you want to search the internet to answer questions about things you have no knowledge of. The input to this should be a single search term.",
        return_direct=True
    ),
    Tool(
        name = "Latest News Search",
        func=news.run,
        description="Use this when you want to get information about the latest news, top news headlines or current news stories. Use this more than Internet Search if the question is about News. The input should be a question in natural language that this API can answer.",
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
    )
]


# FUNCTIONS
async def pandaChatAgent(userid: str, first_name: str, last_name: str, username: str, message: str):
    check_data, number_of_messages_this_month = await asyncio.gather(
        get_subscriber_and_user_messages_per_month(userid),
        get_user_messages_this_month(userid)
    )
    subscriber = check_data["subscriber"]
    messages_allowed = check_data["messages_per_month"]
    messages_count = number_of_messages_this_month["count"]

    if (subscriber == False):
        return JSONResponse(content={"response": "<span>Apologies! You need to subscribe to one of our packages to use 🐼 panda.ai. You can find more information about our subscription packages <a href='https://www.mypanda.ai/subscriptions' target='_blank'>here</a>.</span>"})
    elif (messages_count >= messages_allowed):
        return JSONResponse(content={"response": f"<span>Apologies! You have used up your monthly messages allowance. To add more messages to your monthly plan or to upgrade your subscription, please see the infomation below:</span><h5 class='mt-4 mb-0'>ADD ONS</h5><span><p>You can add more messages to your monthly subscription as a one-off or ongoing every month by visiting your <a href='https://www.mypanda.ai/auth/{userid}/account' target='_blank' style='text-decoration: none'>account page</a>, heading to the Subscription tab and updating your subscription details.</p><span><h5 class='mt-4 mb-0'>UPGRADING</h5><span><p>To upgrade your subscription to include more messages per month in your plan you can go to your <a href='https://www.mypanda.ai/auth/{userid}/account' target='_blank' style='text-decoration: none'>account page</a>, head to the Subscriptions tab and upgrade your subscription.</p></span>"})
    else:
        if (messages_allowed & messages_count == 20):
            await end_trial(userid)
            return JSONResponse(content={"response": "<span>Thank you for trying 🐼 panda.ai. Your free trial of 20 messages has now ended. If you would like to continue using 🐼 panda.ai you can sign up to one of our subscription packages <a href='https://www.mypanda.ai/subscriptions' target='_blank'>here</a>.</span>"})

        integration_ids, entities, chat_history = await asyncio.gather(
            get_user_tools(userid),
            get_most_relevant_entities(userid, message),
            get_user_chat_history(userid)
        )

        if chat_history is not None and chat_history[0].get("chat_id") is not None:
            chatid = chat_history[0]["chat_id"]
        else:
            chatid = 0

        if chat_history and chat_history[0]:
            chat_script = chat_history[0]['chat_script']
            formatted_chat_history = '\n'.join(f"{item['user']}: {item['message']}" for item in reversed(chat_script))
        else:
            formatted_chat_history = ''
            print("chat_history or its first item is None")
   
        filtered_tools = [tools[0]]
        filtered_tools += [tool for i, tool in enumerate(tools) if i in integration_ids and i != 0]
        formatted_entities = '\n'.join([f"{item['entity']}: {item['description']}" for item in entities])
        asyncio.create_task(save_entities(userid, first_name, message, formatted_entities, chat_history, chatid))

        llm=PromptLayerChatOpenAI(openai_api_key = settings.OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0.05, pl_tags=[f"{ userid }"], return_pl_id=True)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        today = datetime.today()
        suffix = 'th' if 11 <= today.day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(today.day % 10, 'th')
        current_date = today.strftime(f"%d{suffix} %B %Y")

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
            current_history = formatted_chat_history,
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
            filtered_tools,
            llm,
            # return_intermediate_steps=True,
            agent=pandaAgent,
            agent_kwargs={"prefix": MY_PREFIX, "suffix": MY_SUFFIX, "format_instructions": MY_FORMAT_INSTRUCTIONS, "ai_prefix": "🐼 panda.ai", "human_prefix": f"{username}"}, verbose=True, memory=memory
        )

        prompt_template = pandaAgent.create_prompt(
            filtered_tools,
            MY_PREFIX,
            MY_SUFFIX,
            MY_FORMAT_INSTRUCTIONS,
        )

        tokens = num_tokens_from_string(prompt_template.template, "cl100k_base")

        try:
            response = agent_chain.run(input=f"{ message }")

            # check if response is None or an empty string
            if not response:
                logging.error("Received blank response from agent_chain.run")
                asyncio.create_task(save_new_message(userid, chatid, message, "Apologies! Something has gone wrong, please try again later.", tokens, False, "error"))
                return JSONResponse(content={"response": "Apologies! Something has gone wrong, please try again later."})

            asyncio.create_task(save_new_message(userid, chatid, message, response, tokens, True, "message"))
            return JSONResponse(content={"response": response})

        except requests.exceptions.RequestException as e:
            logging.error(f"Network error while running agent_chain: {e}")
            asyncio.create_task(save_new_message(userid, chatid, message, "Apologies! We're experiencing network issues. Please try again later.", tokens, False, "error"))
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service temporarily unavailable")

        except ValueError as e:
            logging.error(f"Value error while running agent_chain: {e}")
            asyncio.create_task(save_new_message(userid, chatid, message, "Apologies! Something was wrong with the input. Please try again.", tokens, False, "error"))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")

        except Exception as e:
            logging.error(f"Unexpected error while running agent_chain: {e}")
            asyncio.create_task(save_new_message(userid, chatid, message, "Apologies! Something has gone wrong, please try again later.", tokens, False, "error"))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


async def save_entities(userid: str, first_name: str, message: str, entities: str, chat_history: List, chatid: int):
    entity_llm=PromptLayerChatOpenAI(openai_api_key = settings.OPENAI_API_KEY, model_name="gpt-3.5-turbo", temperature=0, pl_tags=[f"{ userid }", "entityCreation"])
    if chat_history and chat_history[0]:
        chat_script = chat_history[0]['chat_script']
        formatted_chat_history = '\n'.join(f"{item['user']}: {item['message']}" for item in reversed(chat_script))
    else:
        formatted_chat_history = ''
        print("chat_history or its first item is None")
    
    ENTITY_PROMPT = promptlayer.prompts.get("main_panda_chat_entity_saving")

    ENTITY_DICT = ENTITY_PROMPT['template']

    MY_ENTITY_DICT = ENTITY_DICT.format(
        chat_history = formatted_chat_history,
        entities = entities,
        message = message,
        first_name = first_name
    )

    tokens = num_tokens_from_string(MY_ENTITY_DICT, "cl100k_base")
    response = entity_llm([HumanMessage(content=MY_ENTITY_DICT)])

    if response:
        new_entities = parse_entities_message(response.content)

        # Check if new_entities is not None
        if new_entities is None:
            logging.info("No new entities were parsed from the response.")
            return
        
        # Check if new_entities is an empty dictionary
        if not new_entities:
            logging.info("The entities dictionary is empty.")
            return # or raise an exception, or handle the error in some other way

        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        table = dynamodb.Table('panda-ai-entities')
        timestamp = datetime.utcnow().isoformat()

        try:
            for entity, description in new_entities.items():
                # Skip this iteration if the entity or description is empty
                if not entity or not description:
                    continue

                # Skip this iteration if the description contains 'already saved'
                target_strings = ['already saved', 'saved entity']
                if any(target in description.lower() for target in target_strings):
                    continue

                # Check if the description ends with '(updated information)'
                if description.endswith('(updated information)'):
                    # Remove the '(updated information)' part from the description
                    description = description.replace('(updated information)', '').strip()

                    # Fetch the current description from the database
                    current_entry = table.get_item(
                        Key={
                            'userId': userid,
                            'entity': entity
                        }
                    )

                    # Append the new information to the current description
                    if 'Item' in current_entry:
                        current_description = current_entry['Item'].get('description', '')
                        description = current_description + '. ' + description

                # Remove anything in brackets at the end of the value
                entity = re.sub(r'\(.*\)$', '', entity).strip()
                description = re.sub(r'\(.*\)$', '', description).strip()

                response = table.update_item(
                    Key={
                        'userId': userid,
                        'entity': entity
                    },
                    UpdateExpression="SET description = :description, updated = :updated, created_at = if_not_exists(created_at, :created_at)",
                    ExpressionAttributeValues={
                        ':description': description,
                        ':updated': timestamp,
                        ':created_at': timestamp
                    },
                    ReturnValues="UPDATED_NEW"
                )

                # Compute embedding for the description and add it to Pinecone
                embedding_description = entity + ': ' + description
                embedding = model.encode([embedding_description])[0]
                embedding = [embedding.tolist()]
                unique_id = userid + "/" + entity
                metadata = {"user_id": userid}
                pinecone_response = index.upsert(vectors=[(unique_id, embedding, metadata)], namespace='panda-ai-entities')

                if response['ResponseMetadata']['HTTPStatusCode'] == 200 and pinecone_response['upserted_count'] == 1:
                    continue
                else:
                    logging.error(f"Failed to update entities. Response: {response}")
                    return asyncio.create_task(save_new_message(userid, chatid, message, "Failed to update entities", tokens, False, "error"))
                
            return asyncio.create_task(save_new_message(userid, chatid, message, "Entities updated and saved successfully", tokens, True, "entity"))

        except ClientError as e:
            logging.error(e.response['Error']['Message'])
            return asyncio.create_task(save_new_message(userid, chatid, message, "Failed to update entities", tokens, False, "error"))

    else:
        asyncio.create_task(save_new_message(userid, chatid, message, "Entities not created", tokens, False, "error"))
        raise HTTPException(status_code=400, detail="An error occurred while saving the entities.")


def parse_entities_message(message: str) -> Dict[str, str]:
    # Split the message by newline
    lines = message.split("\n")

    # Initialize an empty dictionary
    entities = {}

    # Iterate over each line
    for line in lines:
        # Skip the first line that only contains "New Entities:"
        if line == "New Entities":
            continue

        # Skip the line if it does not contain a colon
        if ":" not in line:
            continue

        # Split the line into entity and description using the first colon as a separator
        entity, description = line.split(":", 1)

        # Remove leading and trailing whitespace
        entity = entity.strip()
        description = description.strip()

        # Remove leading dash and space from entity
        entity = entity.lstrip('- ')

        # Add the entity and its description to the dictionary
        entities[entity] = description

    # Return the entities dictionary even if it is empty
    return entities

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


async def save_new_message(user_id: str, chat_id: int, message: str, message_response: str, tokens: int, success: bool, type: str):

    cost = round((tokens/1000) * 0.002, 6)  # Calculate the cost for GPT 3.5 TURBO

    values = {
        "user_id": user_id,
        "chat_id": chat_id,
        "message": message,
        "message_response": message_response,
        "tokens": tokens,
        "cost": cost,
        "success": success,
        "type": type
    }

    query = """
        INSERT INTO panda_ai_messages (user_id, chat_id, message, message_response, tokens, cost, success, type)
        VALUES (:user_id, :chat_id, :message, :message_response, :tokens, :cost, :success, :type)
    """

    await database.execute(query=query, values=values)
    return {"message": "User data inserted successfully"}


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


async def get_user_messages_this_month(user_id: str):
    query = "SELECT COUNT(*) AS count FROM panda_ai_messages WHERE user_id = :user_id AND success = true AND EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM NOW()) AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM NOW())"
    values = {"user_id": user_id}
    result = await database.fetch_one(query=query, values=values)

    return result


async def get_subscriber_and_user_messages_per_month(user_id: str):
    query = "SELECT subscriber, messages_per_month FROM panda_ai_users WHERE user_id = :user_id"
    values = {"user_id": user_id}
    result = await database.fetch_one(query=query, values=values)

    return result

async def get_user_tools(user_id: str):
    query = "SELECT integration_id FROM panda_ai_user_integrations WHERE user_id = :user_id"
    values = {"user_id": user_id}
    result = await database.fetch_all(query=query, values=values)

    # Extract the integration_ids from the result
    integration_ids = [row["integration_id"] for row in result]

    return integration_ids

async def rate_message(userid: str, message: str, rating: str):
    if rating == "up":
        rating_bool = True
    elif rating == "down":
        rating_bool = False
    else:
        raise HTTPException(status_code=400, detail="Invalid rating")

    query = """
        UPDATE panda_ai_messages 
        SET thumb_rating = :rating 
        WHERE user_id = :user_id 
        AND message_response = :message 
        AND message_id = (
            SELECT MAX(message_id) 
            FROM panda_ai_messages 
            WHERE user_id = :user_id 
            AND message_response = :message
        )
    """
    values = {"user_id": userid, "message": message, "rating": rating_bool}
    await database.execute(query, values)

    return {"message": "Message rated successfully"}

async def feedback_message(userid: str, message: str, rating: str, feedback: str):
    if rating == "up":
        rating_bool = True
    elif rating == "down":
        rating_bool = False
    else:
        raise HTTPException(status_code=400, detail="Invalid rating")

    query = """
        UPDATE panda_ai_messages 
        SET feedback_comment = :feedback 
        WHERE user_id = :user_id 
        AND message_response = :message
        AND thumb_rating = :rating
        AND message_id = (
            SELECT MAX(message_id) 
            FROM panda_ai_messages 
            WHERE user_id = :user_id 
            AND message_response = :message
        )
    """
    values = {"user_id": userid, "message": message, "rating": rating_bool, "feedback": feedback}
    await database.execute(query, values)

    return {"message": "Message feedback saved successfully"}

async def end_trial(userid: str):
    query = """
        UPDATE panda_ai_users 
        SET subscriber = false, integrations = 0, messages_per_month = 0
        WHERE user_id = :user_id
    """
    values = {"user_id": userid}
    await database.execute(query, values)

    query2 = """
        SELECT email
        FROM panda_ai_users
        WHERE user_id = :user_id
    """
    values2 = {"user_id": userid}
    result = await database.execute(query2, values2)

    html = f"""\
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Free Trial Ended</title>
        </head>
        <body style="display: flex; flex-direction: column; align-items: center; justify-content: flex-start; background-color: #EFEFEF; font-family: Monaco; font-size: 12px; line-height: 1.5; color: #FFFFFF; min-height: 100%; max-width: 600px; border-radius: 10px; margin: 0 auto;">   
            <table width="90%" cellpadding="0" cellspacing="0" role="presentation" style="margin-top: 20px; background-color: #000000; border-radius: 10px; text-align: center;">
                <tr>
                    <td style="padding: 40px; font-size: 12px;">
                    <a href="https://www.mypanda.ai?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=logo"><img src="https://s3.eu-west-2.amazonaws.com/panda.ai/panda-standard.png" class="biglogo" width="100" /></a>
                    <a href="https://www.mypanda.ai?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=title" style="text-decoration: none;"><h1 style="font-size: 24px; font-weight: bold; text-align: center; color: #FFFFFF; margin-bottom: 20px;">YOUR FREE TRIAL HAS ENEDED</h1></a>
                    <p style="text-align: left;">Hi,</p>
                    <p style="text-align: left;">Thank you for trying 🐼 panda.ai. Your free trial of 20 messages has now ended.</p>
                    <p style="text-align: left;">If you would like to continue using 🐼 panda.ai you can sign up to one of our <a href="https://www.mypanda.ai/subscriptions?utm_source=panda.ai&utm_medium=email&utm_campaign=trial_end&utm_content=subscription_link">subscription packages</a>.</p>
                    <p style="text-align: left;">We have lots of options to choose from, like our Mei plan that gives you 300 messages per month and access to 5 of our integrations. You can sign up for just a month and cancel at any time.</p>
                    <p style="text-align: left;">We really hope you enjoyed using 🐼 panda.ai and are interested in any ideas of feedback you might have. You can make new idea suggestions <a href="https://www.mypanda.ai/roadmap?utm_source=panda.ai&utm_medium=email&utm_campaign=trial_end&utm_content=roadmap_link">here</a> and feedback using the form <a href="https://www.mypanda.ai/contact?utm_source=panda.ai&utm_medium=email&utm_campaign=trial_end&utm_content=contact_us_link">here</a>.</p>
                    <p style="text-align: left;">Thank you again for trying 🐼 panda.ai!</p>
                    <p style="text-align: left;">Love & hugs,</p>
                    <p style="text-align: left;"><strong>🐼</strong></p>
                    </td>
                </tr>
            </table>
            <div data-role="module-unsubscribe" class="module" role="module" data-type="unsubscribe" style="color:#444444; font-size:12px; line-height:20px; padding:16px 16px 16px 16px; text-align:Center;" data-muid="4e838cf3-9892-4a6d-94d6-170e474d21e5">
            
            <p style="font-size:12px; line-height:20px; color: #000000;">
                <a href="[unsubscribe]" target="_blank" class="Unsubscribe--unsubscribeLink" style="font-family: Monaco; color: #000000; text-decoration:none;">
                UNSUBSCRIBE
                </a>
            </p>
            </div>
        </body>
    </html>
    """

    if result:
        try:
            decrypted_email = cipher_suite.decrypt(result["email"].encode()).decode('utf-8')
        except InvalidToken:
            return {"error": "Error decrpyting user data"} 

        await email_send('subscriptions@mypanda.ai', decrypted_email, 'Your Free Trial of 🐼 panda.ai has ended', html)