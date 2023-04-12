import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueGtag from "vue-gtag";
import SuperTokens from "supertokens-web-js";
import "./assets/styles/panda-main.css";
import { SuperTokensWebJSConfig } from "./config";
import axios from "axios";

SuperTokens.init(SuperTokensWebJSConfig);

const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL;

app.use(router);
app.use(store);
app.use(
  VueGtag,
  {
    appName: 'panda.ai',
    pageTrackerScreenviewEnabled: true,
    config: { id: "G-HS1DM7DQXW" },
  },
  router
);

app.mount("#app");
