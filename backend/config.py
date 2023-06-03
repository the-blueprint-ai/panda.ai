from pydantic import BaseSettings
from dotenv import dotenv_values
from typing import Dict, Any
import os

from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
)
from supertokens_python.recipe import session, thirdpartyemailpassword, dashboard, emailverification
from supertokens_python.recipe.thirdpartyemailpassword import (
    Apple,
    Github,
    Google,
)
from supertokens_python.recipe.thirdpartyemailpassword.types import EmailDeliveryOverrideInput, EmailTemplateVars
from supertokens_python.ingredients.emaildelivery.types import EmailDeliveryConfig
from supertokens_python.recipe.emailverification.types import EmailDeliveryOverrideInput as EVEmailDeliveryOverrideInput, EmailTemplateVars as EVEmailTemplateVars

import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi import HTTPException

# Python Environment Variable setup required on System or .env file
config_env = {
    **dotenv_values(".env"),  # load local file development variables
    **os.environ,  # override loaded values with system environment variables
}

class Settings(BaseSettings):
    APP_NAME: str
    API_DOMAIN: str
    WEBSITE_DOMAIN: str
    WEBHOOKS_USERNAME: str
    WEBHOOKS_PASSWORD: str
    SUBSCRIPTIONS_USERNAME: str
    SUBSCRIPTIONS_PASSWORD: str
    STRIPE_API_KEY: str
    STRIPE_SUBSCRIPTION_UPDATED_ENDPOINT_SECRET: str
    STRIPE_SUBSCRIPTION_DELETED_ENDPOINT_SECRET: str
    STRIPE_CUSTOMER_CREATED_ENDPOINT_SECRET: str
    S3_BUCKET: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    PSQL_DATABASE_URL: str
    FERNET_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT_NAME: str
    SPTKNS_CONNECTION_URI: str
    SPTKNS_API_KEY: str
    SPTKNS_DASHBOARD_API_KEY: str
    SENDGRID_API_KEY: str
    OPENAI_ORGANISATION: str
    OPENAI_API_KEY: str
    PRMPTLYR_API_KEY: str
    GOOGLE_SEARCH_API_KEY: str
    GOOGLE_SEARCH_ENGINE_ID: str
    GOOGLE_MAPS_API_KEY: str
    YOUTUBE_API_KEY: str
    GOOGLE_GEOCODING_API_KEY: str
    TMDB_API_KEY: str
    SPOTIFY_TOKEN_URL: str
    SPOTIFY_SEARCH_URL: str
    SPOTIFY_EMBED_URL: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    WOLFRAM_ALPHA_APPID: str
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
    connection_uri=settings.SPTKNS_CONNECTION_URI,
    api_key=settings.SPTKNS_API_KEY
)

app_info = InputAppInfo(
    app_name=settings.APP_NAME,
    api_domain=settings.API_DOMAIN,
    website_domain=settings.WEBSITE_DOMAIN,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

framework = "fastapi"

def custom_email_delivery(original_implementation: EmailDeliveryOverrideInput) -> EmailDeliveryOverrideInput:
    original_send_email = original_implementation.send_email

    async def send_email(template_vars: EmailTemplateVars, user_context: Dict[str, Any]) -> None:
        # You can change the path, domain of the reset password link,
        # or even deep link it to your mobile app
        # This is: `${websiteDomain}${websiteBasePath}/reset-password`
        template_vars.password_reset_link = template_vars.password_reset_link.replace(
            f"{settings.WEBSITE_DOMAIN}/auth/reset-password", f"{settings.WEBSITE_DOMAIN}/reset-password")
        return await original_send_email(template_vars, user_context)

    original_implementation.send_email = send_email
    return original_implementation


def custom_emailverification_delivery(original_implementation: EVEmailDeliveryOverrideInput) -> EVEmailDeliveryOverrideInput:
    original_send_email = original_implementation.send_email

    async def send_email(template_vars: EVEmailTemplateVars, user_context: Dict[str, Any]) -> None:
        email_verify_content=f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Verification</title>
            </head>
            <body style="display: flex; flex-direction: column; align-items: center; justify-content: flex-start; background-color: #EFEFEF; font-family: Monaco; font-size: 12px; line-height: 1.5; color: #FFFFFF; min-height: 100%; max-width: 600px; border-radius: 10px; margin: 0 auto;">   
                <table width="90%" cellpadding="0" cellspacing="0" role="presentation" style="margin-top: 20px; background-color: #000000; border-radius: 10px; text-align: center;">
                    <tr>
                        <td style="padding: 40px; font-size: 12px;">
                        <a href="https://www.mypanda.ai?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=logo"><img src="https://s3.eu-west-2.amazonaws.com/panda.ai/panda-standard.png" class="biglogo" width="100" /></a>
                        <a href="https://www.mypanda.ai?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=title" style="text-decoration: none;"><h1 style="font-size: 24px; font-weight: bold; text-align: center; color: #FFFFFF; margin-bottom: 20px;">EMAIL VERIFICATION</h1></a>
                        <p style="text-align: left;">Hi,</p>
                        <p style="text-align: left;">Please verify your email address for 🐼 panda.ai by clicking the button below:</p>
                        <div style="border-radius: 6px; margin-bottom: 15px; display: block; text-align: center;">
                            <a href="{template_vars.email_verify_link}" target="_blank"
                                style="background: #FFCB4C; font-size: 14px; line-height: 24px; font-family: Monaco; text-decoration: none; padding: 9px 25px 9px 25px; color: #000000; display: block; border-radius: 6px; width: fit-content; margin: 0 auto;">
                                VERIFY MY EMAIL
                            </a>
                        </div>
                        <p style="text-align: left;">If you have any questions, don't hesitate to reach out to our support team. We're here to help!</p>
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

        message = Mail(
        from_email="verify@mypanda.ai",
        to_emails=template_vars.user.email,
        subject="🐼 panda.ai Email Verification",
        html_content=email_verify_content)

        try:
            sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

            response = sg.send(message)
            return{"Email sent successfully"}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while trying to send email: {e}")

    original_implementation.send_email = send_email
    return original_implementation


# RecipeList contains all the modules that you want to
# Use from SuperTokens. See the full list here: https://supertokens.com/docs/guides
recipe_list = [
    session.init(), # initializes session features
    thirdpartyemailpassword.init(
        email_delivery=EmailDeliveryConfig(override=custom_email_delivery),
        providers=[
            # We have provided you with development keys which you can use for testing.
            # IMPORTANT: Please replace them with your own OAuth keys for production use.
            # Google(
            #     is_default=True,
            #     client_id=settings.GOOGLE_CLIENT_ID,
            #     client_secret=settings.GOOGLE_CLIENT_SECRET
            # ),
            # # Facebook(
            # #     client_id=settings.FACEBOOK_CLIENT_ID,
            # #     client_secret=settings.FACEBOOK_CLIENT_SECRET
            # # ),
            # Github(
            #     is_default=True,
            #     client_id=settings.GITHUB_CLIENT_ID,
            #     client_secret=settings.GITHUB_CLIENT_SECRET,
            # ),
            # Apple(
            #     is_default=True,
            #     client_id=settings.APPLE_CLIENT_ID,
            #     client_key_id=settings.APPLE_CLIENT_KEY_ID,
            #     client_team_id=settings.APPLE_CLIENT_TEAM_ID,
            #     client_private_key=settings.APPLE_CLIENT_PRIVATE_KEY,
            # ),
        ]
    ),
    emailverification.init(
        mode='REQUIRED',
        email_delivery=EmailDeliveryConfig(override=custom_emailverification_delivery)
    ),
    dashboard.init(api_key=settings.SPTKNS_DASHBOARD_API_KEY)
]
