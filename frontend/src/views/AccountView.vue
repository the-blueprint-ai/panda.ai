<script lang="ts">
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";

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
      window.location.href = "/"
    },
  },
  components: {
    navBar,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div className="body">
      <div v-if="session">
        <div>
          <h1>ACCOUNT VIEW</h1>
          <h3>Your UserId Is:</h3>
          <span>{{ userId }}</span>
          <h3>Your Email Is:</h3>
          <span>{{ email }}</span>
        </div>
        <div className="spacer">
          <button className="chatButton userPageButton" @click="redirectToChat">Let's Chat</button>
        </div>
      </div>
      <div v-else>
        <button className="authButton-login" @click="redirectToLogin">Sign In</button>
      </div>
    </div>
  </main>
</template>
<style scoped>
  @import '../assets/styles/panda-main.css';
</style>
