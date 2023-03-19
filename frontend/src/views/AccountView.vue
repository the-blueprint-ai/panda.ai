<script>
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import { mapActions } from "vuex";
import { DateTime } from "luxon";
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
    joined() {
      return this.$store.state.userStore.joined;
    },
    chatHistory() {
      return this.$store.state.userStore.chatHistory;
    },
  },
  async mounted() {
    await this.getSession();
    await this.getUserInfo();
    await this.getUserData();
    await this.getChatHistory();
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
    setJoined(value) {
      this.$store.commit("setJoined", value);
    },
    setChatHistory(value) {
      this.$store.commit("setChatHistory", value);
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
        this.setFirstName(response.first_name);
        this.setLastName(response.last_name);
        this.setUsername(response.username);
        this.setEmail(response.email);
        this.setAvatar(response.avatar);
        var dt = DateTime.fromISO(response.created_at);
        this.setJoined(dt.toLocaleString(DateTime.DATE_FULL));
      } catch (error) {
        // Handle the error
        console.log("An error occurred while saving the file:", error);
      }
    },
    getChatHistory: async function () {
      try {
        const url =
          "http://localhost:3001/get-user-chat-history/?user_id=" + this.userId;
        const res = await fetch(url, {
          method: "GET",
        });

        // Check if the response status indicates an error
        if (!res.ok) {
          throw new Error(`Server responded with status ${res.status}`);
        }

        const response = await res.json();
        console.log(response);
        this.setChatHistory(response);
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
          <img v-if="first_name" v-bind:src="avatar" class="accountAvatar" />
          <img src="../assets/camera.svg" class="avatarCamera" />
        </div>
        <div className="profilePanel">
          <div className="userDetails">
            <h2>{{ first_name }} {{ last_name }}</h2>
            <h3>{{ username }}</h3>
            <p>{{ email }}</p>
            <p>Joined: {{ joined }}</p>
            <button className="chatButton" @click="redirectToChat">Let's Chat</button>
          </div>
          <div className="aboutDetails">
            <h2>ABOUT</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus aliquet elit augue, at feugiat leo pulvinar nec. Maecenas consequat, elit a ornare dignissim, justo lorem auctor lectus, et accumsan urna urna ac est. Phasellus convallis quam eros, et tincidunt mauris iaculis at. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum ultrices sodales condimentum. Fusce rutrum hendrerit dignissim. Aenean non nibh vestibulum, gravida lectus quis, pharetra nulla. Aenean blandit diam porta, ullamcorper neque quis, maximus urna. Vivamus purus libero, vulputate id auctor non, vestibulum et enim.</p>
          </div>
          <div className="editUserDetails">
            <img src="../assets/three-dots-vertical.svg" className="profileEdit" />
          </div>
        </div>
        <div className="accountDetailsWrapper">
          <div className="accountDetailsMenu">
            <button className="accountDetailsMenuButton">History</button>
            <button className="accountDetailsMenuButton">Integrations</button>
            <button className="accountDetailsMenuButton">Subscription</button>
            <button className="accountDetailsMenuButton">Data</button>
            <button className="accountDetailsMenuButton">Settings</button>
          </div>
          <div className="profileMenuLine"></div>
          <div className="userChatHistory">
            <h1>HISTORY GOES HERE</h1>
            <p>{{ chatHistory }}</p>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
<style scoped>
@import "../assets/styles/panda-main.css";
@import "floating-vue/dist/style.css";
</style>
