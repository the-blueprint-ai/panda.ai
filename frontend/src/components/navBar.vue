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
      <div class="col-sm-1 px-5" style="width: 200px">
        <a class="navbar-brand" @click="redirectToHome">
          <img class="logo" src="../../src/assets/panda.png" width="50" />
          panda.ai
        </a>
      </div>
      <div class="col-sm-9 d-flex flex-shrink-1 me-auto">
        <div class="container-fluid">
          <div class="collapse navbar-collapse" id="navbarNav">
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
      <div class="col-sm-2 d-flex justify-content-end">
        <ul class="navbar-nav">
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
            >
              SIGN UP
            </button>
          </li>
          <li v-if="!userId" class="d-flex align-items-center px-2 pe-5">
            <button
              type="button"
              class="btn btn-outline-primary"
              @click="redirectToSignIn"
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
              <img v-bind:src="avatar" class="rounded" ref="avatar" width="60"/>
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
                <a v-if="admin" class="dropdown-item" @click="redirectToUserDashboard"
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
  background-color: #FFCB4C;
  border-radius: 10px;
}
a:hover {
  cursor: pointer;
}
</style>
