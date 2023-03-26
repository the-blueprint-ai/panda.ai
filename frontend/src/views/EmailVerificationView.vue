<script>
import { defineComponent } from "vue";
import * as Session from "supertokens-web-js/recipe/session";
import { mapActions } from "vuex";
import { verifyEmail } from "supertokens-web-js/recipe/emailverification";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {};
  },
  mounted() {
    this.consumeVerificationCode();
  },

  methods: {
    ...mapActions(["getSession", "getUserInfo"]),
    async consumeVerificationCode() {
      try {
        let response = await verifyEmail();
        if (response.status === "EMAIL_VERIFICATION_INVALID_TOKEN_ERROR") {
          // This can happen if the verification code is expired or invalid.
          // You should ask the user to retry
          window.alert(
            "Oops! Seems like the verification link expired. Please try again"
          );
          window.location.assign("/auth/email"); // back to the email sending screen.
        } else {
          // email was verified successfully.
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
      <div class="emailVerifiedContainer">
        <img id="emailSentPanda" src="../assets/panda.png" />
        <h2>EMAIL VERIFIED!</h2>
        <img
          id="emailSentEnvelope"
          src="../assets/icons/envelope-paper-heart-fill.svg"
        />
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style>
@import "../assets/styles/panda-main.css";
</style>
