import ThirdPartyEmailPasswordReact, {
  Github,
  Google,
  Apple,
} from "supertokens-auth-react/recipe/thirdpartyemailpassword";
import SessionReact from "supertokens-auth-react/recipe/session";
import EmailVerification from "supertokens-auth-react/recipe/emailverification";
import Session from "supertokens-web-js/recipe/session";
import { getUserChatHistory } from "./composables/getUserChatHistory.js";

export const SuperTokensReactConfig = {
  appInfo: {
    appName: "panda.ai",
    apiDomain: "http://localhost:3001",
    websiteDomain: "http://localhost:3000",
  },
  recipeList: [
    ThirdPartyEmailPasswordReact.init({
      useShadowDom: false,
      signInAndUpFeature: {
        providers: [Github.init(), Google.init(), Apple.init()],
        signUpForm: {
          termsOfServiceLink: "http://localhost:3000/terms-of-service",
          privacyPolicyLink: "http://localhost:3000/privacy-policy",
        },
      },
      getRedirectionURL: async (context) => {
        const userid = await Session.getUserId();
        const userChatHistory = await getUserChatHistory(userid);
        if (context.action === "SUCCESS") {
          if (context.redirectToPath !== undefined) {
            // we are navigating back to where the user was before they authenticated
            return context.redirectToPath;
          } else if (userChatHistory.length == 0) {
            return "/" + userid + "/onboarding";
          } else {
            return "/" + userid + "/chat";
          }
        }
        return undefined;
      },
      style: `
        [data-supertokens~=container] {
          font-family: "Monaco";
          text-transform: uppercase;
          --palette-background: 0, 0, 0;
          --palette-inputBackground: 255, 255, 255;
          --palette-inputBorder: 0, 0, 0;
          --palette-textTitle: 255, 255, 255;
          --palette-textLabel: 255, 255, 255;
          --palette-textPrimary: 255, 255, 255;
          --palette-error: 255, 203, 76;
          --palette-textInput: 0, 0, 0;
          --palette-buttonText: 0, 0, 0;
          --palette-textLink: 255, 203, 76;
          --palette-primary: 255, 203, 76;
          --palette-primaryBorder: 255, 203, 76;
          --palette-superTokensBrandingBackground: 255, 255, 255;
          --palette-superTokensBrandingText: 0, 0, 0;
        }
        [data-supertokens~="providerButton"] {
          max-width: 280px !important;
        }
        [data-supertokens~="providerButtonText"] {
          font-family: "Monaco";
          text-transform: uppercase;
        }
        [data-supertokens~="inputWrapper"] {
          font-family: "Monaco";
        }
        [data-supertokens~="inputWrapper"]:focus-within {
          background-color: #FFFFFF;
          font-family: "Monaco";
          border: 3px solid #FFCB4C;
          border-radius: 5px;
        }
      `,
    }),
    EmailVerification.init({
      mode: "REQUIRED", // or "OPTIONAL"
    }),
    SessionReact.init(),
  ],
};

export const SuperTokensWebJSConfig = {
  appInfo: {
    appName: "panda.ai",
    apiDomain: "http://localhost:3001",
  },
  recipeList: [EmailVerification.init(), Session.init()],
};
