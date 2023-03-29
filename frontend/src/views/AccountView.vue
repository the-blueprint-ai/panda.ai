<script>
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import { mapActions } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { getUserData } from "../composables/getUserData.js";
import { getUserChatHistory } from "../composables/getUserChatHistory.js";
import UserChatHistory from "../components/userChatHistory.vue";
import UserIntegrations from "../components/userIntegrations.vue";
import UserSubscription from "../components/userSubscription.vue";
import UserData from "../components/userData.vue";
import UserSettings from "../components/userSettings.vue";

export default defineComponent({
  data() {
    return {
      overlay: false,
      opened: false,
      visible: false,
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
      formData: null,
      usernames: [],
      emails: [],
      new_first_name: "",
      new_last_name: "",
      new_username: "",
      new_email: "",
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
    about() {
      return this.$store.state.userStore.about;
    },
    onboarded() {
      return this.$store.state.userStore.onboarded;
    },
    subscriber() {
      return this.$store.state.userStore.subscriber;
    },
    admin() {
      return this.$store.state.userStore.admin;
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
    const { userData } = getUserData(this.userId, this.$store);
    userData(this.userId);
    const { userChatHistory } = getUserChatHistory(this.userId, this.$store);
    userChatHistory(this.userId);
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
    triggerBannerUpload() {
      this.$refs.bannerInput.click();
    },
    triggerAvatarUpload() {
      this.$refs.avatarInput.click();
    },
    async handleBannerUpload(event) {
      const file = event.target.files[0];
      this.formData = new FormData();
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = async (e) => {
        this.formData.append("file", file);

        // Process the uploaded image file here
        try {
          const url =
            import.meta.env.VITE_APP_API_URL + "/users/banner/?user_id=" + this.userId;
          const res = await fetch(url, {
            method: "POST",
            body: this.formData,
          });

          // Check if the response status indicates an error
          if (!res.ok) {
            const errorResponse = await res.json();
            console.error("Server error response:", errorResponse);
            throw new Error(`Server responded with status ${res.status}`);
          }

          // Parse the JSON response
          const jsonResponse = await res.json();
          this.setBanner(jsonResponse.url);
        } catch (error) {
          // Handle the error
          console.error("An error occurred while saving the file:", error);
        }
      };
    },
    async handleAvatarUpload(event) {
      const file = event.target.files[0];
      this.formData = new FormData();
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = async (e) => {
        this.formData.append("file", file);

        // Process the uploaded image file here
        try {
          const url =
            import.meta.env.VITE_APP_API_URL + "/users/avatar/?user_id=" + this.userId;
          const res = await fetch(url, {
            method: "POST",
            body: this.formData,
          });

          // Check if the response status indicates an error
          if (!res.ok) {
            const errorResponse = await res.json();
            console.error("Server error response:", errorResponse);
            throw new Error(`Server responded with status ${res.status}`);
          }

          // Parse the JSON response
          const jsonResponse = await res.json();
          this.setAvatar(jsonResponse.url);
        } catch (error) {
          // Handle the error
          console.error("An error occurred while saving the file:", error);
        }
      };
    },
    async updateUserData() {
      if (this.new_first_name !== "") {
        this.setFirstName(this.new_first_name);
      }
      if (this.new_last_name !== "") {
        this.setLastName(this.new_last_name);
      }
      if (this.new_username !== "") {
        this.setUsername(this.new_username);
      }
      if (this.new_email !== "") {
        this.setEmail(this.new_email);
      }
      try {
        const url =
          import.meta.env.VITE_APP_API_URL + "/users/save/?user_id=" +
          this.userId +
          "&first_name=" +
          this.first_name +
          "&last_name=" +
          this.last_name +
          "&username=" +
          this.username +
          "&email=" +
          this.email;
        const res = await fetch(url, {
          method: "POST",
        });

        this.overlay = !this.overlay;
        // Check if the response status indicates an error
        if (!res.ok) {
          const errorResponse = await res.json();
          console.error("Server error response:", errorResponse);
          throw new Error(`Server responded with status ${res.status}`);
        }
      } catch (error) {
        // Handle the error
        console.error("An error occurred while saving the file:", error);
      }
    },
    activateOverlay() {
      this.overlay = !this.overlay;
      this.focusInput();
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
      <div v-if="session" class="accountWrapper">
        <div class="userBanner">
          <img v-if="banner" v-bind:src="banner" />
          <img v-else src="../assets/banner.png" />
          <img
            src="../assets/icons/camera2.svg"
            @click="triggerBannerUpload"
            class="bannerCamera"
          />
          <input
            type="file"
            ref="bannerInput"
            accept="image/*"
            style="display: none"
            @change="handleBannerUpload"
          />
        </div>
        <div class="profileAvatar">
          <div class="accountAvatarBackground"></div>
          <img v-if="avatar" v-bind:src="avatar" class="accountAvatar" />
          <img v-else src="../assets/user.png" class="accountAvatar" />
          <img
            src="../assets/icons/camera.svg"
            @click="triggerAvatarUpload"
            class="avatarCamera"
          />
          <input
            type="file"
            ref="avatarInput"
            accept="image/*"
            style="display: none"
            @change="handleAvatarUpload"
          />
        </div>
        <div class="profilePanel">
          <div class="userDetails">
            <h2>{{ first_name }} {{ last_name }}</h2>
            <h3>{{ username }}</h3>
            <p>{{ email }}</p>
            <p v-if="joined">Joined: {{ joined }}</p>
            <button class="chatButton" @click="redirectToChat">
              Let's Chat
            </button>
          </div>
          <div v-if="about" class="aboutDetails">
            <h2>ABOUT</h2>
            <p>{{ about }}</p>
          </div>
          <div id="overlay" class="overlay" :class="{ active: overlay }">
            <div class="overlayContent">
              <img
                src="../assets/icons/x.svg"
                class="overlayCloseButton"
                @click="activateOverlay"
              />
              <div class="overlayTitle">
                <h2>Edit Your Details</h2>
                <p>User ID: {{ this.userId }}</p>
              </div>
              <div class="overlayForm">
                <form>
                  <div class="overlayFormInput">
                    <p>First Name:</p>
                    <input
                      id="firstName"
                      v-model="new_first_name"
                      :placeholder="first_name"
                      type="text"
                      name="firstName"
                    />
                  </div>
                  <div class="overlayFormInput">
                    <p>Last Name:</p>
                    <input
                      id="lastName"
                      v-model="new_last_name"
                      :placeholder="last_name"
                      type="text"
                      name="lastName"
                    />
                  </div>
                  <div class="overlayFormInput">
                    <p>Username:</p>
                    <input
                      id="username"
                      v-model="new_username"
                      :placeholder="username"
                      type="text"
                      name="username"
                    />
                  </div>
                  <div class="overlayFormInput">
                    <p>Email:</p>
                    <input
                      id="email"
                      v-model="new_email"
                      :placeholder="email"
                      type="email"
                      name="email"
                    />
                  </div>
                </form>
              </div>
              <div class="overlayButtons">
                <button class="chatButton" @click="updateUserData()">Save</button>
              </div>
            </div>
          </div>
          <div class="editUserDetails">
            <img
              src="../assets/icons/three-dots-vertical.svg"
              class="profileEdit"
              @click="activateOverlay"
            />
          </div>
        </div>
        <div class="accountDetailsWrapper">
          <div class="accountDetailsMenu">
            <button
              class="userChatHistoryMenuButton"
              :class="{ active: historyMenuActive }"
              @click="this.toggleHistory"
            >
              Chat History
            </button>
            <button
              class="userIntegrationsMenuButton"
              :class="{ active: integrationsMenuActive }"
              @click="this.toggleIntegrations"
            >
              Integrations
            </button>
            <button
              class="userSubscriptionMenuButton"
              :class="{ active: subscriptionMenuActive }"
              @click="this.toggleSubscription"
            >
              Subscription
            </button>
            <button
              class="userDataMenuButton"
              :class="{ active: dataMenuActive }"
              @click="this.toggleData"
            >
              Data
            </button>
            <button
              class="userSettingsMenuButton"
              :class="{ active: settingsMenuActive }"
              @click="this.toggleSettings"
            >
              Settings
            </button>
          </div>
          <div class="userChatHistory">
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
</style>
