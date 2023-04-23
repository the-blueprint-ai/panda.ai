<script>
import * as Session from "supertokens-web-js/recipe/session";
import { doesEmailExist } from "supertokens-web-js/recipe/thirdpartyemailpassword";
import { defineComponent } from "vue";
import { mapActions, mapGetters, mapMutations } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { getUserChatHistory } from "../composables/getUserChatHistory.js";
import { emailVerification } from "../composables/emailVerification.js";
import AccountUserChatHistory from "../components/accountUserChatHistory.vue";
import UserIntegrations from "../components/userIntegrations.vue";
import UserSubscription from "../components/userSubscription.vue";
import UserData from "../components/userData.vue";
import UserSettings from "../components/userSettings.vue";
import SpinnerComponent from "../components/spinnerComponent.vue";

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
      new_email: "",
      emailTimer: null,
      emailExistsError: "",
      emailChecking: null,
      emailOk: "",
      new_first_name: "",
      new_last_name: "",
      new_username: "",
      isDisabled: true,
    };
  },
  watch: {
    new_email(newValue) {
      // Clear the previous timer (if there was one)
      clearTimeout(this.emailTimer);

      // Start a new timer for 1000ms
      this.emailTimer = setTimeout(() => {
        this.checkEmail(newValue);
      }, 400);
    },
  },
  async mounted() {
    await this.getUserInfo();
    const { userChatHistory } = getUserChatHistory(this.$store, this.userId);
    userChatHistory(this.userId);
  },
  computed: {
    ...mapGetters("userStore", {
      session: "getStoreSession",
      userId: "getStoreUserId",
      email: "getStoreEmail",
      first_name: "getStoreFirstName",
      last_name: "getStoreLastName",
      username: "getStoreUsername",
      avatar: "getStoreAvatar",
      banner: "getStoreBanner",
      joined: "getStoreJoined",
      about: "getStoreAbout",
      onboarded: "getStoreOnboarded",
      subscriber: "getStoreSubscriber",
      admin: "getStoreAdmin",
      userStoreChatHistory: "getStoreUserChatHistory",
    }),
    isEmailValid() {
      return this.validateEmail(this.new_email);
    },
  },
  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    ...mapMutations("chatStore", {
      setIsDisabled: "setIsDisabled",
    }),
    emailVerification,
    validateEmail: function (email) {
      var re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
    checkEmail: async function (email) {
      try {
        let response = await doesEmailExist({
          email,
        });

        if (response.doesExist) {
          this.emailChecking = false;
          this.emailExistsError =
            "Email already in use. Please choose another one instead";
          this.emailOk = "no";
          setTimeout(() => {
            this.emailExistsError = "";
            this.emailOk = "";
            this.email = "";
            this.$refs.email.value = null;
            this.emailChecking = true;
          }, 3000);
        } else {
          this.emailChecking = false;
          setTimeout(() => {
            this.emailOk = "ok";
          }, 3000);
        }
      } catch (err) {
        console.error(err); // log the error to the console
        if (err.isSuperTokensGeneralError === true) {
          // this may be a custom error message sent from the API by you.
          window.alert(err.message);
        } else {
          window.alert("Oops! Something went wrong.");
        }
      }
    },
    redirectToLogin() {
      this.$router.push("/signin");
    },
    redirectToChat() {
      this.$router.push("/auth/" + this.userId + "/chat");
    },
    async onLogout() {
      await Session.signOut();
      this.$router.push("/");
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
        // Check if the image has the right dimensions (4 times wider than its height)
        const isRightDimensions = await this.checkImageDimensions(e.target.result);
        let imageFile = file;

        if (!isRightDimensions) {
          console.log("Cropping image to the right dimensions.");
          const croppedBlob = await this.cropImage(e.target.result);
          imageFile = new File([croppedBlob], file.name, { type: file.type });
        }

        this.formData.append("file", imageFile);

        // Process the uploaded image file here
        try {
          const url =
            import.meta.env.VITE_APP_API_URL +
            "/users/banner?user_id=" +
            this.userId;
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
          const updatedBannerUrl =
            jsonResponse.url + "?t=" + new Date().getTime();
          this.$store.commit("userStore/setStoreBanner", updatedBannerUrl);
        } catch (error) {
          // Handle the error
          console.error("An error occurred while saving the file:", error);
        }
      };
    },
    async checkImageDimensions(src) {
      return new Promise((resolve) => {
        const img = new Image();
        img.src = src;
        img.onload = () => {
          const width = img.width;
          const height = img.height;
          if (width === height * 4) {
            resolve(true);
          } else {
            resolve(false);
          }
        };
      });
    },
    async cropImage(src) {
      return new Promise((resolve) => {
        const img = new Image();
        img.src = src;
        img.onload = () => {
          const width = img.width;
          const height = img.height;

          // Calculate the dimensions of the cropped image
          const targetHeight = height;
          const targetWidth = targetHeight * 4;

          // Create a canvas and draw the cropped image
          const canvas = document.createElement("canvas");
          canvas.width = targetWidth;
          canvas.height = targetHeight;
          const ctx = canvas.getContext("2d");
          const startX = (width - targetWidth) / 2;
          ctx.drawImage(img, startX, 0, targetWidth, targetHeight, 0, 0, targetWidth, targetHeight);

          // Get the cropped image as a Blob
          canvas.toBlob((blob) => {
            resolve(blob);
          }, img.type);
        };
      });
    },
    async cropToSquare(img) {
      return new Promise((resolve) => {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");

        const width = img.width;
        const height = img.height;
        const size = Math.min(width, height);

        canvas.width = size;
        canvas.height = size;

        const offsetX = width > height ? (width - height) / 2 : 0;
        const offsetY = height > width ? (height - width) / 2 : 0;

        ctx.drawImage(img, offsetX, offsetY, size, size, 0, 0, size, size);
        resolve(canvas.toDataURL());
      });
    },
    dataURLToBlob: function (dataURL) {
      const binary = atob(dataURL.split(",")[1]);
      const array = [];
      for (let i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
      }
      return new Blob([new Uint8Array(array)], { type: "image/png" });
    },
    async handleAvatarUpload(event) {
      const file = event.target.files[0];
      this.formData = new FormData();
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = async (e) => {
        const img = new Image();
        img.src = e.target.result;
        img.onload = async () => {
          const croppedDataURL = await this.cropToSquare(img);
          const croppedBlob = this.dataURLToBlob(croppedDataURL);
          this.formData.append("file", croppedBlob, this.fileName);

          // Process the uploaded image file here
          try {
            const url =
              import.meta.env.VITE_APP_API_URL +
              "/users/avatar?user_id=" +
              this.userId;
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
            const updatedAvatarUrl =
              jsonResponse.url + "?t=" + new Date().getTime();
            this.$store.commit("userStore/setStoreAvatar", updatedAvatarUrl);
          } catch (error) {
            // Handle the error
            console.error("An error occurred while saving the file:", error);
          }
        };
      };
    },
    async updateUserData() {
      if (this.new_first_name !== "") {
        this.$store.commit("userStore/setStoreFirstName", this.new_first_name);
      }
      if (this.new_last_name !== "") {
        this.$store.commit("userStore/setStoreLastName", this.new_last_name);
      }
      if (this.new_username !== "") {
        this.$store.commit("userStore/setStoreUsername", this.new_username);
      }
      if (this.new_email !== "") {
        this.$store.commit("userStore/setStoreEmail", this.new_email);
      }
      try {
        const url =
          import.meta.env.VITE_APP_API_URL +
          "/users/save/?user_id=" +
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
    SpinnerComponent,
    AccountUserChatHistory,
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
    <div class="bodyGW" id="body">
      <div v-if="session" class="mobileAccountWrapper">
        <div class="mobileAccountBar">
          <img
            src="../assets/icons/chat-right-text-fill.svg"
            @click="this.toggleHistory"
          />
          <img
            src="../assets/icons/shuffle.svg"
            @click="this.toggleIntegrations"
          />
          <img
            src="../assets/icons/coin.svg"
            @click="this.toggleSubscription"
          />
          <img
            src="../assets/icons/database-fill-lock.svg"
            @click="this.toggleData"
          />
          <img
            src="../assets/icons/gear-wide-connected.svg"
            @click="this.toggleSettings"
          />
          <img
            class="mobileAccountChatButton"
            src="../assets/icons/chat-heart-fill.svg"
            @click="redirectToChat"
          />
        </div>
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
              <button class="accountChatButton" @click="redirectToChat">
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
                  <p>User ID: {{ userId }}</p>
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
                        :placeholder="'READ ONLY - ' + username"
                        type="text"
                        name="username"
                        readonly
                      />
                    </div>
                    <div class="overlayFormInput">
                      <p>Email:</p>
                      <img
                        v-if="isEmailValid && emailOk === 'ok' && email"
                        id="emailAccountGood"
                        src="../assets/icons/envelope-check-fill.svg"
                      />
                      <img
                        v-if="emailOk === 'no'"
                        id="emailAccountBad"
                        src="../assets/icons/envelope-exclamation-fill.svg"
                      />
                      <input
                        id="email"
                        ref="email"
                        v-model="new_email"
                        :placeholder="'READ ONLY - ' + email"
                        type="email"
                        name="email"
                        readonly
                      />
                    </div>
                    <div>
                      <h6
                        v-if="new_email && emailChecking"
                        style="color: black"
                      >
                        CHECKING...
                      </h6>
                      <h6 v-if="emailExistsError">{{ emailExistsError }}</h6>
                    </div>
                  </form>
                </div>
                <span class="spacer"></span>
                <div class="overlayButtons">
                  <button class="chatButton" @click="updateUserData()">
                    Save
                  </button>
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
                @click="this.toggleData()"
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
              <AccountUserChatHistory
                :history-menu="historyMenu"
                :integrations-menu="integrationsMenu"
                :subscription-menu="subscriptionMenu"
                :data-menu="dataMenu"
                :settings-menu="settingsMenu"
                :user-chat-history="userStoreChatHistory"
                :is-disabled="this.isDisabled"
              ></AccountUserChatHistory>
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
                :user-id="userId"
              ></UserData>
              <UserSettings
                :history-menu="historyMenu"
                :integrations-menu="integrationsMenu"
                :subscription-menu="subscriptionMenu"
                :data-menu="dataMenu"
                :settings-menu="settingsMenu"
                :user-id="this.userId"
                :email="this.email"
              ></UserSettings>
            </div>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
