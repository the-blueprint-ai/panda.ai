<script>
import { deleteUser } from "../composables/deleteUser.js";
import LoadingOverlay from "../components/loadingOverlay.vue";

export default {
  data() {
    return {
      loading: false,
      passwordOverlay: false,
      deleteOverlay: false,
      currentPassword: "",
      newPassword: "",
      confirmNewPassword: "",
      confirmedEmail: "",
    };
  },
  watch: {},
  props: {
    settingsMenu: Boolean,
    userId: String,
    email: String,
  },
  created() {},
  methods: {
    activatePasswordOverlay() {
      this.passwordOverlay = !this.passwordOverlay;
    },
    activateDeleteOverlay() {
      this.deleteOverlay = !this.deleteOverlay;
    },
    async deleteAccount(userId) {
      this.deleteOverlay = false;
      this.loading = true;
      await deleteUser(userId);
      window.location.href = "http://localhost:3000/";
    },
    async changePassword(userId, email, oldPassword, newPassword) {
      this.passwordOverlay = false;
      this.loading = true;
      try {
        const url =
          import.meta.env.VITE_APP_API_URL +
          "/users/change-password?user_id=" +
          userId +
          "&email=" +
          email +
          "&oldPassword=" +
          oldPassword +
          "&newPassword=" +
          newPassword;
        const res = await fetch(url, {
          method: "POST",
        });

        // Check if the response status indicates an error
        if (!res.ok) {
          const errorResponse = await res.json();
          console.error("Server error response:", errorResponse);
          window.alert("Password updated unsuccessful. Please try again.");
        }
        this.loading = false;
        window.alert(
          "Password updated successfully. Please sign in again with your new password."
        );
        window.location.href = "http://localhost:3000/signin";
      } catch (error) {
        // Handle the error
        console.error("An error occurred while saving the file:", error);
      }
    },
  },
  components: {
    LoadingOverlay,
  },
};
</script>

<template>
  <div class="userSettings" v-if="settingsMenu">
    <h1 class="accountSectionHeading">SETTINGS</h1>
    <LoadingOverlay
      v-if="this.loading"
      :loading="this.loading"
      :spinner-size="80"
    ></LoadingOverlay>
    <h1>🐼</h1>
    <h2>CHANGE PASSWORD</h2>
    <p>To change your 🐼 panda.ai password please click the button below:</p>
    <button class="chatButton" @click="activatePasswordOverlay">
      CHANGE PASSWORD
    </button>
    <div
      id="passwordOverlay"
      class="overlay"
      :class="{ active: passwordOverlay }"
    >
      <div class="overlayContent">
        <img
          src="../assets/icons/x.svg"
          class="overlayCloseButton"
          @click="activatePasswordOverlay"
        />
        <div class="overlayTitle">
          <h2>CHANGE PASSWORD</h2>
        </div>
        <div class="overlayForm">
          <h1>🐼</h1>
          <p>
            To change your password, please enter your current password and your
            new password below:
          </p>
          <form>
            <img
              v-if="this.email == this.confirmedEmail"
              id="emailDeleteGood"
              src="../assets/icons/envelope-check-fill.svg"
            />
            <input
              class="changePassword"
              id="currentPassword"
              v-model="currentPassword"
              placeholder="current password"
              type="password"
              name="password"
              autocomplete="password"
            />
            <input
              class="changePassword"
              id="newPassword"
              v-model="newPassword"
              placeholder="new password"
              type="password"
              name="password"
              autocomplete="password"
            />
            <input
              class="changePassword"
              @keyup.enter="
                changePassword(
                  this.userId,
                  this.email,
                  this.currentPassword,
                  this.newPassword
                )
              "
              id="confirmNewPassword"
              v-model="confirmNewPassword"
              placeholder="confirm new password"
              type="password"
              name="password"
              autocomplete="password"
            />
          </form>
          <button
            v-if="this.newPassword === this.confirmNewPassword"
            class="chatButton"
            @click="
              changePassword(
                this.userId,
                this.email,
                this.currentPassword,
                this.newPassword
              )
            "
          >
            CHANGE PASSWORD
          </button>
          <button v-else class="chatButton" disabled>CHANGE PASSWORD</button>
        </div>
      </div>
    </div>
    <span class="spacer"></span>
    <h2>DELETE ACCOUNT</h2>
    <p>To delete your 🐼 panda.ai account please click the button below:</p>
    <button class="chatButton" @click="activateDeleteOverlay">
      DELETE ACCOUNT
    </button>
    <div id="deleteOverlay" class="overlay" :class="{ active: deleteOverlay }">
      <div class="overlayContent">
        <img
          src="../assets/icons/x.svg"
          class="overlayCloseButton"
          @click="activateDeleteOverlay"
        />
        <div class="overlayTitle">
          <h2>DELETE ACCOUNT</h2>
        </div>
        <div class="overlayForm">
          <h1>🐼</h1>
          <p>We're very sad to see you leave us 😭.</p>
          <p>
            To confirm deletion of your 🐼 panda.ai account please re-enter your
            email address below and click confirm
          </p>
          <img
            v-if="this.email == this.confirmedEmail"
            id="emailDeleteGood"
            src="../assets/icons/envelope-check-fill.svg"
          />
          <input
            class="emailDelete"
            id="emailDelete"
            v-model="confirmedEmail"
            :placeholder="email"
            type="email"
            name="email"
          />
          <button
            v-if="this.email === this.confirmedEmail"
            class="chatButton"
            @click="deleteAccount(this.userId)"
          >
            CONFIRM DELETION
          </button>
          <button v-else class="chatButton" disabled>CONFIRM DELETION</button>
        </div>
      </div>
    </div>
  </div>
</template>
