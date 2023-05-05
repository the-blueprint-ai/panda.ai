<script>
import { defineComponent } from "vue";
import { mapGetters } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { getFAQs } from "../composables/getFAQs.js";
import CollapsibleFAQList from "../components/collapsibleFAQList.vue";
import SpinnerComponent from "../components/spinnerComponent.vue";
import { sendEmail } from "../composables/sendEmail.js";
import support_request_html from "../assets/emails/supportRequestEmail.js";
import support_send_html from "../assets/emails/supportSendEmail.js";

export default defineComponent({
  data() {
    return {
      searchQuery: "",
      email: "",
      confirmedEmail: "",
      message: "",
      loading: false,
      buttonText: "SEND",
      failedSend: false,
    };
  },
  async mounted() {
    // Call the getFAQs function and wait for it to complete
    getFAQs(this.$store);
  },
  computed: {
    ...mapGetters("faqsStore", {
      getStoreFAQs: "getStoreSortedFAQs",
    }),
    // faqData() {
    //   return this.getStoreSortedFAQs || [];
    // },
    filteredFaqs() {
      const query = this.searchQuery.trim().toLowerCase();
      const faqs = this.getStoreFAQs.map((faqSection) => ({
        title: faqSection.title,
        items: faqSection.items.map((faq) => ({
          question: faq.question,
          answer: faq.answer,
          visible: faq.visible,
        })),
      }));

      const filterItemsByVisibility = (items) =>
        items.filter((faq) => faq.visible);
      const filterItemsByQuery = (items) =>
        items.filter((faq) => faq.question.toLowerCase().includes(query));

      const filteredFaqSections = faqs
        .map((faqSection) => ({
          ...faqSection,
          items: filterItemsByVisibility(faqSection.items),
        }))
        .filter((faqSection) => faqSection.items.length > 0);

      if (!query) {
        return filteredFaqSections;
      }

      return filteredFaqSections
        .map((faqSection) => ({
          ...faqSection,
          items: filterItemsByQuery(faqSection.items),
        }))
        .filter((faqSection) => faqSection.items.length > 0);
    },
  },
  methods: {
    async sendSupportEmails(to_email, message) {
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
      } catch (error) {
        console.error("An error occurred while sending the emails:", error);
        this.failedSend = true;
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
    CollapsibleFAQList,
    SpinnerComponent,
  },
});
</script>

<template>
  <main style="min-height: 71vh">
    <navBar></navBar>
    <div class="container-fluid bg-primary text-white">
      <div v-if="this.getStoreFAQs" class="container pt-5 pb-5 text-center">
        <h1>🐼</h1>
        <h1 class="mb-5">WHAT CAN WE HELP YOU WITH?</h1>
        <div class="d-flex justify-content-center">
          <div class="form-floating mb-3" style="width: 500px">
            <input
              class="form-control"
              id="searchInput"
              type="text"
              v-model="searchQuery"
              placeholder="🐼 Search for answers..."
            />
            <label class="text-primary" for="searchInput"
              >🐼 Search for answers...</label
            >
          </div>
        </div>
        <CollapsibleFAQList
          v-for="(faqSection, index) in filteredFaqs"
          :key="index"
          :faq-section="faqSection"
          :hide-section-titles="searchQuery.trim() !== ''"
        />
        <div class="d-flex justify-content-center">
          <div class="card text-bg-light mt-5 mb-3" style="width: 500px">
            <div class="card-header mt-n4 pb-3">
              <h1 class="mt-5">CONTACT US</h1>
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
              <button v-else class="btn btn-secondary btn-lg" disabled>
                SEND
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
