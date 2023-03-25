import { createRouter, createWebHistory } from "vue-router";
import * as Session from "supertokens-web-js/recipe/session";
import HomeView from "../views/HomeView.vue";
import notFoundView from "../views/404View.vue";
import AccountView from "../views/AccountView.vue";
import ChatView from "../views/ChatView.vue";
import OnboardingView from "../views/OnboardingView.vue";
import AboutView from "../views/AboutView.vue";
import SignInView from "../views/SignInView.vue";
import SignUpView from "../views/SignUpView.vue";
import RoadmapView from "../views/RoadmapView.vue";
import PrivacyView from "../views/PrivacyView.vue";
import SupportView from "../views/SupportView.vue";
import PrivacyPolicyView from "../views/PrivacyPolicyView.vue";
import TermsOfServiceView from "../views/TermsOfServiceView.vue";
import ContactView from "../views/ContactView.vue";
import TestView from "../views/TestView.vue";

// Authorization Guard
async function checkAuth(to, from, next) {
  const canAccess = await Session.doesSessionExist();
  if (!canAccess) return next("/auth");
  else return next();
};

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
      path: "/signin",
      name: "signin",
      component: SignInView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignUpView,
    },
    {
      path: "/auth/:pathMatch(.*)*",
      name: "auth",
      component: () => import("../views/AuthView.vue"),
    },
    {
      path: "/:userid/account",
      name: "account",
      component: AccountView,
      props: true,
      beforeEnter: checkAuth,
    },
    {
      path: "/:userid/chat",
      name: "chat",
      component: ChatView,
      props: true,
      beforeEnter: checkAuth,
    },
    {
      path: "/:userid/onboarding",
      name: "onboarding",
      component: OnboardingView,
      props: true,
      beforeEnter: checkAuth,
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
      path: "/contact",
      name: "contact",
      component: ContactView,
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
    {
      path: "/test",
      name: "test",
      component: TestView,
    },
  ],
});

export default router;
