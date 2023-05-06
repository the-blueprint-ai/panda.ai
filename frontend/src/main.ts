import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueGtag from "vue-gtag";
import SuperTokens from "supertokens-web-js";
// import "@/assets/styles/panda-global.scss";
import "../node_modules/bootstrap/scss/bootstrap.scss";
import "@/assets/styles/panda-bootstrap-overrides.scss";
import { SuperTokensWebJSConfig } from "./config";
import axios from "axios";

import "bootstrap"

SuperTokens.init(SuperTokensWebJSConfig);

const app = createApp(App);

router.afterEach((to, from) => {
  store.commit("setIsOpen", false);
});

axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL;

app.use(router);
app.use(store);
app.use(
  VueGtag,
  {
    appName: 'panda.ai',
    config: { id: "G-HS1DM7DQXW" },
  },
  router
);

app.mount("#app");
