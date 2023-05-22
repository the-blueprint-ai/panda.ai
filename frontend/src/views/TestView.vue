<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { useToast } from "vue-toastification";

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
      modal: null,
    };
  },
  mounted() {
    this.typeSentence();
    const toast = useToast();
    toast.warning("I'm a toast!");
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
    <div class="container-fluid vh-100 bg-primary text-white">
      <div class="container text-center pt-5 pb-5">
        <h1 class="mb-5">TESTING</h1>
        <button class="btn btn-secondary mb-5" @click="addSentences">
          Add sentences
        </button>
        <div id="app">
          <p v-for="(sentence, index) in sentences" :key="index">
            <span v-html="getCurrentText(index)"></span>
          </p>
        </div>
      </div>
      <h2 class="cursor text-center">TESTING</h2>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
.smallcursor {
  display: inline-block;
  width: 12px;
  height: 16px;
  margin-left: 5px;
  background-color: white;
}
@keyframes cursor-blink {
  0% {
    opacity: 0;
  }
}
.cursor::after {
  margin-left: 10px;
  margin-bottom: -1px;
  content: "";
  width: 15px;
  height: 25px;
  background: #ffcb4c;
  display: inline-block;
  opacity: 100%;
  animation: cursor-blink 1.5s steps(2, jump-none) infinite;
}
</style>
