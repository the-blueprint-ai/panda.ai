<script>
import { defineComponent } from "vue";
import { mapGetters, mapActions, mapState } from "vuex";
import * as Session from "supertokens-web-js/recipe/session";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {};
  },
  watch: {
    getEmail(newValue) {
      if (newValue) {
        console.log("EmailView, from store: " + newValue);
      }
    },
  },
  mounted() {
    console.log("EmailView, from store: " + this.email);
  },
  computed: {
    ...mapGetters("userStore", ["getEmail"]),
    ...mapState("userStore", ["email"]),
  },
  methods: {
    ...mapActions("userStore", ["getSession"]),
    async onLogout() {
      await Session.signOut();
      window.location.href = "/";
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
        <h2>VERIFICATION EMAIL SENT...</h2>
        <img
          id="emailSentEnvelope"
          src="../assets/icons/envelope-paper-heart-fill.svg"
        />
        <div class="signInBar"></div>
        <p>
          Please click on the link in the email we just sent you to confirm your
          email address and complete the sign up process.
        </p>
        <h3 @click="emailVerification">RESEND EMAIL</h3>
        <button class="authButton-login" @click="onLogout">LOGOUT</button>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style>
@import "../assets/styles/panda-main.css";
</style>
