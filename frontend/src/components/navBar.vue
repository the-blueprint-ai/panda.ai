<script>
import * as Session from "supertokens-web-js/recipe/session";

export default {
  data() {
    return {
      session: false,
      userId: "",
    };
  },
  computed: {
    isOpen() {
      return this.$store.state.isOpen;
    },
    avatar() {
      return this.$store.state.userStore.avatar;
    },
  },
  mounted() {
    this.getUserInfo();
  },

  methods: {
    setIsOpenValue(value) {
      this.$store.commit('setIsOpen', value);
    },
    redirectToLogin() {
      window.location.href = "/auth";
    },
    async getUserInfo() {
      this.session = await Session.doesSessionExist();
      if (this.session) {
        this.userId = await Session.getUserId();
      }
    },
    async onLogout() {
      await Session.signOut();
      window.location.href = "/";
    },
    userLink() {
      if (this.userId) {
        return { name: "user", param: { userid: this.userId } };
      } else {
        return { name: "user", param: { userid: "userID" } };
      }
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
  },
};
</script>

<template>
  <div class="navbar">
    <div class="navbar-top">
      <div class="brand-holder">
        <router-link to="/">
          <img class="logo" src="../../src/assets/panda.png" width="50" />
        </router-link>
        <p>panda.ai</p>
      </div>
      <div class="menu-items">
        <div class="menu-icon">
          <router-link to="/">
            <img
              src="../../src/assets/house-door.svg"
              class="homesvg"
              alt="home"
            />
          </router-link>
          <p>home</p>
        </div>
        <div class="menu-icon">
          <router-link to="/about">
            <img
              src="../../src/assets/file-person.svg"
              class="homesvg"
              alt="about"
            />
          </router-link>
          <p>about</p>
        </div>
        <div class="menu-icon">
          <router-link to="/roadmap">
            <img src="../../src/assets/geo.svg" class="homesvg" alt="roadmap" />
          </router-link>
          <p>roadmap</p>
        </div>
        <div class="menu-icon">
          <router-link to="/privacy">
            <img
              src="../../src/assets/file-earmark-lock.svg"
              class="homesvg"
              alt="privacy"
            />
          </router-link>
          <p>privacy</p>
        </div>
      </div>
      <div class="account-items">
        <img
          src="../../src/assets/caret-down-fill.svg"
          class="downsvg"
          ref="menu"
          @click="openClose"
        />
        <div class="dropdown-menu" v-if="isOpen">
          <div class="dropdown-links">
            <router-link :to="'/' + userId + '/chat'">
              <button class="dropdown-button-top">Chat</button>
            </router-link>
            <div class="dropdown-bar"></div>
            <router-link :to="'/' + userId + '/account'">
              <button class="dropdown-button">Account</button>
            </router-link>
            <div class="dropdown-bar"></div>
            <div v-if="session">
              <button class="dropdown-button" @click="onLogout">Logout</button>
            </div>
            <div v-else>
              <router-link to="/auth">
                <button class="dropdown-button">Login</button>
              </router-link>
            </div>
            <div class="dropdown-bar"></div>
            <div class="dropdown-bottom"></div>
          </div>
        </div>
        <img
          class="user-icon"
          v-bind:src="avatar"
          ref="menu"
          @click="openClose"
        />
        <div v-if="session">
          <button class="authButton-login" @click="onLogout">Logout</button>
        </div>
        <div v-else>
          <button class="authButton-signup" @click="redirectToLogin">
            Sign up
          </button>
          <button class="authButton-login" @click="redirectToLogin">
            Login
          </button>
        </div>
        <div class="menu-icon">
          <router-link to="/support">
            <img
              src="../../src/assets/question-square.svg"
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
