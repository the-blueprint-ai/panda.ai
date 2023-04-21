<script>
import { defineComponent } from "vue";
import * as Session from "supertokens-web-js/recipe/session";
import { mapActions, mapGetters } from "vuex";
import { verifyEmail } from "supertokens-web-js/recipe/emailverification";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {};
  },
  computed: {
    ...mapGetters("userStore", {
      session: "getStoreSession",
      userId: "getStoreUserId",
      email: "getStoreEmail",
    }),
  },
  mounted() {
    this.consumeVerificationCode();
  },

  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    async consumeVerificationCode() {
      try {
        let response = await verifyEmail();
        if (response.status === "EMAIL_VERIFICATION_INVALID_TOKEN_ERROR") {
          // This can happen if the verification code is expired or invalid.
          // You should ask the user to retry
          window.alert(
            "Oops! Seems like the verification link expired. Please try again"
          );
          this.$router.push("/auth/email"); // back to the email sending screen.
          // window.location.assign("/auth/email"); // back to the email sending screen.
        } else {
          // email was verified successfully.
          this.$router.push(this.userId + "/onboarding");
          // window.location.href = this.userId + "/onboarding";
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