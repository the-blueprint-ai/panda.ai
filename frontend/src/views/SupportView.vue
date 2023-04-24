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
  async created() {
    // Call the getFAQs function and wait for it to complete
    await getFAQs(this.$store);
  },
  computed: {
    ...mapGetters("faqsStore", {
      getStoreFAQs: "getStoreSortedFAQs",
    }),
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
        setTimeout(() => this.failedSend = false, 2000);
      } finally {
        setTimeout(() => this.buttonText = "SEND", 2000);
        setTimeout(() => this.email = "", 2000);
        setTimeout(() => this.confirmedEmail = "", 2000);
        setTimeout(() => this.message = "", 2000);
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
  <main>
    <navBar></navBar>
    <div class="body">
      <div v-if="getStoreFAQs" class="faqContainer">
        <h1>🐼</h1>
        <h1>WHAT CAN WE HELP YOU WITH?</h1>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="🐼 Search for answers..."
          class="searchBar"
        />
        <CollapsibleFAQList
          v-for="(faqSection, index) in filteredFaqs"
          :key="index"
          :faq-section="faqSection"
          :hide-section-titles="searchQuery.trim() !== ''"
        />
      </div>
      <div class="contactContainer">
        <h2>CONTACT US</h2>
        <p>
          If you can't find what you're looking for in the FAQs above, please
          get in touch with us using the form below:
        </p>
        <div class="contactForm">
          <div class="contactFormItemContainer">
            <div class="contactFormItem">
              <h2>Email:</h2>
              <input v-model="email" class="emailInput" />
            </div>
            <div class="contactFormItem">
              <h2>Confirm Email:</h2>
              <input v-model="confirmedEmail" class="emailInput" />
            </div>
          </div>
          <div class="contactFormItemLong">
            <h2>Please enter your message:</h2>
            <textarea v-model="message" class="messageInput"></textarea>
          </div>
          <button
            v-if="this.email === this.confirmedEmail && this.message.length > 0"
            class="chatButton"
            @click="sendSupportEmails(this.confirmedEmail, this.message)"
          >
            <SpinnerComponent
              :loading="this.loading"
              :button-text="this.buttonText"
            ></SpinnerComponent>
          </button>
          <button v-else class="chatButtonDisabled">SEND</button>
          <div v-if="this.failedSend" class="failedSend"><h2>Message failed to send. Please try again later.</h2></div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
