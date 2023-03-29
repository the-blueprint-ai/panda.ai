<script>
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data: () => {
    return {
      session: false,
      userId: "",
    };
  },
  computed: {
    typeValue() {
      return this.$store.state.typingStore.typeValue;
    },
    typeStatus() {
      return this.$store.state.typingStore.typeStatus;
    },
    typingSpeed() {
      return this.$store.state.typingStore.typingSpeed;
    },
    newTextDelay() {
      return this.$store.state.typingStore.newTextDelay;
    },
    displayTextArray() {
      return this.$store.state.typingStore.displayTextArray;
    },
    displayTextArrayIndex() {
      return this.$store.state.typingStore.displayTextArrayIndex;
    },
    charIndex() {
      return this.$store.state.typingStore.charIndex;
    },
  },
  mounted() {
    this.getUserInfo();
    setTimeout(this.typeText, this.newTextDelay + 200);
  },
  methods: {
    setTypeValueValue(value) {
      this.$store.commit('setTypeValue', value)
    },
    setTypeStatusValue(value) {
      this.$store.commit('setTypeStatus', value)
    },
    setTypingSpeedValue(value) {
      this.$store.commit('setTypingSpeed', value)
    },
    setNewTextDelayValue(value) {
      this.$store.commit('setNewTextDelay', value)
    },
    setDisplayTextArrayValue(value) {
      this.$store.commit('setDisplayTextArray', value)
    },
    setDisplayTextArrayIndexValue(value) {
      this.$store.commit('setDisplayTextArrayIndex', value)
    },
    setCharIndexValue(value) {
      this.$store.commit('setCharIndex', value)
    },
    async getUserInfo() {
      this.session = await Session.doesSessionExist();
      if (this.session) {
        this.userId = await Session.getUserId();
      }
    },
    typeText() {
      if (
        this.charIndex <
        this.displayTextArray[this.displayTextArrayIndex].length
      ) {
        if (!this.typeStatus) this.setTypeStatusValue(true);
        this.setTypeValueValue(
          this.typeValue +
            this.displayTextArray[this.displayTextArrayIndex].charAt(
              this.charIndex
            )
        );
        this.setCharIndexValue(this.charIndex + 1);
        setTimeout(this.typeText, this.typingSpeed);
      } else {
        this.setTypeStatusValue(false);
        setTimeout(this.newTextDelay);
      }
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
      <img src="../../src/assets/panda.png" class="biglogo" width="200" />
      <h1>
        <span class="typed-text">{{ typeValue }}</span>
        <span class="blinking-cursor">|</span>
        <span class="blinking-cursor2">|</span>
        <span class="blinking-cursor2">|</span>
        <span class="blinking-cursor2">|</span>
        <span class="blinking-cursor2">|</span>
        <span class="blinking-cursor2">|</span>
        <span class="blinking-cursor2">|</span>
        <span class="blinking-cursor2">|</span>
        <span class="cursor" :class="{ typing: typeStatus }">&nbsp;</span>
      </h1>
      <div v-if="session">
        <router-link :to="'/' + userId + '/chat'">
          <button class="letsChat">Let's Chat</button>
        </router-link>
      </div>
      <div v-else>
        <router-link :to="'/auth'">
          <button class="letsChat">Let's Chat</button>
        </router-link>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
@import "../assets/styles/panda-main.css";
</style>
