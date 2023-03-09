from supertokens_python.recipe import session, thirdpartyemailpassword, dashboard
from supertokens_python.recipe.thirdpartyemailpassword import (
    Apple,
    Github,
    Google,
)
from supertokens_python import (
    InputAppInfo,
    SupertokensConfig,
)

# this is the location of the SuperTokens core.
supertokens_config = SupertokensConfig(
    # https://try.supertokens.com is for demo purposes. Replace this with the address of your core instance (sign up on supertokens.com), or self host a core.
    connection_uri="https://dev-32918f51bebd11eda5a2f94364e3b284-eu-west-1.aws.supertokens.io:3569",
    api_key="RzoL-gH6kIvoimEbpxGr7bfAjiQT=n"
)

app_info = InputAppInfo(
    app_name="panda.ai",
    api_domain="http://localhost:3001",
    website_domain="http://localhost:3000",
)

framework = "fastapi"

# recipeList contains all the modules that you want to
# use from SuperTokens. See the full list here: https://supertokens.com/docs/guides
recipe_list = [
    session.init(), # initializes session features
    thirdpartyemailpassword.init(
        providers=[
            # We have provided you with development keys which you can use for testing.
            # IMPORTANT: Please replace them with your own OAuth keys for production use.
            Google(
                is_default=True,
                client_id="1060725074195-kmeum4crr01uirfl2op9kd5acmi9jutn.apps.googleusercontent.com",
                client_secret="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"
            ),
            # Facebook(
            #     client_id='FACEBOOK_CLIENT_ID',
            #     client_secret='FACEBOOK_CLIENT_SECRET'
            # ),
            Github(
                is_default=True,
                client_id="467101b197249757c71f",
                client_secret="e97051221f4b6426e8fe8d51486396703012f5bd",
            ),
            Apple(
                is_default=True,
                client_id="4398792-io.supertokens.example.service",
                client_key_id="7M48Y4RYDL",
                client_team_id="YWQCXGJRJL",
                client_private_key="-----BEGIN PRIVATE KEY-----\nMIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgu8gXs+XYkqXD6Ala9Sf/iJXzhbwcoG5dMh1OonpdJUmgCgYIKoZIzj0DAQehRANCAASfrvlFbFCYqn3I2zeknYXLwtH30JuOKestDbSfZYxZNMqhF/OzdZFTV0zc5u5s3eN+oCWbnvl0hM+9IW0UlkdA\n-----END PRIVATE KEY-----",
            ),
        ]
    ),
    dashboard.init(api_key="63818ab7-a904-409e-acc7-b8b5092974e1")
]
