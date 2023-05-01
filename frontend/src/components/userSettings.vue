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
  watch: {
    newPassword() {
      if (this.isPasswordValid == true) {
        this.passwordOk = "ok";
        this.badPasswordError = "";
      } else {
        this.passwordOk = "no";
        this.badPasswordError =
          "Your password must be at least 8 characters long and include one lowercase, one uppercase and a number.";
      }
    },
    confirmNewPassword() {
      if (this.confirmNewPassword == this.newPassword) {
        this.passwordOk = "ok";
        this.badPasswordError = "";
      } else {
        this.passwordOk = "no";
        this.badPasswordError =
          "Your confirmed password must match your new password.";
      }
    },
  },
  props: {
    settingsMenu: Boolean,
    userId: String,
    email: String,
  },
  created() {},
  computed: {
    isPasswordValid() {
      return this.validatePassword(this.password);
    },
  },
  methods: {
    validatePassword: function (password) {
      const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
      return regex.test(password);
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
    <LoadingOverlay
      v-if="this.loading"
      :loading="this.loading"
      :spinner-size="80"
    ></LoadingOverlay>
    <h1>🐼</h1>
    <h2>CHANGE PASSWORD</h2>
    <p>To change your 🐼 panda.ai password please click the button below:</p>
    <button
      type="button"
      class="btn btn-secondary btn-lg mt-1 mb-5"
      data-bs-toggle="modal"
      data-bs-target="#passwordModal"
    >
      CHANGE PASSWORD
    </button>
    <div
      class="modal fade"
      id="passwordModal"
      tabindex="-1"
      aria-labelledby="passwordModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title" id="passwordModalLabel">CHANGE PASSWORD</h4>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body text-center">
            <h1>🐼</h1>
            <p>
              To change your password, please enter your current password and
              your new password below:
            </p>
            <div class="form-floating mb-2">
              <input
                type="password"
                name="password"
                class="form-control mt-4"
                id="currentPassword"
                v-model="currentPassword"
                autocomplete="password"
                placeholder="current password"
              />
              <label for="floatingInput">current password</label>
            </div>
            <div class="form-floating mb-2">
              <input
                type="password"
                name="password"
                class="form-control mt-2"
                id="newPassword"
                v-model="newPassword"
                autocomplete="password"
                placeholder="new password"
              />
              <label for="floatingInput">new password</label>
            </div>
            <div class="form-floating mb-3">
              <input
                type="password"
                name="password"
                class="form-control mt-2"
                id="confirmNewPassword"
                v-model="confirmNewPassword"
                autocomplete="password"
                placeholder="confirm new password"
                @keyup.enter="
                  changePassword(
                    this.userId,
                    this.email,
                    this.currentPassword,
                    this.newPassword
                  )
                "
              />
              <label for="floatingInput">confirm new password</label>
              <div id="passwordHelpBlock" class="form-text">
                Your new password must be at least 8 characters long and include
                one lowercase, one uppercase and a number.
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              v-if="
                this.newPassword.length > 0 &&
                this.newPassword === this.confirmNewPassword
              "
              @click="
                changePassword(
                  this.userId,
                  this.email,
                  this.currentPassword,
                  this.newPassword
                )
              "
              type="button"
              class="btn btn-secondary"
            >
              CHANGE PASSWORD
            </button>
            <button v-else class="btn btn-secondary" disabled>
              CHANGE PASSWORD
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- 
        <div class="overlayForm">
          <form>
            <img
              v-if="this.email == this.confirmedEmail"
              id="emailDeleteGood"
              src="../assets/icons/envelope-check-fill.svg"
            />
          </form>
    </div> -->
    <span class="spacer"></span>
    <h2>DELETE ACCOUNT</h2>
    <p>To delete your 🐼 panda.ai account please click the button below:</p>
    <button
      type="button"
      class="btn btn-secondary btn-lg mt-1"
      data-bs-toggle="modal"
      data-bs-target="#deleteModal"
    >
      DELETE ACCOUNT
    </button>

    <div
      class="modal fade"
      id="deleteModal"
      tabindex="-1"
      aria-labelledby="deleteModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title" id="deleteModalLabel">DELETE ACCOUNT</h4>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body text-center">
            <h1>🐼</h1>
            <p>We're very sad to see you leave us 😭.</p>
            <p>
              To confirm deletion of your 🐼 panda.ai account please re-enter
              your email address below and click confirm deletion.
            </p>
            <div class="form-floating mb-3">
              <input
                type="email"
                name="email"
                class="form-control mt-4"
                id="emailDelete"
                v-model="confirmedEmail"
                :placeholder="email"
                autocomplete="email"
              />
              <label for="floatingInput">{{ email }}</label>
            </div>
          </div>
          <div class="modal-footer">
            <button
              v-if="this.email === this.confirmedEmail"
              type="button"
              class="btn btn-secondary"
              @click="deleteAccount(this.userId)"
            >
              CONFIRM DELETION
            </button>
            <button v-else class="btn btn-secondary" disabled>
              CONFIRM DELETION
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.userSettings {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
}
</style>
