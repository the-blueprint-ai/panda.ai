<script>
import { defineComponent } from "vue";
import { emailPasswordSignIn } from "supertokens-web-js/recipe/thirdpartyemailpassword";
import * as Session from "supertokens-web-js/recipe/session";
import { mapActions } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    signInClicked: async function (email, password) {
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
              // Email validation failed (for example incorrect email syntax).
              window.alert(formField.error);
            }
          });
        } else if (response.status === "WRONG_CREDENTIALS_ERROR") {
          window.alert("Email password combination is incorrect.");
        } else {
          await this.getSession;
          let userId = await Session.getUserId();
          this.$router.push("/auth/" + userId + "/chat");
          // window.location.href = "/auth/" + userId + "/chat";
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
          <h3>NOT REGISTERED YET?</h3>
          <p @click="toSignUp()">SIGN UP</p>
        </div>
        <div class="signInBar"></div>
        <div class="emailPassword">
          <h2>Email</h2>
          <input ref="email" v-model="this.email" type="email" placeholder="kung-fu@panda.ai" />
          <h2>Password</h2>
          <input ref="password" v-model="this.password" type="password" placeholder="sKad00sh" @keyup.enter="signInClicked(this.email, this.password)" />
          <button @click="signInClicked(this.email, this.password)">SIGN IN</button>
          <h3 @click="toForgotPassword()">FORGOT PASSWORD?</h3>
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
