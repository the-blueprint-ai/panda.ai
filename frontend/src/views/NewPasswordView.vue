<script>
import { defineComponent } from "vue";
import { submitNewPassword } from "supertokens-web-js/recipe/thirdpartyemailpassword";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {
      password: "",
      passwordOk: "",
      badPasswordError: "",
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
          window.location.assign("/signin"); // back to the login screen.
        } else {
          window.alert("Password reset successful!");
          window.location.assign("/signin");
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
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div class="bodyG">
      <div class="emailSentContainer">
        <img id="emailSentPanda" src="../assets/panda.png" />
        <h2>CHOOSE A NEW PASSWORD</h2>
        <img
          id="emailSentEnvelope"
          src="../assets/icons/envelope-paper-heart-fill.svg"
        />
        <div class="signInBar"></div>
        <p>Please enter a new password below:</p>
        <div class="emailPassword">
          <img
            v-if="isPasswordValid && passwordOk === 'ok' && password"
            id="passwordGood"
            src="../assets/icons/shield-fill-check.svg"
          />
          <img
            v-if="passwordOk === 'no'"
            id="passwordBad"
            src="../assets/icons/shield-fill-exclamation.svg"
          />
          <input
            ref="email"
            v-model="this.password"
            type="password"
            placeholder="sKad00sh"
            @keyup.enter="newPasswordEntered(this.password)"
          />
          <h6 v-if="badPasswordError">{{ badPasswordError }}</h6>
          <button
            v-if="!badPasswordError"
            @click="newPasswordEntered(this.password)"
          >
            RESET PASSWORD
          </button>
          <button
            v-else
            style="
              background-color: #c8c8c8;
              border: 5px solid #c8c8c8;
              cursor: default;
            "
          >
            RESET PASSWORD
          </button>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style>
@import "../assets/styles/panda-main.css";
</style>
