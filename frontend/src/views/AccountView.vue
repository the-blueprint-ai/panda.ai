<script>
import * as Session from "supertokens-web-js/recipe/session";
import { doesEmailExist } from "supertokens-web-js/recipe/thirdpartyemailpassword";
import { doesUsernameExist } from "../composables/doesUsernameExist.js";
import { defineComponent } from "vue";
import { mapActions, mapGetters, mapMutations } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { getUserChatHistory } from "../composables/getUserChatHistory.js";
import { getIntegrations } from "../composables/getIntegrations.js";
import { getIntegrationsList } from "../composables/getIntegrationsList.js";
import AccountUserChatHistory from "../components/accountUserChatHistory.vue";
import UserIntegrations from "../components/userIntegrations.vue";
import UserSubscription from "../components/userSubscription.vue";
import UserData from "../components/userData.vue";
import UserSettings from "../components/userSettings.vue";
import SpinnerComponent from "../components/spinnerComponent.vue";
import { useToast } from "vue-toastification";

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
      emailTimer: null,
      usernameTimer: null,
      emailExistsError: "",
      usernameExistsError: "",
      new_first_name: "",
      new_last_name: "",
      new_username: "",
      new_email: "",
      isDisabled: true,
      saveDetailsButtonText: "SAVE DETAILS",
      detailsUpdated: false,
      formSubmitted: false,
      loading: false,
      selectedOption: null,
      accountDataOptions: [
        { text: "Chat History", value: "chatHistory" },
        { text: "Integrations", value: "integrations" },
        { text: "Subscription", value: "subscription" },
        { text: "Data", value: "data" },
        { text: "Settings", value: "settings" },
      ],
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
    new_username(newValue) {
      // Clear the previous timer (if there was one)
      clearTimeout(this.usernameTimer);

      // Start a new timer for 1000ms
      this.usernameTimer = setTimeout(() => {
        this.checkUsername(newValue);
      }, 400);
    },
  },
  async mounted() {
    if (!this.userId) {
      await this.getUserInfo();
    }
    const { userChatHistory } = getUserChatHistory(this.$store, this.userId);
    userChatHistory(this.userId);
    const { integrations } = getIntegrations(this.$store, this.userId);
    integrations(this.userId);
    const { integrationsList } = getIntegrationsList(this.$store, this.userId);
    integrationsList(this.userId);
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
      subscribed: "getStoreSubscribed",
      integrations: "getStoreIntegrations",
      messagesPerMonth: "getStoreMessagesPerMonth",
      subscriberID: "getStoreSubscriberID",
      planID: "getStorePlanID",
      userStoreChatHistory: "getStoreUserChatHistory",
      currentIntegrations: "getStoreCurrentIntegrations",
    }),
    isEmailValid() {
      return this.validateEmail(this.new_email);
    },
    isUsernameValid() {
      return !this.usernameExistsError;
    },
  },
  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    ...mapMutations("chatStore", {
      setIsDisabled: "setIsDisabled",
    }),
    validateEmail: function (email) {
      var re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
    checkEmail: async function (email) {
      const toast = useToast();
      try {
        let response = await doesEmailExist({
          email,
        });

        if (response.doesExist) {
          toast.warning(
            "Email already registered. Please choose another one instead."
          );
          this.emailExistsError =
            "Email already registered. Please choose another one instead.";
          setTimeout(() => {
            this.emailExistsError = "";
            this.new_email = "";
          }, 3600);
        }
      } catch (err) {
        toast.error(err);
        if (err.isSuperTokensGeneralError === true) {
          // this may be a custom error message sent from the API by you.
          toast.error(`Server responded with status ${err.message}`);
        } else {
          toast.error("Oops! Something went wrong. Please try again.");
        }
      }
    },
    checkUsername: async function (username) {
      try {
        let response = await doesUsernameExist(username);

        if (response) {
          toast.warning(
            "Username already registered. Please choose another one instead."
          );
          this.usernameExistsError =
            "Username already registered. Please choose another one instead.";
          setTimeout(() => {
            this.usernameExistsError = "";
            this.new_username = "";
          }, 3600);
        }
      } catch (err) {
        toast.error(err);
        if (err.isSuperTokensGeneralError === true) {
          // this may be a custom error message sent from the API by you.
          toast.error(`Server responded with status ${err.message}`);
        } else {
          toast.error("Oops! Something went wrong. Please try again.");
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
      const toast = useToast();
      const file = event.target.files[0];
      this.formData = new FormData();
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = async (e) => {
        // Check if the image has the right dimensions (4 times wider than its height)
        const isRightDimensions = await this.checkImageDimensions(
          e.target.result
        );
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
            toast.error("Server error response:", errorResponse);
            toast.error(`Server responded with status ${res.status}`);
          }

          // Parse the JSON response
          const jsonResponse = await res.json();
          const updatedBannerUrl =
            jsonResponse.url + "?t=" + new Date().getTime();
          this.$store.commit("userStore/setStoreBanner", updatedBannerUrl);
          toast.success("Banner updated successfully!");
        } catch (error) {
          // Handle the error
          toast.error("An error occurred while saving the file:", error);
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
          ctx.drawImage(
            img,
            startX,
            0,
            targetWidth,
            targetHeight,
            0,
            0,
            targetWidth,
            targetHeight
          );

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
      const toast = useToast();
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
              toast.error("Server error response:", errorResponse);
              toast.error(`Server responded with status ${res.status}`);
            }

            // Parse the JSON response
            const jsonResponse = await res.json();
            const updatedAvatarUrl =
              jsonResponse.url + "?t=" + new Date().getTime();
            this.$store.commit("userStore/setStoreAvatar", updatedAvatarUrl);
            toast.success("Avatar updated successfully!");
          } catch (error) {
            // Handle the error
            toast.error("An error occurred while saving the file:", error);
          }
        };
      };
    },
    async updateUserData() {
      this.loading = true;
      const toast = useToast();

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

        const url2 =
          import.meta.env.VITE_APP_API_URL +
          "/users/change-email?user_id=" +
          this.userId +
          "&new_email=" +
          this.email;
        const res2 = await fetch(url2, {
          method: "POST",
        });

        // Check if the response status indicates an error
        if (!res.ok || !res2.ok) {
          const errorResponse = await res.json();
          toast.error("Server error response:", errorResponse);
          toast.error(`Server responded with status ${res.status}`);
        } else {
          this.loading = false;
          this.saveDetailsButtonText = "SAVED!";
          toast.success("Details updated!");
          setTimeout(() => {
            this.saveDetailsButtonText = "SAVE DETAILS";
            this.detailsUpdated = true;
          }, 1200);
        }
      } catch (error) {
        // Handle the error
        toast.error("An error occurred while saving the file:", error);
      }
    },
    closeModal() {
      this.detailsUpdated = false;
    },
    activateOverlay() {
      this.overlay = !this.overlay;
    },
    onOptionChange(event) {
      const option = event.target.value;
      switch (option) {
        case "chatHistory":
          this.toggleHistory();
          break;
        case "integrations":
          this.toggleIntegrations();
          break;
        case "subscription":
          this.toggleSubscription();
          break;
        case "data":
          this.toggleData();
          break;
        case "settings":
          this.toggleSettings();
          break;
      }
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
    <div v-if="session">
      <div class="mainContainer container-fluid bg-light text-white">
        <div class="container d-flex flex-column pt-4 pb-5">
          <div
            v-if="userStoreChatHistory"
            class="card text-bg-white text-primary text-center"
          >
            <img v-if="banner" v-bind:src="banner" class="card-img-top" />
            <img v-else src="../assets/banner.png" class="card-img-top" />
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
            <div
              class="card-body text-start d-flex justify-content-between pt-4 pb-4 px-4"
            >
              <div class="profile d-flex">
                <div class="profileLeft">
                  <div class="accountAvatarBackground"></div>
                  <img
                    v-if="avatar"
                    v-bind:src="avatar"
                    class="accountAvatar"
                  />
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
                  <div class="profileDetails">
                    <div class="d-flex flex-row align-items-center">
                      <h2 class="card-title" style="margin-top: 30px">
                        {{ first_name }} {{ last_name }}
                      </h2>
                      <img
                        v-if="subscriber"
                        class="subscriberCheck mb-1 ms-2"
                        src="../assets/icons/patch-check-fill.svg"
                        style="width: 25px"
                      />
                    </div>
                    <h5 class="card-subtitle mb-2 text-muted">
                      {{ username }}
                    </h5>
                    <p class="mt-4">{{ email }}</p>
                    <p class="mt-n3" v-if="joined">Joined: {{ joined }}</p>
                  </div>
                  <button
                    class="btn btn-secondary btn-lg ms-4"
                    @click="redirectToChat"
                    style="width: 170px"
                  >
                    Let's Chat
                  </button>
                </div>
                <div v-if="about.length > 0" class="about ms-5">
                  <h2>ABOUT</h2>
                  <p>{{ about }}</p>
                </div>
              </div>
              <div
                class="edit ms-5 me-5"
                data-bs-toggle="modal"
                data-bs-target="#userDetailsModal"
              >
                <img
                  src="../assets/icons/three-dots-vertical.svg"
                  class="profileEdit"
                  style="cursor: pointer"
                />
              </div>
              <div
                class="modal fade"
                id="userDetailsModal"
                tabindex="-1"
                aria-labelledby="userDetailsModalLabel"
                aria-hidden="true"
              >
                <div class="modal-dialog modal-dialog-centered">
                  <div class="modal-content">
                    <div
                      class="modal-header d-inline-flex flex-column align-items-start w-100"
                    >
                      <div class="d-flex flex-row align-items-start w-100">
                        <h4 class="modal-title" id="userDetailsModalLabel">
                          EDIT YOUR DETAILS
                        </h4>
                        <button
                          type="button"
                          class="btn-close"
                          data-bs-dismiss="modal"
                          aria-label="Close"
                        ></button>
                      </div>
                      <p class="text-start mt-n1 mb-0" style="font-size: 12px">
                        {{ this.userId }}
                      </p>
                    </div>
                    <div class="modal-body text-center">
                      <h1>🐼</h1>
                      <p>To edit your details, please update them below:</p>
                      <p class="ms-1 mb-n4 text-start">First Name:</p>
                      <div class="form-floating mb-2">
                        <input
                          type="text"
                          name="first_name"
                          class="form-control mt-4"
                          id="first_name"
                          v-model="new_first_name"
                          :placeholder="first_name"
                        />
                        <label for="floatingInput">{{ first_name }}</label>
                      </div>
                      <p class="ms-1 mb-n4 text-start">Last Name:</p>
                      <div class="form-floating mb-2">
                        <input
                          type="text"
                          name="last_name"
                          class="form-control mt-4"
                          id="last_name"
                          v-model="new_last_name"
                          :placeholder="last_name"
                        />
                        <label for="floatingInput">{{ last_name }}</label>
                      </div>
                      <p class="ms-1 mb-n4 text-start">Username:</p>
                      <div class="form-floating mb-2">
                        <input
                          type="text"
                          name="username"
                          class="form-control mt-4"
                          id="username"
                          v-model="new_username"
                          :placeholder="username"
                          :class="{
                            'is-valid':
                              this.new_username.length > 0 &&
                              !usernameExistsError,
                            'is-invalid': usernameExistsError,
                          }"
                        />
                        <label for="floatingInput">{{ username }}</label>
                        <div class="valid-feedback">🐼 Looks good!</div>
                        <div
                          v-if="usernameExistsError"
                          class="invalid-feedback text-danger"
                        >
                          {{ this.usernameExistsError }}
                        </div>
                      </div>
                      <p class="ms-1 mb-n4 text-start">Email:</p>
                      <div class="form-floating mb-2">
                        <input
                          type="email"
                          name="email"
                          class="form-control mt-4"
                          id="email"
                          v-model="new_email"
                          :placeholder="email"
                          autocomplete="email"
                          :class="{
                            'is-valid':
                              this.new_email.length > 0 && !emailExistsError,
                            'is-invalid': emailExistsError,
                          }"
                        />
                        <label for="floatingInput">{{ email }}</label>
                        <div class="valid-feedback">🐼 Looks good!</div>
                        <div
                          v-if="emailExistsError"
                          class="invalid-feedback text-danger"
                        >
                          {{ this.emailExistsError }}
                        </div>
                        <div
                          id="validationServerUsernameFeedback"
                          class="invalid-feedback"
                        >
                          Please enter a valid email address.
                        </div>
                      </div>
                    </div>
                    <div class="modal-footer">
                      <button
                        v-if="!this.detailsUpdated"
                        @click="updateUserData()"
                        type="button"
                        class="btn btn-secondary d-flex justify-content-center"
                        style="width: 130px"
                        :disabled="
                          emailExistsError.length > 0 ||
                          usernameExistsError.length > 0
                        "
                      >
                        <SpinnerComponent
                          :loading="this.loading"
                          :button-text="this.saveDetailsButtonText"
                        ></SpinnerComponent>
                      </button>
                      <button
                        v-else
                        class="btn btn-danger d-flex justify-content-center"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                        @click="closeModal()"
                        style="width: 130px"
                      >
                        CLOSE
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div
            v-if="userStoreChatHistory"
            class="card text-bg-white text-primary mt-4"
          >
            <div class="card-header">
              <div
                class="accountCardTitles d-flex justify-content-around pt-3 pb-2"
              >
                <h4
                  class="userChatHistoryMenuButton"
                  :class="{ active: historyMenuActive }"
                  @click="this.toggleHistory"
                  style="cursor: pointer"
                >
                  CHAT HISTORY
                </h4>
                <h4
                  class="userIntegrationsMenuButton"
                  :class="{ active: integrationsMenuActive }"
                  @click="this.toggleIntegrations"
                  style="cursor: pointer"
                >
                  INTEGRATIONS
                </h4>
                <h4
                  class="userSubscriptionMenuButton"
                  :class="{ active: subscriptionMenuActive }"
                  @click="this.toggleSubscription"
                  style="cursor: pointer"
                >
                  SUBSCRIPTION
                </h4>
                <h4
                  class="userDataMenuButton"
                  :class="{ active: dataMenuActive }"
                  @click="this.toggleData()"
                  style="cursor: pointer"
                >
                  DATA
                </h4>
                <h4
                  class="userSettingsMenuButton"
                  :class="{ active: settingsMenuActive }"
                  @click="this.toggleSettings"
                  style="cursor: pointer"
                >
                  SETTINGS
                </h4>
              </div>
              <div class="accountCardSelector">
                <select
                  v-model="selectedOption"
                  class="form-select mb-2"
                  @change="onOptionChange"
                >
                  <option
                    v-for="accountDataOption in accountDataOptions"
                    :key="accountDataOption.value"
                    :value="accountDataOption.value"
                  >
                    {{ accountDataOption.text }}
                  </option>
                </select>
              </div>
            </div>
            <div class="card-body scrollable-card-body text-start">
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
                :integrations="integrations"
              ></UserIntegrations>
              <UserSubscription
                :history-menu="historyMenu"
                :integrations-menu="integrationsMenu"
                :subscription-menu="subscriptionMenu"
                :data-menu="dataMenu"
                :settings-menu="settingsMenu"
                :email="email"
                :subscriber="subscriber"
                :subscribed="subscribed"
                :integrations="integrations"
                :messages-per-month="messagesPerMonth"
                :planID="planID"
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

<style scoped>
.bannerCamera {
  width: 100%;
  opacity: 0;
  position: absolute;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  transition: 1s ease;
}
.bannerCamera:hover {
  transition-delay: 0.3s;
  opacity: 1;
  cursor: pointer;
}
.avatarCamera {
  width: 186px;
  margin-top: -193px;
  margin-left: 17px;
  opacity: 0;
  position: absolute;
  border-radius: 40px;
  transition: 1s ease;
}
.avatarCamera:hover {
  transition-delay: 0.3s;
  opacity: 1;
  cursor: pointer;
}
.accountAvatarBackground {
  display: flex;
  height: 200px;
  width: 200px;
  border-radius: 50px;
  background-color: #ffffff;
  border: 7px solid #ffffff;
  align-items: start;
  position: relative;
  margin-top: -115px;
  margin-left: 10px;
}
.accountAvatar {
  display: flex;
  height: 200px;
  width: 200px;
  border-radius: 50px;
  background-color: #ffffff;
  border: 7px solid #ffffff;
  align-items: start;
  position: relative;
  margin-top: -205px;
  margin-left: 10px;
}
.subscriberCheck {
  z-index: 200;
}
.profileDetails {
  margin-top: -30px;
  margin-left: 40px;
}
.profileEdit {
  width: 30px;
}
.accountCardSelector {
  display: none;
}
.scrollable-card-body {
  height: 900px;
  overflow-y: auto;
}
h4.userChatHistoryMenuButton:hover,
h4.userIntegrationsMenuButton:hover,
h4.userSubscriptionMenuButton:hover,
h4.userDataMenuButton:hover,
h4.userSettingsMenuButton:hover {
  background-image: linear-gradient(to right, #ffcb4c 100%, transparent 0%);
  background-position-y: 26px;
  background-repeat: repeat-x;
  background-size: 1px 5px;
}
h4.userChatHistoryMenuButton.active,
h4.userIntegrationsMenuButton.active,
h4.userSubscriptionMenuButton.active,
h4.userDataMenuButton.active,
h4.userSettingsMenuButton.active {
  background-image: linear-gradient(to right, #ffcb4c 100%, transparent 0%);
  background-position-y: 26px;
  background-repeat: repeat-x;
  background-size: 1px 5px;
}
@media (max-width: 992px) {
  .card-header h4 {
    font-size: 18px;
  }
}
@media (max-width: 768px) {
  .card-header h4 {
    font-size: 16px;
  }
  .about {
    display: none;
  }
}
@media (max-width: 576px) {
  .accountCardTitles {
    display: none !important;
  }
  .accountCardSelector {
    width: 100%;
    display: block;
    margin-top: 10px;
  }
}
</style>
