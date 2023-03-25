from pydantic import BaseSettings
from dotenv import dotenv_values
import os

from supertokens_python.recipe import session, thirdpartyemailpassword, dashboard, emailverification, usermetadata
from supertokens_python.recipe.thirdpartyemailpassword import (
    Apple,
    Github,
    Google,
)
from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
)

# Python Environment Variable setup required on System or .env file
config_env = {
    **dotenv_values(".env"),  # load local file development variables
    **os.environ,  # override loaded values with system environment variables
}

class Settings(BaseSettings):
    S3_BUCKET: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    PSQL_DATABASE_URL: str
    FERNET_KEY: str
    SPTKNS_CONNECTION_URI: str
    SPTKNS_API_KEY: str
    SPTKNS_DASHBOARD_API_KEY: str
    APP_NAME: str
    API_DOMAIN: str
    WEBSITE_DOMAIN: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    FACEBOOK_CLIENT_ID: str
    FACEBOOK_CLIENT_SECRET: str
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    APPLE_CLIENT_ID: str
    APPLE_CLIENT_KEY_ID: str
    APPLE_CLIENT_TEAM_ID: str
    APPLE_CLIENT_PRIVATE_KEY: str

# specify .env file location as Config attribute
    class Config:
        env_file = ".env"

# global instance
settings = Settings()

# This is the location of the SuperTokens core.
supertokens_config = SupertokensConfig(
    # https://try.supertokens.com is for demo purposes. Replace this with the address of your core instance (sign up on supertokens.com), or self host a core.
    connection_uri=settings.SPTKNS_CONNECTION_URI,
    api_key=settings.SPTKNS_API_KEY
)

app_info = InputAppInfo(
    app_name=settings.APP_NAME,
    api_domain=settings.API_DOMAIN,
    website_domain=settings.WEBSITE_DOMAIN,
)

framework = "fastapi"

# RecipeList contains all the modules that you want to
# Use from SuperTokens. See the full list here: https://supertokens.com/docs/guides
recipe_list = [
    session.init(), # initializes session features
    thirdpartyemailpassword.init(
        providers=[
            # We have provided you with development keys which you can use for testing.
            # IMPORTANT: Please replace them with your own OAuth keys for production use.
            Google(
                is_default=True,
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET
            ),
            # Facebook(
            #     client_id=settings.FACEBOOK_CLIENT_ID,
            #     client_secret=settings.FACEBOOK_CLIENT_SECRET
            # ),
            Github(
                is_default=True,
                client_id=settings.GITHUB_CLIENT_ID,
                client_secret=settings.GITHUB_CLIENT_SECRET,
            ),
            Apple(
                is_default=True,
                client_id=settings.APPLE_CLIENT_ID,
                client_key_id=settings.APPLE_CLIENT_KEY_ID,
                client_team_id=settings.APPLE_CLIENT_TEAM_ID,
                client_private_key=settings.APPLE_CLIENT_PRIVATE_KEY,
            ),
        ]
    ),
    usermetadata.init(),
    emailverification.init(mode='REQUIRED'),
    dashboard.init(api_key=settings.SPTKNS_DASHBOARD_API_KEY)
]
