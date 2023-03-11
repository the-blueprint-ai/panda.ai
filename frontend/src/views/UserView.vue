<script lang="ts">
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";

export default defineComponent({
  data() {
    return {
      session: false,
      userId: "",
      email: "",
      first_name: "",
      last_name: "",
      username: "",
    };
  },
  mounted() {
    this.getUserInfo();
  },
  methods: {
    redirectToLogin() {
      window.location.href = "/auth";
    },
    redirectToChat() {
      window.location.href = "/user/chat";
    },
    async getUserInfo() {
      this.session = await Session.doesSessionExist();
      if (this.session) {
        this.userId = await Session.getUserId();
        this.email = "test@test.com";
      }
    },
    async onLogout() {
      await Session.signOut();
      window.location.reload();
    },
  },
});
</script>

<template>
  <main>
    <div className="body">
      <img src="../../src/assets/panda.png" width="200"/>
      <h1>Welcome to panda.ai</h1>

      <div v-if="session">
        <div>
          <h2>USER VIEW</h2>
          <h3>Your UserId Is:</h3>
          <span>{{ userId }}</span>
          <h3>Your Email Is:</h3>
          <span>{{ email }}</span>
        </div>
        <div className="spacer">
          <button className="chatButton userPageButton" @click="redirectToChat">Let's Chat</button>
        </div>
        <button className="authButton" @click="onLogout">Sign Out</button>
      </div>
      <div v-else>
        <button className="authButton" @click="redirectToLogin">Sign In</button>
      </div>
    </div>
  </main>
</template>
<style scoped>
  @import '../assets/styles/panda-main.css';
</style>
