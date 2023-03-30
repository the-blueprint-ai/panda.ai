<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {
      sentences: [
        "This is the first sentence.",
        "Here is the second one.",
        "And this is the last sentence.",
        "Or is it?",
        "How many sentences can I do?!",
        "One more?!",
      ],
      currentIndex: 0,
      currentLetter: 0,
      typingSpeed: 50,
      pauseDuration: 1000,
      initiallength: 6,
      lastTypedIndex: -1,
    };
  },
  mounted() {
    this.typeSentence();
  },
  methods: {
    getCurrentText(index) {
      if (index < this.currentIndex) {
        return this.sentences[index];
      } else if (index === this.currentIndex) {
        return (
          this.sentences[index].substring(0, this.currentLetter) +
          '<span class="cursor"></span>'
        );
      } else if (
        index === this.sentences.length - 1 &&
        this.currentIndex === this.sentences.length
      ) {
        return this.sentences[index] + '<span class="cursor"></span>';
      }
      return "";
    },
    typeSentence() {
      if (this.currentIndex >= this.sentences.length) {
        this.lastTypedIndex = this.sentences.length - 1;
        return;
      }

      if (this.currentLetter < this.sentences[this.currentIndex].length) {
        this.currentLetter++;
        setTimeout(this.typeSentence, this.typingSpeed);
      } else {
        setTimeout(() => {
          this.currentIndex++;
          this.currentLetter = 0;
          this.typeSentence();
        }, this.pauseDuration);
      }
    },
    addSentences() {
      this.sentences.push("New sentence 1");
      this.sentences.push("New sentence 2");
      this.sentences.push("New sentence 3");
    },
  },
  watch: {
    sentences: {
      deep: true,
      handler(newValue, oldValue) {
        if (this.lastTypedIndex !== this.sentences.length - 1) {
          this.typeSentence();
        }
      },
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
    <div class="body">
      <h1>TESTING</h1>
      <button @click="addSentences">Add sentences</button>
      <div id="app">
        <p v-for="(sentence, index) in sentences" :key="index">
          <span v-html="getCurrentText(index)"></span>
        </p>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style>
/* @import "../assets/styles/panda-main.css"; */

.smallcursor {
  display: inline-block;
  width: 12px;
  height: 16px;
  margin-left: 5px;
  background-color: white;
}
</style>
