import ThirdPartyEmailPassword from "supertokens-web-js/recipe/thirdpartyemailpassword";
// import SessionReact from "supertokens-auth-react/recipe/session";
import EmailVerification from "supertokens-auth-react/recipe/emailverification";
import Session from "supertokens-web-js/recipe/session";

export const SuperTokensReactConfig = {
  appInfo: {
    appName: import.meta.env.VITE_APP_APP_NAME,
    apiDomain: import.meta.env.VITE_APP_API_URL,
    websiteDomain: import.meta.env.VITE_APP_BASE_URL,
  },
  recipeList: [
    ThirdPartyEmailPassword.init({}),
    EmailVerification.init({
      mode: "REQUIRED", // or "OPTIONAL"
    }),
    Session.init(),
  ],
};

export const SuperTokensWebJSConfig = {
  appInfo: {
    appName: import.meta.env.VITE_APP_APP_NAME,
    apiDomain: import.meta.env.VITE_APP_API_URL,
  },
  recipeList: [EmailVerification.init(), Session.init(), ThirdPartyEmailPassword.init()],
};
