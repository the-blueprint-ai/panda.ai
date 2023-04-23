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
    redirectToAccount() {
      this.$router.push("/auth/" + this.userId + "/account");
    },
    redirectToChat() {
      this.$router.push("/auth/" + this.userId + "/chat");
    },
    async onLogout() {
      await Session.signOut();
      window.location.href = "https://www.mypanda.ai/";
    },
    onTouchStart(event) {
      this.startX = event.touches[0].clientX;
      this.startY = event.touches[0].clientY;
    },

    onTouchMove(event) {
      this.endX = event.touches[0].clientX;
      this.endY = event.touches[0].clientY;
    },

    onTouchEnd() {
      const deltaX = this.endX - this.startX;
      const deltaY = this.endY - this.startY;

      if (Math.abs(deltaX) > Math.abs(deltaY) && deltaX > 0 && this.startX < 20) {
        this.toggleMenu();
      }
    },
    toggleMenu() {
      const menu = this.$refs.hamburgerMenu;

      if (!menu.style.left || menu.style.left === "-100%") {
        menu.style.left = "0";
      } else {
        menu.style.left = "-100%";
      }
    },
    openClose(event) {
      // Update the openClose method to take the event object as a parameter
      var _this = this;

      const closeListener = (e) => {
        if (
          _this.catchOutsideClick(e, _this.$refs.avatar) &&
          _this.catchOutsideClick(e, _this.$refs.caret)
        )
          window.removeEventListener("click", closeListener),
            _this.setIsOpenValue(false);
      };

      window.addEventListener("click", closeListener);

      this.setIsOpenValue(!this.isOpen);
    },
    catchOutsideClick(event, dropdown) {
      if (!dropdown) return false; // Add this line to check if dropdown is null

      // When user clicks menu or a child of the menu — do nothing
      if (dropdown == event.target || dropdown.contains(event.target))
        return false;

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
  <div
    class="navbar"
    @touchstart="onTouchStart"
    @touchmove="onTouchMove"
    @touchend="onTouchEnd"
  >
    <div class="navbar-top">
      <div class="mobileMenu">
        <img
          class="hamburgerMenuIcon"
          @click="toggleMenu"
          src="../../src/assets/icons/list.svg"
          width="50"
        />
        <nav class="hamburgerMenu" ref="hamburgerMenu">
          <img
            src="../assets/icons/x.svg"
            class="mobileMenuCloseButton"
            @click="toggleMenu"
          />
          <div class="mobileMenuTop">
            <div class="mobileMenuAvatar" v-if="onboarded">
              <img
                class="mobileMenuUserIcon"
                v-bind:src="avatar"
                ref="avatar"
                @click="redirectToAccount"
              />
              <button class="mobileMenuChatButton" @click="redirectToChat">
                Let's Chat
              </button>
            </div>
            <div v-else>
              <div class="mobileMenuButtons">
                <button
                  class="mobileMenuButtonSignUp"
                  @click="redirectToSignUp"
                >
                  Sign up
                </button>
                <button class="mobileMenuButtonLogin" @click="redirectToSignIn">
                  Sign In
                </button>
              </div>
            </div>
            <div class="mobileMenuList">
              <router-link to="/">
                <div class="mobileMenuIconTop">
                  <img
                    src="../../src/assets/icons/house-door.svg"
                    class="homesvg"
                    alt="home"
                  />
                  <p>HOME</p>
                </div>
              </router-link>
              <router-link to="/about">
                <div class="mobileMenuIcon">
                  <img
                    src="../../src/assets/icons/file-person.svg"
                    class="homesvg"
                    alt="about"
                  />
                  <p>ABOUT</p>
                </div>
              </router-link>
              <router-link to="/roadmap">
                <div class="mobileMenuIcon">
                  <img
                    src="../../src/assets/icons/geo.svg"
                    class="homesvg"
                    alt="roadmap"
                  />
                  <p>ROADMAP</p>
                </div>
              </router-link>
              <router-link to="/privacy">
                <div class="mobileMenuIcon">
                  <img
                    src="../../src/assets/icons/file-earmark-lock.svg"
                    class="homesvg"
                    alt="privacy"
                  />
                  <p>PRIVACY</p>
                </div>
              </router-link>
              <router-link to="/support">
                <div class="mobileMenuIcon">
                  <img
                    src="../../src/assets/icons/question-square.svg"
                    class="homesvg"
                    alt="support"
                  />
                  <p>SUPPORT</p>
                </div>
              </router-link>
              <router-link to="/terms-of-service">
                <div class="mobileMenuIcon">
                  <img
                    src="../../src/assets/icons/emoji-smile.svg"
                    class="homesvg"
                    alt="support"
                  />
                  <p>TERMS OF SERVICE</p>
                </div>
              </router-link>
              <router-link to="/privacy-policy">
                <div class="mobileMenuIconBottom">
                  <img
                    src="../../src/assets/icons/file-earmark-lock.svg"
                    class="homesvg"
                    alt="support"
                  />
                  <p>PRIVACY POLICY</p>
                </div>
              </router-link>
            </div>
          </div>
          <div class="mobileMenuBottom">
            <button
              v-if="onboarded"
              class="mobileMenuChatButton"
              @click="onLogout"
            >
              Sign Out
            </button>
            <div class="mobileMenuBrandHolderBottom">
              <img class="logo" src="../../src/assets/panda.png" width="50" />
              <div class="mobileMenuBrandHolderBottomBrandText">
                <h2>panda.ai</h2>
                <p>MADE WITH ❤️</p>
              </div>
            </div>
          </div>
        </nav>
      </div>
      <div class="brandHolderTop">
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
        <div @click="openClose">
          <img
            v-if="onboarded"
            src="../../src/assets/icons/caret-down-fill.svg"
            class="downsvg"
            ref="caret"
          />
        </div>
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
          ref="avatar"
          @click="openClose"
        />
        <div v-else>
          <!-- <button class="authButton-signup" @click="redirectToSignUp">
            Sign up
          </button> -->
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
