<script>
import { defineComponent } from "vue";
import { emailPasswordSignIn } from "supertokens-web-js/recipe/thirdpartyemailpassword";
import * as Session from "supertokens-web-js/recipe/session";
import { mapActions } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import SpinnerComponent from "../components/spinnerComponent.vue";

export default defineComponent({
  data() {
    return {
      email: "",
      password: "",
      loading: false,
      buttonText: "SIGN IN",
    };
  },
  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    signInClicked: async function (email, password) {
      this.loading = true;
      try {
        let response = await emailPasswordSignIn({
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
          response.formFields.forEach((formField) => {
            if (formField.id === "email") {
              this.loading = false;
              // Email validation failed (for example incorrect email syntax).
              window.alert(formField.error);
            }
          });
        } else if (response.status === "WRONG_CREDENTIALS_ERROR") {
          this.loading = false;
          window.alert("Email password combination is incorrect.");
        } else {
          await this.getSession;
          let userId = await Session.getUserId();
          if (userId) {
            this.loading = false;
            this.$router.push("/auth/" + userId + "/chat");
          }
        }
      } catch (err) {
        if (err.isSuperTokensGeneralError === true) {
          this.loading = false;
          // this may be a custom error message sent from the API by you.
          window.alert(err.message);
        } else {
          this.loading = false;
          window.alert("Oops! Something went wrong.");
        }
      }
    },
    toSignUp() {
      this.$router.push("/signup");
    },
    toForgotPassword() {
      this.$router.push("/password-reset");
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
          <h2>SIGN IN</h2>
          <!-- <h3>NOT REGISTERED YET?</h3>
          <p @click="toSignUp()">SIGN UP</p> -->
        </div>
        <div class="signInBar"></div>
        <div class="emailPassword">
          <h2>Email</h2>
          <form>
            <input
              ref="email"
              v-model="this.email"
              type="email"
              placeholder="kung-fu@panda.ai"
              autocomplete="email"
            />
          </form>
          <h2>Password</h2>
          <form @submit.prevent="signInClicked(this.email, this.password)">
            <input
              ref="password"
              v-model="this.password"
              type="password"
              placeholder="sKad00sh"
              @keyup.enter="signInClicked(this.email, this.password)"
              autocomplete="password"
            />
          </form>
          <button class="signInButton" @click="signInClicked(this.email, this.password)">
            <SpinnerComponent
              :loading="this.loading"
              :button-text="this.buttonText"
            ></SpinnerComponent>
          </button>
          <h3 @click="toForgotPassword()">FORGOT PASSWORD?</h3>
        </div>
        <!-- <div class="signInBar"></div>
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
        </div> -->
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
