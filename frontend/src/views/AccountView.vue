<script>
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import { mapActions } from "vuex";
import { DateTime } from "luxon";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import UserChatHistory from "../components/userChatHistory.vue";
import UserIntegrations from "../components/userIntegrations.vue";
import UserSubscription from "../components/userSubscription.vue";
import UserData from "../components/userData.vue";
import UserSettings from "../components/userSettings.vue";

export default defineComponent({
  data() {
    return {
      historyMenu: true,
      integrationsMenu: false,
      subscriptionMenu: false,
      dataMenu: false,
      settingsMenu: false,
      historyMenuActive: true,
      integrationsMenuActive: false,
      subscriptionMenuActive: false,
      dataMenuActive: false,
      settingsMenuActive: false,
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
    banner() {
      return this.$store.state.userStore.banner;
    },
    joined() {
      return this.$store.state.userStore.joined;
    },
    userChatHistory() {
      return this.$store.state.userStore.userChatHistory;
    },
  },
  async mounted() {
    await this.getSession();
    await this.getUserInfo();
    await this.getUserData();
    await this.getUserChatHistory();
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
    setBanner(value) {
      this.$store.commit("setBanner", value);
    },
    setJoined(value) {
      this.$store.commit("setJoined", value);
    },
    setUserChatHistory(value) {
      this.$store.commit("setUserChatHistory", value);
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
        this.setBanner(response.banner);
        var dt = DateTime.fromISO(response.created_at);
        this.setJoined(dt.toLocaleString(DateTime.DATE_FULL));
      } catch (error) {
        // Handle the error
        console.log("An error occurred while saving the file:", error);
      }
    },
    getUserChatHistory: async function () {
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

        let chatHistory = [];

        for (let i in response) {
          var dt = DateTime.fromISO(response[i].created_at);
          var date = dt.toLocaleString(DateTime.DATE_FULL);
          var dt3 = DateTime.now().plus({ days: -1 });
          var yest = dt3.toLocaleString(DateTime.DATE_FULL);

          if (date == DateTime.now().DATE_FULL) {
            date = "Today";
          } else if (date == yest) {
            date = "Yesterday";
          } else {
            date = dt.toLocaleString(DateTime.DATE_FULL);
          }

          let time = dt.toLocaleString(DateTime.TIME_24_SIMPLE);
          let content = response[i].chat_script;

          let dateEntry = chatHistory.find(entry => entry.date === date); //null;

          if (!dateEntry) {
            dateEntry = {
              date: date,
              title: content.at(-1).message,
              chats: [],
            };
            chatHistory.push(dateEntry);
          }

          dateEntry.chats.push({
            time: time,
            content: content,
          });
        }

        // Use the groupedChatData object here, or set it to a reactive data property
        console.log(chatHistory);
        this.setUserChatHistory(chatHistory);
      } catch (error) {
        // Handle the error
        console.log("An error occurred while saving the file:", error);
      }
    },
    triggerBannerUpload() {
      this.$refs.bannerInput.click();
    },
    triggerAvatarUpload() {
      this.$refs.avatarInput.click();
    },
    handleBannerUpload(event) {
      const file = event.target.files[0];
      // Process the uploaded image file here
      console.log("Banner");
    },
    handleAvatarUpload(event) {
      const file = event.target.files[0];
      // Process the uploaded image file here
      console.log("Avatar");
    },
    toggleHistory() {
      this.historyMenu = true;
      this.integrationsMenu = false;
      this.subscriptionMenu = false;
      this.dataMenu = false;
      this.settingsMenu = false;
      this.historyMenuActive = true;
      this.integrationsMenuActive = false;
      this.subscriptionMenuActive = false;
      this.dataMenuActive = false;
      this.settingsMenuActive = false;
      this.classList.toggle("is-active");
    },
    toggleIntegrations() {
      this.historyMenu = false;
      this.integrationsMenu = true;
      this.subscriptionMenu = false;
      this.dataMenu = false;
      this.settingsMenu = false;
      this.historyMenuActive = false;
      this.integrationsMenuActive = true;
      this.subscriptionMenuActive = false;
      this.dataMenuActive = false;
      this.settingsMenuActive = false;
    },
    toggleSubscription() {
      this.historyMenu = false;
      this.integrationsMenu = false;
      this.subscriptionMenu = true;
      this.dataMenu = false;
      this.settingsMenu = false;
      this.historyMenuActive = false;
      this.integrationsMenuActive = false;
      this.subscriptionMenuActive = true;
      this.dataMenuActive = false;
      this.settingsMenuActive = false;
    },
    toggleData() {
      this.historyMenu = false;
      this.integrationsMenu = false;
      this.subscriptionMenu = false;
      this.dataMenu = true;
      this.settingsMenu = false;
      this.historyMenuActive = false;
      this.integrationsMenuActive = false;
      this.subscriptionMenuActive = false;
      this.dataMenuActive = true;
      this.settingsMenuActive = false;
    },
    toggleSettings() {
      this.historyMenu = false;
      this.integrationsMenu = false;
      this.subscriptionMenu = false;
      this.dataMenu = false;
      this.settingsMenu = true;
      this.historyMenuActive = false;
      this.integrationsMenuActive = false;
      this.subscriptionMenuActive = false;
      this.dataMenuActive = false;
      this.settingsMenuActive = true;
    },
  },
  components: {
    navBar,
    navFooter,
    UserChatHistory,
    UserIntegrations,
    UserSubscription,
    UserData,
    UserSettings,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div class="bodyG">
      <div v-if="session" className="accountWrapper">
        <div class="userBanner">
          <img v-bind:src="banner" />
          <img src="../assets/camera2.svg" @click="triggerBannerUpload" class="bannerCamera" />
          <input type="file" ref="bannerInput" accept="image/*" style="display:none;" @change="handleBannerUpload" />
        </div>
        <div class="profileAvatar">
          <div class="accountAvatarBackground"></div>
          <img v-if="first_name" v-bind:src="avatar" class="accountAvatar" />
          <img src="../assets/camera.svg" @click="triggerAvatarUpload" class="avatarCamera" />
          <input type="file" ref="avatarInput" accept="image/*" style="display:none;" @change="handleAvatarUpload" />
        </div>
        <div class="profilePanel">
          <div class="userDetails">
            <h2>{{ first_name }} {{ last_name }}</h2>
            <h3>{{ username }}</h3>
            <p>{{ email }}</p>
            <p>Joined: {{ joined }}</p>
            <button className="chatButton" @click="redirectToChat">
              Let's Chat
            </button>
          </div>
          <div class="aboutDetails">
            <h2>ABOUT</h2>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus
              aliquet elit augue, at feugiat leo pulvinar nec. Maecenas
              consequat, elit a ornare dignissim, justo lorem auctor lectus, et
              accumsan urna urna ac est. Phasellus convallis quam eros, et
              tincidunt mauris iaculis at. Orci varius natoque penatibus et
              magnis dis parturient montes, nascetur ridiculus mus. Vestibulum
              ultrices sodales condimentum. Fusce rutrum hendrerit dignissim.
              Aenean non nibh vestibulum, gravida lectus quis, pharetra nulla.
              Aenean blandit diam porta, ullamcorper neque quis, maximus urna.
              Vivamus purus libero, vulputate id auctor non, vestibulum et enim.
            </p>
          </div>
          <div class="editUserDetails">
            <img
              src="../assets/three-dots-vertical.svg"
              class="profileEdit"
            />
          </div>
        </div>
        <div className="accountDetailsWrapper">
          <div className="accountDetailsMenu">
            <button class="userChatHistoryMenuButton" :class="{active:historyMenuActive}" @click=this.toggleHistory>History</button>
            <button class="userIntegrationsMenuButton" :class="{active:integrationsMenuActive}" @click=this.toggleIntegrations>Integrations</button>
            <button class="userSubscriptionMenuButton" :class="{active:subscriptionMenuActive}" @click=this.toggleSubscription>Subscription</button>
            <button class="userDataMenuButton" :class="{active:dataMenuActive}" @click=this.toggleData>Data</button>
            <button class="userSettingsMenuButton" :class="{active:settingsMenuActive}" @click=this.toggleSettings>Settings</button>
          </div>
          <div className="userChatHistory">
            <UserChatHistory
              :history-menu="historyMenu"
              :integrations-menu="integrationsMenu"
              :subscription-menu="subscriptionMenu"
              :data-menu="dataMenu"
              :settings-menu="settingsMenu"
              :user-chat-history="userChatHistory"
            ></UserChatHistory>
            <UserIntegrations
              :history-menu="historyMenu"
              :integrations-menu="integrationsMenu"
              :subscription-menu="subscriptionMenu"
              :data-menu="dataMenu"
              :settings-menu="settingsMenu"
            ></UserIntegrations>
            <UserSubscription
              :history-menu="historyMenu"
              :integrations-menu="integrationsMenu"
              :subscription-menu="subscriptionMenu"
              :data-menu="dataMenu"
              :settings-menu="settingsMenu"
            ></UserSubscription>
            <UserData
              :history-menu="historyMenu"
              :integrations-menu="integrationsMenu"
              :subscription-menu="subscriptionMenu"
              :data-menu="dataMenu"
              :settings-menu="settingsMenu"
            ></UserData>
            <UserSettings
              :history-menu="historyMenu"
              :integrations-menu="integrationsMenu"
              :subscription-menu="subscriptionMenu"
              :data-menu="dataMenu"
              :settings-menu="settingsMenu"
            ></UserSettings>
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
