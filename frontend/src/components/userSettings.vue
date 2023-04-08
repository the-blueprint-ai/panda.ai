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
      window.location.href = ("http://localhost:3000/");
    },
  },
  components: {
    LoadingOverlay,
  },
};
</script>

<template>
  <div class="userSettings" v-if="settingsMenu">
    <LoadingOverlay v-if="this.loading" :loading="this.loading"></LoadingOverlay>
    <h1>🐼</h1>
    <h2>CHANGE PASSWORD</h2>
    <p>To change your 🐼 panda.ai password please click the button below:</p>
    <button class="chatButton" @click="activatePasswordOverlay">CHANGE PASSWORD</button>
    <div id="passwordOverlay" class="overlay" :class="{ active: passwordOverlay }">
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
            To change your password, please enter your current password and your new password below:
          </p>
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
          />
          <input
            class="changePassword"
            id="newPassword"
            v-model="newPassword"
            placeholder="new password"
            type="password"
            name="password"
          />
          <input
            class="changePassword"
            id="confirmNewPassword"
            v-model="confirmNewPassword"
            placeholder="confirm new password"
            type="password"
            name="password"
          />
          <button v-if="this.currentPassword === this.newPassword === this.confirmNewPassword" class="chatButton" @click="changePassword(this.userId)">CHANGE PASSWORD</button>
          <button v-else class="chatButton" disabled>CHANGE PASSWORD</button>
        </div>
      </div>
    </div>
    <span class="spacer"></span>
    <h2>DELETE ACCOUNT</h2>
    <p>To delete your 🐼 panda.ai account please click the button below:</p>
    <button class="chatButton" @click="activateDeleteOverlay">DELETE ACCOUNT</button>
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
            id="email"
            v-model="confirmedEmail"
            :placeholder="email"
            type="email"
            name="email"
          />
          <button v-if="this.email === this.confirmedEmail" class="chatButton" @click="deleteAccount(this.userId)">CONFIRM DELETION</button>
          <button v-else class="chatButton" disabled>CONFIRM DELETION</button>
        </div>
      </div>
    </div>
  </div>
</template>
