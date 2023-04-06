<script>
import { defineComponent } from "vue";
import { mapGetters } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { getFAQs } from "../composables/getFAQs.js";
import CollapsibleFAQList from "../components/collapsibleFAQList.vue";

export default defineComponent({
  data() {
    return {
      searchQuery: "",
      email: "",
      confirmedEmail: "",
      message: "",
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
  components: {
    navBar,
    navFooter,
    CollapsibleFAQList,
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
          <div class="contactFormItem">
            <h2>Email:</h2>
            <input v-model="email" class="emailInput" />
          </div>
          <div class="contactFormItem">
            <h2>Confirm Email:</h2>
            <input v-model="confirmedEmail" class="emailInput" />
          </div>
          <div class="contactFormItemLong">
            <h2>Please enter your message:</h2>
            <textarea v-model="message" class="messageInput"></textarea>
          </div>
          <button
            v-if="this.email === this.confirmedEmail && this.message.length > 0"
            class="chatButton"
          >
            SEND
          </button>
          <button v-else class="chatButtonDisabled">SEND</button>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style>
@import "../assets/styles/panda-main.css";
</style>
