<script lang="ts">
import * as Session from "supertokens-web-js/recipe/session";

export default {
  data: () => {
    return {
      session: false,
      userId: "",
      isOpen: false,
    };
  },
  mounted() {
    this.getUserInfo();
  },

  methods: {
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

      const closeListener = (e: any) => {
        if (_this.catchOutsideClick(e, _this.$refs.menu))
          window.removeEventListener("click", closeListener),
            (_this.isOpen = false);
      };

      window.addEventListener("click", closeListener);

      this.isOpen = !this.isOpen;
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
  <div className="navbar">
    <div className="navbar-top">
      <div className="brand-holder">
        <router-link to="/">
          <img className="logo" src="../../src/assets/panda.png" width="50" />
        </router-link>
        <p font-size="15px">panda.ai</p>
      </div>
      <div className="menu-items">
        <div className="menu-icon">
          <router-link to="/">
            <img
              src="../../src/assets/house-door.svg"
              className="homesvg"
              alt="home"
            />
          </router-link>
          <p>home</p>
        </div>
        <div className="menu-icon">
          <router-link to="/about">
            <img
              src="../../src/assets/file-person.svg"
              className="homesvg"
              alt="about"
            />
          </router-link>
          <p>about</p>
        </div>
        <div className="menu-icon">
          <router-link to="/roadmap">
            <img
              src="../../src/assets/geo.svg"
              className="homesvg"
              alt="roadmap"
            />
          </router-link>
          <p>roadmap</p>
        </div>
        <div className="menu-icon">
          <router-link to="/privacy">
            <img
              src="../../src/assets/file-earmark-lock.svg"
              className="homesvg"
              alt="privacy"
            />
          </router-link>
          <p>privacy</p>
        </div>
      </div>
      <div className="account-items">
        <img
          src="../../src/assets/caret-down-fill.svg"
          className="downsvg"
          ref="menu"
          @click="openClose"
        />
        <div className="dropdown-menu" v-if="isOpen">
          <div className="dropdown-links">
            <router-link :to="'/' + userId + '/chat'">
              <button className="dropdown-button-top">Chat</button>
            </router-link>
            <div className="dropdown-bar"></div>
            <router-link :to="'/' + userId + '/account'">
              <button className="dropdown-button">Account</button>
            </router-link>
            <div className="dropdown-bar"></div>
            <div v-if="session">
              <button className="dropdown-button" @click="onLogout">
                Logout
              </button>
            </div>
            <div v-else>
              <router-link to="/auth">
                <button className="dropdown-button">Login</button>
              </router-link>
            </div>
            <div className="dropdown-bar"></div>
            <div className="dropdown-bottom"></div>
          </div>
        </div>
        <img
          className="user-icon"
          src="../../src/assets/user.png"
          ref="menu"
          @click="openClose"
        />
        <div v-if="session">
          <button className="authButton-login" @click="onLogout">Logout</button>
        </div>
        <div v-else>
          <button className="authButton-signup" @click="redirectToLogin">
            Sign up
          </button>
          <button className="authButton-login" @click="redirectToLogin">
            Login
          </button>
        </div>
        <div className="menu-icon">
          <router-link to="/support">
            <img
              src="../../src/assets/question-square.svg"
              className="homesvg"
              alt="support"
            />
          </router-link>
          <p>support</p>
        </div>
      </div>
    </div>
    <div className="navbarbar"></div>
  </div>
</template>
