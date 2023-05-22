<script>
import { defineComponent } from "vue";
import * as Session from "supertokens-web-js/recipe/session";
import { mapActions, mapGetters } from "vuex";
import { verifyEmail } from "supertokens-web-js/recipe/emailverification";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { useToast } from "vue-toastification";

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
  async mounted() {
    if (!this.session) {
      await this.getSession();
      this.consumeVerificationCode();
    } else if (this.session) {
      this.consumeVerificationCode();
    }
  },

  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    async consumeVerificationCode() {
      const toast = useToast();
      try {
        let response = await verifyEmail();
        if (response.status === "EMAIL_VERIFICATION_INVALID_TOKEN_ERROR") {
          // This can happen if the verification code is expired or invalid.
          // You should ask the user to retry
          toast.error(
            "Oops! Seems like the verification link expired. Please try again later."
          );
          this.$router.push("/auth/verify-email"); // back to the email sending screen.
        } else {
          // email was verified successfully.
          toast.success("Email verified successfully!");
          this.$router.push(this.userId + "/onboarding");
        }
      } catch (err) {
        if (err.isSuperTokensGeneralError === true) {
          // this may be a custom error message sent from the API by you.
          toast.error(err.message);
        } else {
          toast.error(
            "Oops! Seems like the verification link expired. Please try again later."
          );
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
    <div class="mainContainer container-fluid bg-primary text-white">
      <div class="container d-flex justify-content-center pt-5 pb-5">
        <div class="card text-bg-light text-center mb-3" style="width: 32rem">
          <div class="card-header pt-3 pb-3">
            <img
              src="../assets/panda.png"
              class="w-20 h-20"
              alt="panda"
              width="50"
            />
            <h2 class="pt-3">EMAIL VERIFIED!</h2>
          </div>
          <div class="card-body pt-4 pb-4 px-5">
            <img
              id="emailSentEnvelope"
              src="../assets/icons/envelope-paper-heart-fill.svg"
              width="50"
            />
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
