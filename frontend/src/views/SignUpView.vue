<script>
import { defineComponent } from "vue";
import {
  emailPasswordSignUp,
  doesEmailExist,
} from "supertokens-web-js/recipe/thirdpartyemailpassword";
import { emailVerification } from "../composables/emailVerification.js";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import SpinnerComponent from "../components/spinnerComponent.vue";

export default defineComponent({
  data() {
    return {
      email: "",
      password: "",
      isTyping: false,
      emailTimer: null,
      emailExistsError: "",
      emailChecking: true,
      emailOk: "",
      passwordOk: "",
      badPasswordError: "",
      loading: false,
      buttonText: "SIGN UP",
    };
  },
  watch: {
    email(newValue) {
      // Clear the previous timer (if there was one)
      clearTimeout(this.emailTimer);

      // Start a new timer for 1000ms
      this.emailTimer = setTimeout(() => {
        this.checkEmail(newValue);
      }, 400);
    },
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
    isEmailValid() {
      return this.validateEmail(this.email);
    },
    isPasswordValid() {
      return this.validatePassword(this.password);
    },
  },
  methods: {
    emailVerification,
    validateEmail: function (email) {
      var re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
    validatePassword: function (password) {
      const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
      return regex.test(password);
    },
    signUpClicked: async function (store, email, password) {
      this.loading = true;
      try {
        let response = await emailPasswordSignUp({
          formFields: [
            {
              id: "email",
              value: email,
            },
            {
              id: "password",
              value: password,
            },
          ],
        });

        if (response.status === "FIELD_ERROR") {
          // one of the input formFields failed validaiton
          response.formFields.forEach((formField) => {
            if (formField.id === "email") {
              // Email validation failed (for example incorrect email syntax),
              // or the email is not unique.
              this.loading = false;
              window.alert(formField.error);
            } else if (formField.id === "password") {
              // Password validation failed.
              // Maybe it didn't match the password strength
              this.loading = false;
              window.alert(formField.error);
            }
          });
        } else {
          // sign up successful. The session tokens are automatically handled by
          // the frontend SDK.
          store.commit("userStore/setStoreEmail", email);
          this.emailVerification();
        }
      } catch (err) {
        if (err.isSuperTokensGeneralError === true) {
          // this may be a custom error message sent from the API by you.
          this.loading = false;
          window.alert(err.message);
        } else {
          this.loading = false;
          window.alert("Oops! Something went wrong.");
        }
      }
    },
    checkEmail: async function (email) {
      try {
        let response = await doesEmailExist({
          email,
        });

        if (response.doesExist) {
          this.emailChecking = false;
          this.emailExistsError =
            "Email already in use. Please sign in instead";
          this.emailOk = "no";
          setTimeout(() => {
            this.emailExistsError = "";
            this.emailOk = "";
            this.email = "";
            this.$refs.email.value = null;
            this.emailChecking = true;
          }, 3000);
        } else {
          this.emailChecking = false;
          setTimeout(() => {
            this.emailOk = "ok";
          }, 3000);
        }
      } catch (err) {
        console.error(err); // log the error to the console
        if (err.isSuperTokensGeneralError === true) {
          // this may be a custom error message sent from the API by you.
          window.alert(err.message);
        } else {
          window.alert("Oops! Something went wrong.");
        }
      }
    },
    toSignIn() {
      this.$router.push("/signin");
    },
    toToS() {
      this.$router.push("/terms-of-service");
    },
    toPP() {
      this.$router.push("/privacy-policy");
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
  <main>
    <navBar></navBar>
    <div class="bodyG">
      <div class="signInContainer">
        <div class="signInContainerTitle">
          <img src="../assets/panda.png" />
          <h2>SIGN UP</h2>
          <h3>ALREADY HAVE AN ACCOUNT?</h3>
          <p @click="toSignIn()">SIGN IN</p>
        </div>
        <div class="signInBar"></div>
        <div class="emailPassword">
          <h2>Email</h2>
          <img
            v-if="isEmailValid && emailOk === 'ok' && email"
            id="emailGood"
            src="../assets/icons/envelope-check-fill.svg"
          />
          <img
            v-if="emailOk === 'no'"
            id="emailBad"
            src="../assets/icons/envelope-exclamation-fill.svg"
          />
          <input
            ref="email"
            v-model="email"
            @input="isTyping = true"
            type="email"
            placeholder="kung-fu@panda.ai"
          />
          <h6 v-if="email && emailChecking" style="color: white">
            CHECKING...
          </h6>
          <h6 v-if="emailExistsError">{{ emailExistsError }}</h6>
          <h2>Password</h2>
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
            ref="password"
            v-model="password"
            type="password"
            placeholder="sKad00sh"
            @keyup.enter="signUpClicked(this.$store, this.email, this.password)"
          />
          <h6 v-if="badPasswordError">{{ badPasswordError }}</h6>
          <button
            v-if="
              isEmailValid &&
              emailOk === 'ok' &&
              email &&
              isPasswordValid &&
              passwordOk === 'ok' &&
              password
            "
            @click="signUpClicked(this.$store, this.email, this.password)"
          >
            <SpinnerComponent :loading="this.loading" :button-text=this.buttonText></SpinnerComponent>
          </button>
          <button
            v-else
            style="
              background-color: #c8c8c8;
              border: 5px solid #c8c8c8;
              cursor: default;
            "
          >
            <SpinnerComponent :loading="this.loading" :button-text=this.buttonText></SpinnerComponent>
          </button>
          <h4>BY CONTINUING YOU AGREE TO OUR:</h4>
          <h5 @click="toToS()">TERMS OF SERVICE</h5>
          <h5 @click="toPP()">PRIVACY POLICY</h5>
        </div>
        <div class="signInBar"></div>
        <div class="signInOption"><p>OR</p></div>
        <div class="thirdPartySignIn">
          <div class="thirdPartyButton">
            <img src="../assets/icons/github.svg" />Continue With GitHub
          </div>
          <div class="thirdPartyButton">
            <img src="../assets/icons/google.svg" />Continue With Google
          </div>
          <div class="thirdPartyButton">
            <img src="../assets/icons/apple.svg" />Continue With Apple
          </div>
          <div class="thirdPartyButton">
            <img src="../assets/icons/facebook.svg" />Continue With Facebook
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
@import "../assets/styles/panda-main.css";
</style>
