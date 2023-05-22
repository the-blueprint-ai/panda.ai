<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import SpinnerComponent from "../components/spinnerComponent.vue";
import { sendEmail } from "../composables/sendEmail.js";
import support_request_html from "../assets/emails/supportRequestEmail.js";
import support_send_html from "../assets/emails/supportSendEmail.js";
import { useToast } from "vue-toastification";

export default defineComponent({
  data() {
    return {
      email: "",
      confirmedEmail: "",
      message: "",
      loading: false,
      buttonText: "SEND",
      failedSend: false,
    };
  },
  methods: {
    async sendSupportEmails(to_email, message) {
      const toast = useToast();
      this.loading = true;
      const support_message = support_send_html(this.confirmedEmail, message);
      try {
        await sendEmail(
          "support@mypanda.ai",
          to_email,
          "Thank you for your support message",
          support_request_html
        );
        await sendEmail(
          "website@mypanda.ai",
          "support@mypanda.ai",
          "Website support request",
          support_message
        );
        this.loading = false;
        this.buttonText = "SENT!";
        toast.success("Email sent!");
      } catch (error) {
        this.failedSend = true;
        toast.error("An error occurred while sending the emails:", error);
        setTimeout(() => (this.failedSend = false), 2000);
      } finally {
        setTimeout(() => (this.buttonText = "SEND"), 2000);
        setTimeout(() => (this.email = ""), 2000);
        setTimeout(() => (this.confirmedEmail = ""), 2000);
        setTimeout(() => (this.message = ""), 2000);
      }
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
    <div class="container-fluid vh-100 bg-primary text-white">
      <div class="container text-center pt-5 pb-5">
        <div
          class="card text-bg-light mt-5 mb-3 m-auto"
          style="max-width: 32rem"
        >
          <div class="card-header pt-3 pb-3">
            <h1>🐼</h1>
            <h1>CONTACT US</h1>
            <p>
              If you can't find what you're looking for in the FAQs above,
              please get in touch with us using the form below:
            </p>
          </div>
          <div class="card-body pt-5 pb-4 px-5">
            <div class="form-floating mb-3">
              <input
                class="form-control"
                id="emailInput"
                type="email"
                v-model="email"
                placeholder="kungu-fu-panda@mypanda.ai"
              />
              <label class="text-primary" for="emailInput">Email</label>
            </div>
            <div class="form-floating mb-3">
              <input
                class="form-control"
                id="confirmInput"
                type="email"
                v-model="confirmedEmail"
                placeholder="kungu-fu-panda@mypanda.ai"
              />
              <label class="text-primary" for="confirmInput"
                >Confirm Email</label
              >
            </div>
            <div class="form-floating mb-3">
              <textarea
                class="form-control"
                id="messageInput"
                type="email"
                v-model="message"
                placeholder="kungu-fu-panda@mypanda.ai"
              ></textarea>
              <label class="text-primary" for="messageInput"
                >Please enter your message...</label
              >
            </div>
          </div>
          <div class="card-footer pt-4 pb-4">
            <button
              v-if="
                this.email.length > 0 &&
                this.email === this.confirmedEmail &&
                this.message.length > 0
              "
              class="btn btn-secondary btn-lg d-inline-flex justify-content-center"
              @click="sendSupportEmails(this.confirmedEmail, this.message)"
              style="width: 70%"
            >
              <SpinnerComponent
                :loading="this.loading"
                :button-text="this.buttonText"
              ></SpinnerComponent>
            </button>
            <button
              v-else
              class="btn btn-secondary btn-lg m-auto"
              style="width: 70%"
              disabled
            >
              SEND
            </button>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
