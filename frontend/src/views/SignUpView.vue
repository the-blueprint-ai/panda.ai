<script>
import { defineComponent } from "vue";
import {
  emailPasswordSignUp,
  doesEmailExist,
} from "supertokens-web-js/recipe/thirdpartyemailpassword";
import * as Session from "supertokens-web-js/recipe/session";
import { mapActions } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {
      email: "",
      password: "",
      isTyping: false,
      emailTimer: null,
      emailExistsError: "",
    };
  },
  watch: {
    email(newValue) {
      // Clear the previous timer (if there was one)
      clearTimeout(this.emailTimer);

      // Start a new timer for 1000ms
      this.emailTimer = setTimeout(() => {
        this.checkEmail(newValue);
      }, 800);
    },
  },
  methods: {
    ...mapActions(["getSession", "getUserInfo"]),
    signUpClicked: async function (email, password) {
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
              window.alert(formField.error);
            } else if (formField.id === "password") {
              // Password validation failed.
              // Maybe it didn't match the password strength
              window.alert(formField.error);
            }
          });
        } else {
          // sign up successful. The session tokens are automatically handled by
          // the frontend SDK.
          await this.getSession();
          let userId = await Session.getUserId();
          window.location.href = userId + "/onboarding";
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
    checkEmail: async function (email) {
      try {
        let response = await doesEmailExist({
          email,
        });

        if (response.doesExist) {
          this.emailExistsError =
            "Email already exists. Please sign in instead";
          setTimeout(() => {
            this.emailExistsError = "";
          }, 4000);
          setTimeout(() => {
            this.email = "";
          }, 3000);
          setTimeout(() => {
            this.$refs.email.value = null;
          }, 10);
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
          <input
            ref="email"
            v-model="this.email"
            @input="isTyping = true"
            type="text"
            placeholder="kung-fu@panda.ai"
          />
          <h6 v-if="emailExistsError">{{ emailExistsError }}</h6>
          <h2>Password</h2>
          <input ref="password" v-model="this.password" type="text" placeholder="sKad00sh" />
          <button @click="signUpClicked(this.email, this.password)">
            SIGN UP
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
