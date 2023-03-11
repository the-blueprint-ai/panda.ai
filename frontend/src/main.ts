import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import SuperTokens from "supertokens-web-js";
import "./assets/styles/panda-main.css";
import { SuperTokensWebJSConfig } from "./config";

SuperTokens.init(SuperTokensWebJSConfig);

const app = createApp(App);

app.use(router);

app.mount("#app");
