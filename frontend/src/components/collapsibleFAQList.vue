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
  },
};
</script>

<template>
  <div class="faqContent">
    <div v-if="!hideSectionTitles" class="faqTitle">
      <h2>{{ faqSection.title }}</h2>
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
        <p>{{ faq.answer }}</p>
      </div>
    </div>
  </div>
</template>

<style>
@import "../assets/styles/panda-main.css";
</style>
