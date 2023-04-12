import ThirdPartyEmailPassword from "supertokens-web-js/recipe/thirdpartyemailpassword";
import EmailVerification from "supertokens-web-js/recipe/emailverification";
import Session from "supertokens-web-js/recipe/session";

export const SuperTokensWebJSConfig = {
  appInfo: {
    appName: import.meta.env.VITE_APP_APP_NAME,
    apiDomain: import.meta.env.VITE_APP_API_URL,
    websiteDomain: import.meta.env.VITE_APP_BASE_URL,
  },
  recipeList: [
    EmailVerification.init({
      mode: "REQUIRED", // or "OPTIONAL"
    }),
    Session.init(),
    ThirdPartyEmailPassword.init(),
  ],
};
