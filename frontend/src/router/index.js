import { createRouter, createWebHistory } from "vue-router";
import * as Session from "supertokens-web-js/recipe/session";
import { checkAdmin } from "../composables/checkAdmin.js";
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
import EmailView from "../views/EmailView.vue";
import EmailVerificationView from "../views/EmailVerificationView.vue";
import PasswordResetView from "../views/PasswordResetView.vue";
import NewPasswordView from "../views/NewPasswordView.vue";
import TestView from "../views/TestView.vue";
import AdminView from "../views/AdminView.vue";
import UnsubscribeView from "../views/UnsubscribeView.vue";

// Authorization Guard
async function checkAuth(to, from, next) {
  const canAccess = await Session.doesSessionExist();
  if (!canAccess) return next("/signin");
  else return next();
}

// Admin Guard
async function adminGuard(to, from, next) {
  const userId = await Session.getUserId();
  const { checkAdmin: isUserAdmin } = checkAdmin(userId); // Destructure the checkAdmin function
  const canAccess = await isUserAdmin(); // Call the checkAdmin function
  if (!canAccess) return next("/auth/" + userId + "/account");
  else if (to.path === "/auth/admin" || to.path === "/auth/admin/") {
    return next("/auth/admin/dashboard");
  } else return next();
}

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
    // {
    //   path: "/signup",
    //   name: "signup",
    //   component: SignUpView,
    // },
    {
      path: "/password-reset",
      name: "passwordreset",
      component: PasswordResetView,
    },
    {
      path: "/reset-password",
      name: "newpassword",
      component: NewPasswordView,
    },
    {
      path: "/auth/email",
      name: "email",
      component: EmailView,
      beforeEnter: checkAuth,
    },
    {
      path: "/auth/verify-email",
      name: "emailverification",
      component: EmailVerificationView,
      beforeEnter: checkAuth,
    },
    {
      path: "/auth/:pathMatch(.*)*",
      name: "auth",
      beforeEnter: checkAuth,
    },
    {
      path: "/auth/:userid/account",
      name: "account",
      component: AccountView,
      props: true,
      beforeEnter: checkAuth,
    },
    {
      path: "/auth/:userid/chat",
      name: "chat",
      component: ChatView,
      props: true,
      beforeEnter: checkAuth,
    },
    {
      path: "/auth/:userid/onboarding",
      name: "onboarding",
      component: OnboardingView,
      props: true,
      beforeEnter: checkAuth,
    },
    {
      path: "/auth/admin/:pathMatch(.*)*",
      name: "admin",
      beforeEnter: adminGuard,
    },
    {
      path: "/auth/admin/dashboard",
      name: "admindashboard",
      component: AdminView,
      beforeEnter: adminGuard,
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
      path: "/unsubscribe",
      name: "unsubscribe",
      component: UnsubscribeView,
    },
    {
      path: "/auth/test",
      name: "test",
      component: TestView,
      beforeEnter: checkAuth,
    },
  ],
});

export default router;
