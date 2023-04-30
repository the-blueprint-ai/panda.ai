<script>
export default {
  props: {
    faqSection: {
      type: Object,
      default: () => ({}),
    },
    hideSectionTitles: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      visibleItems: [],
    };
  },
  created() {
    this.initVisibleItems();
  },
  methods: {
    toggleVisibility(index) {
      this.visibleItems[index] = !this.visibleItems[index];
    },
    initVisibleItems() {
      this.visibleItems = this.faqSection.items.map(() => false);
    },
    formatAnswer(answer) {
      const urlRegex = /(https?:\/\/[^\s]+[\w/.)]+)/g;
      const formattedAnswer = answer.replace(
        urlRegex,
        '<a href="$&" target="_blank">$&</a>'
      );
      return formattedAnswer;
    },
  },
};
</script>

<template>
  <div class="faqContent">
    <div v-if="!hideSectionTitles" class="faqTitle">
      <h2 class="text-uppercase mt-3 mb-3">{{ faqSection.title }}</h2>
    </div>
    <div
      v-for="(faq, index) in faqSection.items"
      :key="index"
      class="faqContent"
    >
      <button class="faqQuestion" @click="toggleVisibility(index)">
        {{ faq.question }}
        <img
          v-if="visibleItems[index]"
          src="../assets/icons/caret-up-fill.svg"
        />
        <img v-else src="../assets/icons/caret-down-fill.svg" />
      </button>
      <div v-if="visibleItems[index]" class="faqAnswer">
        <p v-html="formatAnswer(faq.answer)"></p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.faqContent {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
.faqQuestion {
  width: 700px;
  display: flex;
  justify-content: space-between;
  margin-top: 0px;
  margin-bottom: 15px;
  background-color: #FFFFFF;
  color: #000000;
  border: none;
  border-radius: 8px;
  padding: 20px;
  text-align: left;
  text-transform: uppercase;
  font-size: 18px;
  font-family: 'Iosevka';
}
.faqQuestion img {
  margin-top: 4px;
}
.faqQuestion:hover {
  cursor: pointer;
  background-color: #FFCB4C;
}
.faqAnswer {
  width: 680px;
  padding: 10px;
  padding-top: 20px;
  margin-top: -20px;
  text-align: start;
}
.faqAnswer a {
  color: #FFCB4C;
  text-decoration: none;
}
</style>
