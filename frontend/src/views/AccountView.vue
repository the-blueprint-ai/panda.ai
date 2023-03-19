<script>
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import { mapActions } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {};
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
    await this.getUserData();
  },
  methods: {
    ...mapActions(["getSession", "getUserInfo"]),
    redirectToLogin() {
      window.location.href = "/auth";
    },
    redirectToChat() {
      window.location.href = "/" + this.userId + "/chat";
    },
    async onLogout() {
      await Session.signOut();
      window.location.href = "/";
    },
    setFirstName(value) {
      this.$store.commit("setFirstName", value);
    },
    setLastName(value) {
      this.$store.commit("setLastName", value);
    },
    setUsername(value) {
      this.$store.commit("setUsername", value);
    },
    setEmail(value) {
      this.$store.commit("setEmail", value);
    },
    setAvatar(value) {
      this.$store.commit("setAvatar", value);
    },
    getUserData: async function () {
      try {
        const url =
          "http://localhost:3001/get-user-data/?user_id=" + this.userId;
        const res = await fetch(url, {
          method: "GET",
        });

        // Check if the response status indicates an error
        if (!res.ok) {
          throw new Error(`Server responded with status ${res.status}`);
        }

        const response = await res.json();
        console.log(response);
        this.setFirstName(response.first_name);
        this.setLastName(response.last_name);
        this.setUsername(response.username);
        this.setEmail(response.email);
        this.setAvatar(response.avatar);
      } catch (error) {
        // Handle the error
        console.log("An error occurred while saving the file:", error);
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
    <div className="bodyG">
      <div v-if="session" className="accountWrapper">
        <div className="userBanner">
          <img src="../assets/camera2.svg" class="bannerCamera" />
        </div>
        <div className="profileAvatar">
          <div class="accountAvatarBackground"></div>
          <img v-bind:src="avatar" class="accountAvatar" />
          <img src="../assets/camera.svg" class="avatarCamera" />
        </div>
        <div className="profilePanel">
          <div className="userDetails">
            <h2>{{ first_name }} {{ last_name }}</h2>
            <h3>{{ username }}</h3>
            <p>{{ email }}</p>
            <button className="chatButton" @click="redirectToChat">Let's Chat</button>
          </div>
          <div className="aboutDetails">
            <h2>ABOUT</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam maximus ut libero id tempor. Nulla eget consequat nunc, cursus tempor nisi. Vestibulum euismod magna sed sem tristique, sit amet fringilla orci accumsan. In nec sem vel dolor dapibus congue. Sed rutrum massa eget ante efficitur pretium. In tristique rutrum ipsum vitae blandit. Sed pretium, leo suscipit pulvinar aliquet, quam quam posuere massa, sed mattis leo purus non massa. Quisque blandit.</p>
          </div>
          <div className="editUserDetails">
            <img src="../assets/three-dots-vertical.svg" className="profileEdit" />
          </div>
        </div>
        <div className="spacer"></div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
<style scoped>
@import "../assets/styles/panda-main.css";
</style>
