<script>
import * as Session from "supertokens-web-js/recipe/session";
import { mapActions, mapGetters } from "vuex";
import { getUserData } from "../composables/getUserData.js";

export default {
  data() {
    return {};
  },
  computed: {
    ...mapGetters("userStore", {
      session: "getStoreSession",
      userId: "getStoreUserId",
      avatar: "getStoreAvatar",
      onboarded: "getStoreOnboarded",
      admin: "getStoreAdmin",
    }),
    isOpen() {
      return this.$store.state.isOpen;
    },
  },
  async mounted() {
    try {
      await this.getSession();
      if (this.session) {
        await this.getUserInfo();
      }
      if (this.userId) {
        const { userData } = getUserData(this.$store, this.userId);
        userData(this.userId);
      }
    } catch (error) {
      console.error("Error getting session/userData:", error);
    }
  },

  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    setIsOpenValue(value) {
      this.$store.commit("setIsOpen", value);
    },
    redirectToSignUp() {
      this.$router.push("/signup");
    },
    redirectToSignIn() {
      this.$router.push("/signin");
    },
    async onLogout() {
      await Session.signOut();
      window.location.href = ("http://localhost:3000/");
    },
    openClose() {
      var _this = this;

      const closeListener = (e) => {
        if (_this.catchOutsideClick(e, _this.$refs.menu))
          window.removeEventListener("click", closeListener),
            _this.setIsOpenValue(false);
      };

      window.addEventListener("click", closeListener);

      this.setIsOpenValue(!this.isOpen);
    },
    catchOutsideClick(event, dropdown) {
      // When user clicks menu — do nothing
      if (dropdown == event.target) return false;

      // When user clicks outside of the menu — close the menu
      if (this.isOpen && dropdown != event.target) return true;
    },
    goToUserDashboard() {
      window.open("http://localhost:3001/auth/dashboard");
    },
  },
};
</script>

<template>
  <div class="navbar">
    <div class="navbar-top">
      <div class="brandHolder">
        <router-link to="/">
          <img class="logo" src="../../src/assets/panda.png" width="50" />
        </router-link>
        <router-link to="/">
          <p>panda.ai</p>
        </router-link>
      </div>
      <div class="menu-items">
        <div class="menu-icon">
          <router-link to="/">
            <img
              src="../../src/assets/icons/house-door.svg"
              class="homesvg"
              alt="home"
            />
          </router-link>
          <p>home</p>
        </div>
        <div class="menu-icon">
          <router-link to="/about">
            <img
              src="../../src/assets/icons/file-person.svg"
              class="homesvg"
              alt="about"
            />
          </router-link>
          <p>about</p>
        </div>
        <div class="menu-icon">
          <router-link to="/roadmap">
            <img
              src="../../src/assets/icons/geo.svg"
              class="homesvg"
              alt="roadmap"
            />
          </router-link>
          <p>roadmap</p>
        </div>
        <div class="menu-icon">
          <router-link to="/privacy">
            <img
              src="../../src/assets/icons/file-earmark-lock.svg"
              class="homesvg"
              alt="privacy"
            />
          </router-link>
          <p>privacy</p>
        </div>
      </div>
      <div class="account-items">
        <img
          v-if="onboarded"
          src="../../src/assets/icons/caret-down-fill.svg"
          class="downsvg"
          ref="menu"
          @click="openClose"
        />
        <div class="dropdown-menu" v-if="isOpen">
          <div class="dropdown-links">
            <router-link :to="'/auth/' + userId + '/chat'">
              <button class="dropdown-button-top">Chat</button>
            </router-link>
            <div class="dropdown-bar"></div>
            <router-link :to="'/auth/' + userId + '/account'">
              <button class="dropdown-button">Account</button>
            </router-link>
            <div class="dropdown-bar"></div>
            <div v-if="admin">
              <router-link :to="'/auth/admin/dashboard'">
              <button class="dropdown-button">Admin Panel</button>
              </router-link>
              <div class="dropdown-bar"></div>
              <button class="dropdown-button" @click="goToUserDashboard">
                User Dashboard
              </button>
              <div class="dropdown-bar"></div>
            </div>
            <div v-if="session">
              <button class="dropdown-button" @click="onLogout">
                Sign Out
              </button>
            </div>
            <div v-else>
              <router-link to="/signin">
                <button class="dropdown-button">Sign In</button>
              </router-link>
            </div>
            <div class="dropdown-bar"></div>
            <div class="dropdown-bottom"></div>
          </div>
        </div>
        <img
          v-if="onboarded"
          class="user-icon"
          v-bind:src="avatar"
          ref="menu"
          @click="openClose"
        />
        <div v-else>
          <button class="authButton-signup" @click="redirectToSignUp">
            Sign up
          </button>
          <button class="authButton-login" @click="redirectToSignIn">
            Sign In
          </button>
        </div>
        <div class="menu-icon">
          <router-link to="/support">
            <img
              src="../../src/assets/icons/question-square.svg"
              class="homesvg"
              alt="support"
            />
          </router-link>
          <p>support</p>
        </div>
      </div>
    </div>
    <div class="navbarbar"></div>
  </div>
</template>
