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
    redirectToHome() {
      this.$router.push("/");
    },
    redirectToAbout() {
      this.$router.push("/about");
    },
    redirectToPricing() {
      this.$router.push("/pricing");
    },
    redirectToRoadmap() {
      this.$router.push("/roadmap");
    },
    redirectToPrivacy() {
      this.$router.push("/privacy");
    },
    redirectToSupport() {
      this.$router.push("/support");
    },
    redirectToPP() {
      this.$router.push("/privacy-policy");
    },
    redirectToToS() {
      this.$router.push("/terms-of-service");
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
    redirectToAdmin() {
      this.$router.push("/auth/admin/dashboard");
    },
    redirectToUserDashboard() {
      window.open("https://api.mypanda.ai/auth/dashboard", "_blank");
    },
    async onLogout() {
      await Session.signOut();
      window.location.href = "https://www.mypanda.ai/";
    },
  },
};
</script>

<template>
  <div class="row">
    <div class="navbar navbar-expand-lg bg-white pt-2 pb-2">
      <button
        class="navbar-toggler ms-4"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasNavbar"
        aria-controls="offcanvasNavbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        class="offcanvas offcanvas-start"
        tabindex="-1"
        id="offcanvasNavbar"
        aria-labelledby="offcanvasNavbarLabel"
      >
        <div class="offcanvas-header d-flex flex-column">
          <div class="">
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="offcanvas"
              aria-label="Close"
            ></button>
          </div>
          <div v-if="!userId" class="d-flex flex-column align-items-center">
            <img
              src="../../src/assets/panda.png"
              class="img mt-3"
              ref="panda"
              width="200"
              @click="redirectToAccount"
            />
            <router-link :to="'/signin'">
              <button type="button" class="btn btn-secondary btn-lg mt-4">
                LET'S CHAT
              </button>
            </router-link>
          </div>
          <div v-if="userId" class="d-flex flex-column align-items-center">
            <img
              v-bind:src="avatar"
              class="img-thumbnail rounded-circle mt-3"
              ref="avatar"
              width="200"
              @click="redirectToAccount"
            />
            <router-link :to="'/auth/' + userId + '/chat'">
              <button type="button" class="btn btn-secondary btn-lg mt-4">
                LET'S CHAT
              </button>
            </router-link>
          </div>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav flex-grow-1">
            <li><hr class="divider mt-0 mb-0" /></li>
            <li
              class="nav-item w-100 d-flex flex-row align-items-start ps-2 pt-3"
              @click="redirectToHome"
            >
              <img src="../../src/assets/icons/house-door.svg" alt="home" />
              <p class="nav-link text-uppercase ms-4 mb-0">home</p>
            </li>
            <li
              class="nav-item w-100 d-flex flex-row align-items-start ps-2 pt-3"
              @click="redirectToAbout"
            >
              <img src="../../src/assets/icons/file-person.svg" alt="about" />
              <p class="nav-link text-uppercase ms-4 mb-0">about</p>
            </li>
            <li
              class="nav-item w-100 d-flex flex-row align-items-start ps-2 pt-3"
              @click="redirectToPricing"
            >
              <img src="../../src/assets/icons/tag.svg" alt="about" />
              <p class="nav-link text-uppercase ms-4 mb-0">pricing</p>
            </li>
            <li
              class="nav-item w-100 d-flex flex-row align-items-start ps-2 pt-3"
              @click="redirectToRoadmap"
            >
              <img src="../../src/assets/icons/geo.svg" alt="roadmap" />
              <p class="nav-link text-uppercase ms-4 mb-0">roadmap</p>
            </li>
            <li
              class="nav-item w-100 d-flex flex-row align-items-start ps-2 pt-3"
              @click="redirectToPrivacy"
            >
              <img
                src="../../src/assets/icons/file-earmark-lock.svg"
                alt="privacy"
              />
              <p class="nav-link text-uppercase ms-4 mb-0">privacy</p>
            </li>
            <li
              class="nav-item w-100 d-flex flex-row align-items-start ps-2 pt-3"
              @click="redirectToSupport"
            >
              <img
                src="../../src/assets/icons/question-square.svg"
                alt="support"
              />
              <p class="nav-link text-uppercase ms-4">support</p>
            </li>
            <div v-if="admin" class="">
              <li><hr class="divider mt-0 mb-0" /></li>
              <li
                class="nav-item w-100 d-flex flex-row align-items-start ps-2 pt-3"
                @click="redirectToAdmin"
              >
                <img
                  src="../../src/assets/icons/graph-up-arrow.svg"
                  alt="admin"
                />
                <p class="nav-link text-uppercase ms-4 mb-0">ADMIN PANEL</p>
              </li>
              <li
                class="nav-item w-100 d-flex flex-row align-items-start ps-2 pt-3"
                @click="redirectToUserDashboard"
              >
                <img
                  src="../../src/assets/icons/person-circle.svg"
                  alt="user-dashboard"
                />
                <p class="nav-link text-uppercase ms-4">USER DASHBOARD</p>
              </li>
            </div>
            <li><hr class="divider mt-0 mb-0" /></li>
            <li
              class="nav-item w-100 d-flex flex-row align-items-start ps-2 pt-3"
              @click="redirectToToS"
            >
              <img
                src="../../src/assets/icons/emoji-smile.svg"
                alt="user-dashboard"
              />
              <p class="nav-link text-uppercase ms-4 mb-0">TERMS OF SERVICE</p>
            </li>
            <li
              class="nav-item w-100 d-flex flex-row align-items-start ps-2 pt-3"
              @click="redirectToPP"
            >
              <img
                src="../../src/assets/icons/file-earmark-lock.svg"
                alt="user-dashboard"
              />
              <p class="nav-link text-uppercase ms-4">PRIVACY POLICY</p>
            </li>
            <div v-if="!userId" class="d-flex justify-content-center">
              <li><hr class="divider mt-0" /></li>
              <li class="d-flex align-items-center ps-5 px-2">
                <button
                  type="button"
                  class="btn btn-outline-primary"
                  @click="redirectToSignUp"
                  style="width: 100px"
                >
                  SIGN UP
                </button>
              </li>
              <li class="d-flex align-items-center px-2 pe-5">
                <button
                  type="button"
                  class="btn btn-outline-primary"
                  @click="redirectToSignIn"
                  style="width: 100px"
                >
                  SIGN IN
                </button>
              </li>
            </div>
          </ul>
        </div>
        <hr class="divider mt-0 mb-0" />
        <div class="bg-light">
          <div class="row list-unstyled d-flex justify-content-evenly mt-5">
            <li class="nav-item">
              <img
                navigate-to="discord"
                @click="navigate($event)"
                src="../assets/icons/discord.svg"
                width="30"
                height="30"
              />
            </li>
            <li class="nav-item">
              <img
                navigate-to="twitter"
                @click="navigate($event)"
                src="../assets/icons/twitter.svg"
                width="30"
                height="30"
              />
            </li>
            <li class="nav-item">
              <img
                navigate-to="linkedin"
                @click="navigate($event)"
                src="../assets/icons/linkedin.svg"
                width="30"
                height="30"
              />
            </li>
            <li class="nav-item">
              <a :href="'mailto:contact@mypanda.ai?subject=Hello!'">
                <img
                  navigate-to="contact"
                  src="../assets/icons/envelope-at-fill.svg"
                  width="30"
                  height="30"
                />
              </a>
            </li>
          </div>
          <div class="d-flex flex-row mt-5 justify-content-center">
            <img
              class="w25 h25"
              src="../../src/assets/panda.png"
              style="height: 50px; width: 50px"
            />
            <div>
              <h4 class="ms-3 pt-0 lh-1">panda.ai</h4>
              <p class="ms-3 lh-1">MADE WITH ❤️</p>
            </div>
          </div>
          <div class="copywright row mb-5 px-5 pt-3 text-center">
            <h5>©panda.ai 2023</h5>
          </div>
        </div>
      </div>
      <div class="col-sm-1 px-5" style="width: 200px">
        <a class="navbar-brand" @click="redirectToHome">
          <img class="logo" src="../../src/assets/panda.png" width="50" />
          panda.ai
        </a>
      </div>
      <div class="col-sm-9 d-flex flex-shrink-1 me-auto">
        <div class="container-fluid">
          <div class="navbarLinks navbar" id="navbarNav">
            <ul class="navbar-nav">
              <div class="col px-3" @click="redirectToHome">
                <li class="nav-item pt-3">
                  <img src="../../src/assets/icons/house-door.svg" alt="home" />
                  <a class="nav-link">home</a>
                </li>
              </div>
              <div class="col px-3" @click="redirectToAbout">
                <li class="nav-item pt-3">
                  <img
                    src="../../src/assets/icons/file-person.svg"
                    alt="about"
                  />
                  <a class="nav-link">about</a>
                </li>
              </div>
              <div class="col px-3" @click="redirectToPricing">
                <li class="nav-item pt-3">
                  <img src="../../src/assets/icons/tag.svg" alt="about" />
                  <a class="nav-link">pricing</a>
                </li>
              </div>
              <div class="col px-3" @click="redirectToRoadmap">
                <li class="nav-item pt-3">
                  <img src="../../src/assets/icons/geo.svg" alt="roadmap" />
                  <a class="nav-link">roadmap</a>
                </li>
              </div>
              <div class="col px-3" @click="redirectToPrivacy">
                <li class="nav-item pt-3">
                  <img
                    src="../../src/assets/icons/file-earmark-lock.svg"
                    alt="privacy"
                  />
                  <a class="nav-link">privacy</a>
                </li>
              </div>
            </ul>
          </div>
        </div>
      </div>
      <div
        class="navbarEndButtons col-sm-2 d-flex flex-row justify-content-end"
      >
        <ul class="navbar-nav d-flex flex-row">
          <li class="nav-item pt-3" @click="redirectToSupport">
            <img
              src="../../src/assets/icons/question-square.svg"
              alt="support"
            />
            <a class="nav-link">support</a>
          </li>
          <li v-if="!userId" class="d-flex align-items-center ps-5 px-2">
            <button
              type="button"
              class="btn btn-outline-primary"
              @click="redirectToSignUp"
              style="width: 100px"
            >
              SIGN UP
            </button>
          </li>
          <li v-if="!userId" class="d-flex align-items-center px-2 pe-5">
            <button
              type="button"
              class="btn btn-outline-primary"
              @click="redirectToSignIn"
              style="width: 100px"
            >
              SIGN IN
            </button>
          </li>
          <li v-if="userId" class="dropdown px-3 pe-4">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <img
                v-bind:src="avatar"
                class="rounded"
                ref="avatar"
                width="60"
              />
            </a>
            <ul class="dropdown-menu dropdown-menu-lg-end me-4">
              <li><a class="dropdown-item" @click="redirectToChat">CHAT</a></li>
              <li>
                <a class="dropdown-item" @click="redirectToAccount">ACCOUNT</a>
              </li>
              <li><hr v-if="admin" class="dropdown-divider" /></li>
              <li><h6 v-if="admin" class="dropdown-header">ADMIN</h6></li>
              <li>
                <a v-if="admin" class="dropdown-item" @click="redirectToAdmin"
                  >ADMIN PANEL</a
                >
              </li>
              <li>
                <a
                  v-if="admin"
                  class="dropdown-item"
                  @click="redirectToUserDashboard"
                  >USER DASHBOARD</a
                >
              </li>
              <li><hr class="dropdown-divider" /></li>
              <li>
                <a class="dropdown-item" @click="onLogout">SIGN OUT</a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<!-- 
  
    <div class="mobileMenuTop">
      <div class="mobileMenuAvatar" v-if="userId">
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
        <router-link to="/pricing">
          <div class="mobileMenuIcon">
            <img
              src="../../src/assets/icons/tag.svg"
              class="homesvg"
              alt="about"
            />
            <p>PRICING</p>
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
        v-if="userId"
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
</div> -->

<style scoped>
.nav-item {
  width: 3.5vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}
.nav-item img {
  width: 2rem;
}
.nav-item:hover {
  background-color: #ffcb4c;
  border-radius: 10px;
}
a:hover {
  cursor: pointer;
}
@media (min-width: 992px) {
  .navbar-toggler {
    display: none;
  }
  .offcanvas {
    display: none;
  }
}
@media (max-width: 992px) {
  .navbar {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
  }
  .navbarLinks {
    display: none;
  }
  .navbarEndButtons {
    display: none !important;
  }
}
@media (max-width: 576px) {
  .navbar {
    display: flex;
    flex-direction: row;
    justify-content: center;
  }
  .navbarLinks {
    display: none;
  }
}
</style>
