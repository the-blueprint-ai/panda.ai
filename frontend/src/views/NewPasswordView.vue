<script>
import { defineComponent } from "vue";
import { submitNewPassword } from "supertokens-web-js/recipe/thirdpartyemailpassword";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import SpinnerComponent from "../components/spinnerComponent.vue";

export default defineComponent({
  data() {
    return {
      password: "",
      passwordOk: "",
      badPasswordError: "",
      sendButtonText: "RESET PASSWORD",
    };
  },
  watch: {
    password() {
      if (this.isPasswordValid == true) {
        this.passwordOk = "ok";
        this.badPasswordError = "";
      } else {
        this.passwordOk = "no";
        this.badPasswordError =
          "Your password must be at least 8 characters long and include one lowercase, one uppercase and a number.";
      }
    },
  },
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
    newPasswordEntered: async function (newPassword) {
      try {
        let response = await submitNewPassword({
          formFields: [
            {
              id: "password",
              value: newPassword,
            },
          ],
        });

        if (response.status === "FIELD_ERROR") {
          response.formFields.forEach((formField) => {
            if (formField.id === "password") {
              // New password did not meet password criteria on the backend.
              window.alert(formField.error);
            }
          });
        } else if (response.status === "RESET_PASSWORD_INVALID_TOKEN_ERROR") {
          // the password reset token in the URL is invalid, expired, or already consumed
          window.alert("Password reset failed. Please try again");
          this.$router.push("signin"); // back to the login screen.
        } else {
          window.alert("Password reset successful!");
          this.$router.push("signin"); // back to the login screen.
        }
      } catch (err) {
        if (err.isSuperTokensGeneralError === true) {
          // this may be a custom error message sent from the API by you.
          window.alert(err.message);
        } else {
          window.alert("Oops! Something went wrong.");
        }
      }
    },
  },
  components: {
    navBar,
    navFooter,
    SpinnerComponent,
  },
});
</script>

<template>
  <main style="height: 71vh">
    <navBar></navBar>
    <div class="container-fluid h-100 bg-primary text-white">
      <div class="container d-flex justify-content-center pt-5 pb-5">
        <div class="card text-bg-light text-center mb-3" style="width: 32rem">
          <div class="card-header pt-3 pb-3">
            <img
              src="../assets/panda.png"
              class="w-20 h-20"
              alt="panda"
              width="50"
            />
            <h2 class="pt-3">CHOOSE A NEW PASSWORD</h2>
          </div>
          <div class="card-body pt-4 pb-4 px-5">
            <p>Please enter a new password below:</p>
            <div class="form-floating mb-3">
              <input
                type="password"
                ref="password"
                v-model="this.email"
                class="form-control"
                id="floatingInput"
                placeholder="sKad00sh"
                autocomplete="password"
                @keyup.enter="sendEmailClicked(this.email)"
              />
              <label for="floatingInput">Password</label>
            </div>
            <div class="form-floating mb-3">
              <input
                type="password"
                ref="confirmPassword"
                v-model="this.email"
                class="form-control"
                id="floatingInput"
                placeholder="sKad00sh"
                autocomplete="password"
                @keyup.enter="sendEmailClicked(this.email)"
              />
              <label for="floatingInput">Confirm Password</label>
            </div>
            <div class="pt-4">
              <button
                type="button"
                class="btn btn-secondary btn-lg mb-3 d-inline-flex justify-content-center"
                style="width: 70%"
                @click="newPasswordEntered(this.password)"
              >
                <SpinnerComponent
                  :loading="this.loading"
                  :button-text="this.sendButtonText"
                ></SpinnerComponent>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
