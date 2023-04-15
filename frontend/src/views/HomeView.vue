<script>
import { defineComponent } from "vue";
import { mapActions, mapGetters, mapMutations } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data: () => {
    return {
      typingTimeout: null,
    };
  },
  computed: {
    ...mapGetters("userStore", {
      session: "getStoreSession",
      userId: "getStoreUserId",
    }),
    ...mapGetters("typingStore", {
      typeValue: "getTypeValue",
      typeStatus: "getTypeStatus",
      typingSpeed: "getTypingSpeed",
      newTextDelay: "getNewTextDelay",
      displayTextArray: "getDisplayTextArray",
      displayTextArrayIndex: "getDisplayTextArrayIndex",
      charIndex: "getCharIndex",
    }),
  },
  async mounted() {
    this.initHomePage();
  },
  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    ...mapMutations("typingStore", {
      setTypeValueValue: "setTypeValue",
      setTypeStatusValue: "setTypeStatus",
      setDisplayTextArray: "setDisplayTextArray",
      setTypingSpeedValue: "setTypingSpeed",
      setNewTextDelayValue: "setNewTextDelay",
      setDisplayTextArrayValue: "setDisplayTextArray",
      setDisplayTextArrayIndexValue: "setDisplayTextArrayIndex",
      setCharIndexValue: "setCharIndex",
    }),
    async initHomePage() {
      this.setCharIndexValue(0);
      this.setTypeValueValue("");
      setTimeout(this.typeText, this.newTextDelay + 200);
      try {
        await this.getSession();
        if (this.session) {
          await this.getUserInfo();
        }
      } catch (error) {
        console.error("Error in initHomePage:", error);
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
        this.typingTimeout = setTimeout(this.typeText, this.typingSpeed);
      } else {
        this.setTypeStatusValue(false);
        this.typingTimeout = setTimeout(this.newTextDelay);
      }
    },
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.initHomePage();
    });
  },
  beforeRouteUpdate(to, from, next) {
    this.initHomePage();
    next();
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
        <router-link :to="'/signin'">
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
