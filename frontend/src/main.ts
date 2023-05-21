import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VueGtag from "vue-gtag";
import SuperTokens from "supertokens-web-js";
import Toast, { POSITION } from "vue-toastification";
import "../node_modules/bootstrap/scss/bootstrap.scss";
import "@/assets/styles/panda-bootstrap-overrides.scss";
import { SuperTokensWebJSConfig } from "./config";
// import axios from "axios";

import "bootstrap";

SuperTokens.init(SuperTokensWebJSConfig);

const app = createApp(App);

router.afterEach((to, from) => {
  store.commit("setIsOpen", false);
});

// axios.defaults.withCredentials = true;
// axios.defaults.baseURL = import.meta.env.VITE_APP_API_URL;

app.use(router);
app.use(store);
app.use(Toast, {
  transition: "Vue-Toastification__bounce",
  position: POSITION.TOP_RIGHT,
  timeout: 5000,
  maxToasts: 20,
  newestOnTop: true,
  showCloseButtonOnHover: true,
  draggable: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  closeOnClick: true,
});
app.use(
  VueGtag,
  {
    appName: "panda.ai",
    config: { id: "G-HS1DM7DQXW" },
  },
  router
);

app.mount("#app");
