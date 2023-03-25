<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  methods: {
    toSignUp() {
      this.$router.push("/signup");
    },
    toForgotPassword() {
      this.$router.push("/");
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
          <Input></Input>
          <h2>Password</h2>
          <Input></Input>
          <button>SIGN IN</button>
          <h3 @click="toForgotPassword()">FORGOT PASSWORD?</h3>
        </div>
        <div class="signInBar"></div>
        <div class="signInOption"><p>OR</p></div>
        <div class="thirdPartySignIn">
          <div class="thirdPartyButton"><img src="../assets/icons/github.svg" />Continue With GitHub</div>
          <div class="thirdPartyButton"><img src="../assets/icons/google.svg" />Continue With Google</div>
          <div class="thirdPartyButton"><img src="../assets/icons/apple.svg" />Continue With Apple</div>
          <div class="thirdPartyButton"><img src="../assets/icons/facebook.svg" />Continue With Facebook</div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
@import "../assets/styles/panda-main.css";
</style>
