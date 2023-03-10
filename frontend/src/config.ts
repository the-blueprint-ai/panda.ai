import ThirdPartyEmailPasswordReact, {
  Github,
  Google,
  Apple,
} from "supertokens-auth-react/recipe/thirdpartyemailpassword";
import SessionReact from "supertokens-auth-react/recipe/session";
import EmailVerification from "supertokens-auth-react/recipe/emailverification";
import Session from "supertokens-web-js/recipe/session";

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
      },
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
