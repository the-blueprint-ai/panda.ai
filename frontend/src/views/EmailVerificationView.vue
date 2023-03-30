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
  computed: {
    email() {
      return this.$store.state.userStore.email;
    },
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
          console.log("EmailVerificationView: " + this.email);
          this.saveEmail(userId, this.email);
          // window.location.href = userId + "/onboarding";
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
    async saveEmail(userId, email) {
      console.log("saveEmail called. userID is: " + userId, "email is: " + email);
      try {
        const url =
          import.meta.env.VITE_APP_API_URL + "/users/save/?user_id=" +
          userId +
          "&email=" +
          email;
        const res = await fetch(url, {
          method: "POST",
        });
        // Check if the response status indicates an error
        if (!res.ok) {
          const errorResponse = await res.json();
          console.error("Server error response:", errorResponse);
          throw new Error(`Server responded with status ${res.status}`);
        }
      } catch (error) {
        // Handle the error
        console.error("An error occurred while saving the email:", error);
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
