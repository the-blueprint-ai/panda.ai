<script>
import { deleteUser } from "../composables/deleteUser.js";
import SpinnerComponent from "../components/spinnerComponent.vue";
import { useToast } from "vue-toastification";

export default {
  data() {
    return {
      loading: false,
      buttonText: "CHANGE PASSWORD",
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
      this.$router.push("/");
    },
    async changePassword(userId, email, oldPassword, newPassword) {
      const toast = useToast();
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
          toast.warning("Password updated unsuccessful. Please try again.");
        }
        this.loading = false;
        toast.success(
          "Password updated successfully. Please sign in again with your new password."
        );
        this.$router.push("/signin/");
      } catch (error) {
        // Handle the error
        console.error("An error occurred while saving the file:", error);
      }
    },
  },
  components: {
    SpinnerComponent,
  },
};
</script>

<template>
  <div
    class="userSettings d-flex flex-row flex-wrap justify-content-around text-center"
    v-if="settingsMenu"
  >
    <div class="card mt-4 mx-auto">
      <div class="card-header">
        <h1>🐼</h1>
        <h2>CHANGE PASSWORD</h2>
      </div>
      <div class="card-body">
        <p>
          To change your 🐼 panda.ai password please click the button below.
        </p>
      </div>
      <div class="card-footer">
        <button
          type="button"
          class="btn btn-secondary btn-lg mt-2 mb-2"
          data-bs-toggle="modal"
          data-bs-target="#passwordModal"
        >
          CHANGE PASSWORD
        </button>
      </div>
    </div>
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
              class="btn btn-secondary d-flex justify-content-center"
              data-bs-dismiss="modal"
              style="width: 35%"
            >
              <SpinnerComponent
                :loading="this.loading"
                :button-text="this.buttonText"
              ></SpinnerComponent>
            </button>
            <button
              v-else
              class="btn btn-secondary"
              style="width: 35%"
              disabled
            >
              CHANGE PASSWORD
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="card mt-4 mx-auto">
      <div class="card-header">
        <h1>🐼</h1>
        <h2>DELETE ACCOUNT</h2>
      </div>
      <div class="card-body">
        <p>To delete your 🐼 panda.ai account please click the button below.</p>
      </div>
      <div class="card-footer">
        <button
          type="button"
          class="btn btn-secondary btn-lg mt-2 mb-2"
          data-bs-toggle="modal"
          data-bs-target="#deleteModal"
        >
          DELETE ACCOUNT
        </button>
      </div>
    </div>
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
            <p class="mb-4">We're very sad to see you leave us 😭.</p>
            <p class="mb-4 text-danger">
              PLEASE NOTE: Deleting your account will delete all your data from
              our systems and cancel your subscription. The data will not be
              recoverable if you change your mind and 🐼 panda.ai will no longer
              remember anything about you 😭.
            </p>
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
              <label for="floatingInput">Enter email...</label>
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
