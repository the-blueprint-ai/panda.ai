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
      modal: null,
    };
  },
  props: {
    modalId: {
      type: String,
      required: true,
    },
  },
  mounted() {
    this.typeSentence();
    this.isMobile = window.innerWidth <= 768;
    window.addEventListener("resize", () => {
      this.isMobile = window.innerWidth <= 768;
    });
    const bootstrapModal = new bootstrap.Modal(
      document.getElementById(this.modalId)
    );
    this.modal = bootstrapModal;
  },
  methods: {
    closeModal() {
      this.modal.hide();
    },
    openModal() {
      this.modal.show();
    },
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
  <main style="height: 71vh">
    <navBar></navBar>
    <div class="container-fluid h-100 bg-primary text-white">
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
        <!-- Button trigger modal -->
        <button type="button" class="btn btn-secondary mt-5" @click="openModal">
          Launch demo modal
        </button>

        <!-- Modal -->
        <div
          class="modal fade"
          :id="modalId"
          tabindex="-1"
          :aria-labelledby="modalId + 'Label'"
          aria-hidden="true"
        >
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h1 class="modal-title fs-5" :id="modalId + 'Label'">
                  Modal title
                </h1>
                <button
                  type="button"
                  class="btn-close"
                  @click="closeModal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                <slot></slot>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="closeModal"
                >
                  Close
                </button>
                <button type="button" class="btn btn-primary">
                  Save changes
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style>
.smallcursor {
  display: inline-block;
  width: 12px;
  height: 16px;
  margin-left: 5px;
  background-color: white;
}
</style>
