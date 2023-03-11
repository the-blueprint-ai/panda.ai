import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import UserView from "../views/UserView.vue";
import ChatView from "../views/ChatView.vue";
import PrivacyPolicyView from "../views/PrivacyPolicyView.vue";
import TermsOfServiceView from "../views/TermsOfServiceView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/auth/:pathMatch(.*)*",
      name: "auth",
      component: () => import("../views/AuthView.vue"),
    },
    {
      path: "/user",
      name: "user",
      component: UserView,
    },
    {
      path: "/user/chat",
      name: "chat",
      component: ChatView,
    },
    {
      path: "/privacy-policy",
      name: "privacypolicy",
      component: PrivacyPolicyView,
    },
    {
      path: "/terms-of-service",
      name: "termsofservice",
      component: TermsOfServiceView,
    },
  ],
});

export default router;
