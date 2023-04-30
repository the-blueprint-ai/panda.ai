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
      this.$router.push("/auth/" + this.userId + "/chat");
    },
    async onLogout() {
      await Session.signOut();
      window.location.href = "https://www.mypanda.ai/";
    },
    // toggleMenu() {
    //   const menu = this.$refs.hamburgerMenu;

    //   if (!menu.style.left || menu.style.left === "-120%") {
    //     menu.style.left = "0";
    //   } else {
    //     menu.style.left = "-120%";
    //   }
    // },
    // openClose(event) {
    //   // Update the openClose method to take the event object as a parameter
    //   var _this = this;

    //   const closeListener = (e) => {
    //     if (
    //       _this.catchOutsideClick(e, _this.$refs.avatar) &&
    //       _this.catchOutsideClick(e, _this.$refs.caret)
    //     )
    //       window.removeEventListener("click", closeListener),
    //         _this.setIsOpenValue(false);
    //   };

    //   window.addEventListener("click", closeListener);

    //   this.setIsOpenValue(!this.isOpen);
    // },
    // catchOutsideClick(event, dropdown) {
    //   if (!dropdown) return false; // Add this line to check if dropdown is null

    //   // When user clicks menu or a child of the menu — do nothing
    //   if (dropdown == event.target || dropdown.contains(event.target))
    //     return false;

    //   // When user clicks outside of the menu — close the menu
    //   if (this.isOpen && dropdown != event.target) return true;
    // },
  },
};
</script>

<template>
  <div class="row">
    <div class="navbar navbar-expand-lg bg-white pt-2 pb-2">
      <div class="col-sm-1 px-5">
        <a class="navbar-brand" @click="redirectToHome">
          <img class="logo" src="../../src/assets/panda.png" width="50" />
          panda.ai
        </a>
      </div>
      <div class="col-sm-9">
        <div class="container-fluid">
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <div class="col px-3">
                <li class="nav-item pt-2">
                  <img src="../../src/assets/icons/house-door.svg" alt="home" />
                  <a class="nav-link" @click="redirectToHome">home</a>
                </li>
              </div>
              <div class="col px-3">
                <li class="nav-item pt-2">
                  <img
                    src="../../src/assets/icons/file-person.svg"
                    alt="about"
                  />
                  <a class="nav-link" @click="redirectToAbout">about</a>
                </li>
              </div>
              <div class="col px-3">
                <li class="nav-item pt-2">
                  <img src="../../src/assets/icons/tag.svg" alt="about" />
                  <a class="nav-link" @click="redirectToPricing">pricing</a>
                </li>
              </div>
              <div class="col px-3">
                <li class="nav-item pt-2">
                  <img src="../../src/assets/icons/geo.svg" alt="roadmap" />
                  <a class="nav-link" @click="redirectToRoadmap">roadmap</a>
                </li>
              </div>
              <div class="col px-3">
                <li class="nav-item pt-2">
                  <img
                    src="../../src/assets/icons/file-earmark-lock.svg"
                    alt="privacy"
                  />
                  <a class="nav-link" @click="redirectToPrivacy">privacy</a>
                </li>
              </div>
            </ul>
          </div>
        </div>
      </div>
      <div class="col-sm-2 d-flex justify-content-end">
        <ul class="navbar-nav">
          <li v-if="userId" class="nav-item pt-2">
            <img
              src="../../src/assets/icons/question-square.svg"
              alt="support"
            />
            <a class="nav-link" @click="redirectToSupport">support</a>
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
          <li v-if="userId" class="dropdown px-3 ps-4 pe-4">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <img v-bind:src="avatar" class="rounded" ref="avatar" width="60"/>
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" @click="redirectToChat">Chat</a></li>
              <li>
                <a class="dropdown-item" @click="redirectToAccount">Account</a>
              </li>
              <li><hr v-if="admin" class="dropdown-divider" /></li>
              <li>
                <a v-if="admin" class="dropdown-item" @click="redirectToAdmin"
                  >Admin Panel</a
                >
              </li>
              <li>
                <a v-if="admin" class="dropdown-item" @click="redirectToUserDashboard"
                  >User Dashboard</a
                >
              </li>
              <li><hr class="dropdown-divider" /></li>
              <li>
                <a class="dropdown-item" @click="onLogout">Sign Out</a>
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
  width: 80px;
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
