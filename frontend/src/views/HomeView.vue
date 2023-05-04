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
  <main style="height: 71vh">
    <navBar></navBar>
    <div class="container-fluid h-100 bg-black text-white">
      <div class="container text-center pt-5 pb-5">
        <img src="../../src/assets/panda.png" width="200" />
        <h1 class="pt-5 pb-5">
          <span class="typed-text">{{ typeValue }}</span>
          <span class="cursorSpace" :class="{ typing: typeStatus }">&nbsp;</span>
          <span class="cursor"></span>
        </h1>
        <div v-if="session">
          <router-link :to="'/auth/' + userId + '/chat'">
            <button type="button" class="btn btn-secondary btn-lg">LET'S CHAT</button>
          </router-link>
        </div>
        <div v-else>
          <router-link :to="'/signin'">
            <button type="button" class="btn btn-secondary btn-lg">LET'S CHAT</button>
          </router-link>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
@keyframes cursor-blink {
  0% {
    opacity: 0;
  }
}
.cursor::after {
  margin-bottom: -3px;
  content: "";
  width: 20px;
  height: 35px;
  background: #FFFFFF;
  display: inline-block;
  opacity: 100%;
  animation: cursor-blink 1s steps(2, jump-none) infinite;
}
</style>
