import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import SuperTokens from "supertokens-web-js";
import "./assets/styles/panda-main.css";
import { SuperTokensWebJSConfig } from "./config";
import axios from "axios";
import FloatingVue from 'floating-vue'

SuperTokens.init(SuperTokensWebJSConfig);

const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://localhost:3001"; // the FastAPI backend

app.use(router);
app.use(store);
app.use(FloatingVue);

app.mount("#app");
