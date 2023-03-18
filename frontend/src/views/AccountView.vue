<script>
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import { mapActions } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {
      // session: false,
      // userId: "",
      // email: "",
      // first_name: "",
      // last_name: "",
      // username: "",
    };
  },
  computed: {
    session() {
      return this.$store.state.userStore.session;
    },
    userId() {
      return this.$store.state.userStore.userId;
    },
    email() {
      return this.$store.state.userStore.email;
    },
    first_name() {
      return this.$store.state.userStore.first_name;
    },
    last_name() {
      return this.$store.state.userStore.last_name;
    },
    username() {
      return this.$store.state.userStore.username;
    },
    avatar() {
      return this.$store.state.userStore.avatar;
    },
  },
  async mounted() {
    await this.getSession();
    await this.getUserInfo();
  },
  methods: {
    ...mapActions(['getSession', 'getUserInfo']),
    redirectToLogin() {
      window.location.href = "/auth";
    },
    redirectToChat() {
      window.location.href = "/" + this.userId + "/chat";
    },
    async onLogout() {
      await Session.signOut();
      window.location.href = "/"
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
      <div v-if="session">
        <div>
          <h1>ACCOUNT VIEW</h1>
          <h3>Your UserID Is:</h3>
          <span>{{ userId }}</span>
          <h3>Your SessionID Is:</h3>
          <span>{{ session }}</span>
          <h3>Your Email Is:</h3>
          <span>{{ email }}</span>
          <h3>Your First Name Is:</h3>
          <span>{{ first_name }}</span>
          <h3>Your Last Name Is:</h3>
          <span>{{ last_name }}</span>
          <h3>Your Username Is:</h3>
          <span>{{ username }}</span>
          <h3>Your Avatar Is:</h3>
          <span><img v-bind:src="avatar" class="avatar" /></span>
        </div>
        <div className="spacer">
          <button className="chatButton userPageButton" @click="redirectToChat">Let's Chat</button>
        </div>
      </div>
      <div v-else>
        <button className="authButton-login" @click="redirectToLogin">Sign In</button>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
<style scoped>
@import "../assets/styles/panda-main.css";
</style>
