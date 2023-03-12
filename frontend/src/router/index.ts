import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import notFoundView from "../views/404View.vue";
import AccountView from "../views/AccountView.vue";
import ChatView from "../views/ChatView.vue";
import AboutView from "../views/AboutView.vue";
import RoadmapView from "../views/RoadmapView.vue";
import PrivacyView from "../views/PrivacyView.vue";
import SupportView from "../views/SupportView.vue";
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
      path: "/:pathMatch(.*)",
      name: "404",
      component: notFoundView,
    },
    {
      path: "/auth/:pathMatch(.*)*",
      name: "auth",
      component: () => import("../views/AuthView.vue"),
    },
    {
      path: "/user/account",
      name: "account",
      component: AccountView,
    },
    {
      path: "/user/chat",
      name: "chat",
      component: ChatView,
    },
    {
      path: "/about",
      name: "about",
      component: AboutView,
    },
    {
      path: "/roadmap",
      name: "roadmap",
      component: RoadmapView,
    },
    {
      path: "/privacy",
      name: "privacy",
      component: PrivacyView,
    },
    {
      path: "/support",
      name: "support",
      component: SupportView,
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
