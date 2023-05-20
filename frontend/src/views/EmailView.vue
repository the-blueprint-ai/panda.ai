<script>
import { defineComponent } from "vue";
import { mapActions, mapGetters } from "vuex";
import * as Session from "supertokens-web-js/recipe/session";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { emailVerification } from "../composables/emailVerification.js";
import { saveEmail } from "../composables/saveEmail.js";
import { sendEmail } from "../composables/sendEmail.js";
import welcome_html from "../assets/emails/welcomeEmail.js";
import SpinnerComponent from "../components/spinnerComponent.vue";
import { useToast } from "vue-toastification";

export default defineComponent({
  data() {
    return {
      sendButtonText: "LOGOUT",
      loading: false,
    };
  },
  watch: {},
  async mounted() {
    await this.getSession();
    await this.getUserInfo();
    saveEmail(this.userId, this.email);
    sendEmail(
      "hello@mypanda.ai",
      this.email,
      "Welcome to 🐼 panda.ai!",
      welcome_html
    );
  },
  computed: {
    ...mapGetters("userStore", {
      userId: "getStoreUserId",
      email: "getStoreEmail",
    }),
  },
  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    async callEmailVerification(userId) {
      console.log("called");
      const toast = useToast();
      await emailVerification(userId, toast);
    },
    async onLogout() {
      await Session.signOut();
      this.$router.push("/");
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
  <main style="height: 71vh">
    <navBar></navBar>
    <div class="container-fluid h-100 bg-primary text-white">
      <div class="container d-flex justify-content-center pt-5 pb-5">
        <div class="card text-bg-light text-center mb-3" style="width: 32rem">
          <div class="card-header pt-3 pb-3">
            <img
              src="../assets/panda.png"
              class="w-20 h-20"
              alt="panda"
              width="50"
            />
            <h2 class="pt-3">VERIFICATION EMAIL SENT...</h2>
          </div>
          <div class="card-body pt-4 pb-4 px-5">
            <p>
              Please click on the link in the email we just sent you to confirm
              your email address and complete the sign up process.
            </p>
            <h5
              class="text-secondary mt-4"
              @click="callEmailVerification(userId)"
              style="cursor: pointer"
            >
              RESEND EMAIL
            </h5>
            <div class="pt-4">
              <button
                type="button"
                class="btn btn-secondary btn-lg mb-3 d-inline-flex justify-content-center"
                @click="onLogout"
                style="width: 70%"
              >
                <SpinnerComponent
                  :loading="this.loading"
                  :button-text="this.sendButtonText"
                ></SpinnerComponent>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
