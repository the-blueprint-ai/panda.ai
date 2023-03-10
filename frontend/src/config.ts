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
        signUpForm: {
          termsOfServiceLink: "https://example.com/terms-of-service",
          privacyPolicyLink: "https://example.com/privacy-policy"
        },
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
