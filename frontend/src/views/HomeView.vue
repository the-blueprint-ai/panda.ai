<script lang="ts">
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data: () => {
    return {
      session: false,
      userId: "",
      typeValue: "",
      typeStatus: false,
      displayTextArray: ["Welcome to panda.ai"],
      typingSpeed: 100,
      newTextDelay: 1500,
      displayTextArrayIndex: 0,
      charIndex: 0,
    };
  },
  props: {},
  created() {
    setTimeout(this.typeText, this.newTextDelay + 200);
  },
  mounted() {
    this.getUserInfo();
  },
  methods: {
    async getUserInfo() {
      this.session = await Session.doesSessionExist();
      if (this.session) {
        this.userId = await Session.getUserId();
      }
    },
    userLink() {
      if (this.userId) {
        return { name: "user", param: { userid: this.userId } };
      } else {
        return { name: "user", param: { userid: "userID" } };
      }
    },
    typeText() {
      if (
        this.charIndex <
        this.displayTextArray[this.displayTextArrayIndex].length
      ) {
        if (!this.typeStatus) this.typeStatus = true;
        this.typeValue += this.displayTextArray[
          this.displayTextArrayIndex
        ].charAt(this.charIndex);
        this.charIndex += 1;
        setTimeout(this.typeText, this.typingSpeed);
      } else {
        this.typeStatus = false;
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
    <div className="body">
      <img src="../../src/assets/panda.png" className="biglogo" width="200" />
      <h1>
        <span className="typed-text">{{ typeValue }}</span>
        <span className="blinking-cursor">|</span>
        <span className="blinking-cursor2">|</span>
        <span className="blinking-cursor2">|</span>
        <span className="blinking-cursor2">|</span>
        <span className="blinking-cursor2">|</span>
        <span className="blinking-cursor2">|</span>
        <span className="blinking-cursor2">|</span>
        <span className="blinking-cursor2">|</span>
        <span className="cursor" :class="{ typing: typeStatus }">&nbsp;</span>
      </h1>
      <router-link :to="'/' + userId + '/chat'">
        <button className="letsChat">Let's Chat</button>
      </router-link>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
@import "../assets/styles/panda-main.css";
</style>
