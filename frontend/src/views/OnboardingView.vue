<script>
import { defineComponent } from "vue";
import { mapActions, mapGetters, mapMutations } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import chatMessage from "../components/chatMessage.vue";
import ImageUpload from "../components/imageUpload.vue";
import { daypartFunc } from "../composables/daypart.js";
import { privatePanda } from "../data/chat/privatePanda.js";
import { piratePanda } from "../data/chat/piratePanda.js";
import { streetPanda } from "../data/chat/streetPanda.js";
import { pandaWeather } from "../data/chat/pandaWeather.js";
import { saveUserData } from "../composables/saveUserData.js";
import { saveUserChatHistory } from "../composables/saveUserChatHistory.js";
import { useToast } from "vue-toastification";

export default defineComponent({
  data() {
    return {
      messageToSend: "",
      chatIndex: "",
      parts: [],
      chatName: "",
    };
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
      userChatHistory: "getStoreUserChatHistory",
    }),
    ...mapGetters("chatStore", {
      inputIsVisible: "getInputIsVisible",
      imageDrop: "getImageDrop",
      daypart: "getDaypart",
      chatHistory: "getChatStoreChatHistory",
      isDisabled: "getIsDisabled",
    }),
    ...mapGetters("imageUploadStore", {
      success: "getSuccess",
      error: "getError",
    }),
    userData() {
      return {
        user_id: this.userId,
        first_name: this.first_name,
        last_name: this.last_name,
        username: this.username,
        avatar: this.avatar,
        onboarded: true,
      };
    },
    chatHistoryObject() {
      const chatHistoryObj = {
        user_id: this.userId,
        chat_script: this.chatHistory,
      };
      return chatHistoryObj;
    },
  },
  async mounted() {
    await this.getSession();
    await this.getUserInfo();
    this.setUserId(this.userId);
    this.startMessage();
    this.getDaypart();
  },
  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    ...mapMutations("chatStore", {
      setInputIsVisibleValue: "setInputIsVisible",
      setDaypartValue: "setDaypart",
      setImageDropValue: "setImageDrop",
      addToChatHistory: "setChatStoreChatHistory",
      emptyChatHistoryValues: "emptyChatHistory",
      removeFromChatHistory: "removeChatHistory",
      setIsDisabledValue: "setIsDisabled",
    }),
    ...mapMutations("userStore", {
      setUserId: "setStoreUserId",
      setFirstNameValue: "setStoreFirstName",
      setLastNameValue: "setStoreLastName",
      setUsernameValue: "setStoreUsername",
      setAvatarValue: "setStoreAvatar",
    }),
    ...mapMutations("imageUploadStore", {
      setSuccess: "setSuccess",
    }),
    getRandomChat(
      daypart = "",
      first_name = "",
      last_name = "",
      username = ""
    ) {
      const chatFunctions = [
        privatePanda,
        piratePanda,
        streetPanda,
        pandaWeather,
      ];
      if (!this.getRandomChat.previousFunction) {
        // if no previous function has been selected, select a random one
        this.chatIndex = this.getRandomChat.previousFunction =
          chatFunctions[Math.floor(Math.random() * chatFunctions.length)];
        this.parts = String(this.chatIndex).split(/\s*\(\s*/);
        const functionPrefix = "function ";
        this.chatName = this.parts[0].substring(functionPrefix.length);
      }
      const chat = this.getRandomChat.previousFunction(
        daypart,
        first_name,
        last_name,
        username
      );
      return chat;
    },
    getDaypart() {
      const dp = daypartFunc();
      this.setDaypartValue(dp);
    },
    redirectToLogin() {
      this.$router.push("/signin");
    },
    focusInput() {
      if (this.$refs.messageInput) {
        this.$refs.messageInput.focus();
      }
    },
    randomChat(chat) {
      return chat[Math.floor(Math.random() * chat.length)];
    },
    async finishOnboarding(userId) {
      const toast = useToast();
      try {
        const url =
          import.meta.env.VITE_APP_API_URL +
          "/users/set-onboarded?userId=" +
          userId;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();
        this.$router.push("/auth/" + userId + "/account");
      } catch (error) {
        toast.error(error);
      }
    },
    startMessage() {
      this.setIsDisabledValue(true);
      setTimeout(
        () => this.addToChatHistory(this.getRandomChat(this.daypart)[0]),
        1200
      );
      setTimeout(() => this.addToChatHistory(this.getRandomChat()[1]), 3200);
      setTimeout(() => this.addToChatHistory(this.getRandomChat()[2]), 5200);
      setTimeout(() => this.setIsDisabledValue(false), 5200);
      setTimeout(() => this.focusInput(), 5210);
    },
    submitMessage() {
      // Add code to send to chatBot
      this.addToChatHistory({ user: "user", message: this.messageToSend });
      if (this.first_name == "") {
        this.setIsDisabledValue(true);
        this.setFirstNameValue(this.messageToSend);
        setTimeout(
          () =>
            this.addToChatHistory(
              this.getRandomChat(this.daypart, this.first_name)[3]
            ),
          1200
        );
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[4]), 3200);
        setTimeout(() => this.setIsDisabledValue(false), 3200);
        setTimeout(() => this.focusInput(), 3210);
      } else if (this.last_name == "") {
        this.setIsDisabledValue(true);
        this.setLastNameValue(this.messageToSend);
        setTimeout(
          () =>
            this.addToChatHistory(
              this.getRandomChat(
                this.daypart,
                this.first_name,
                this.last_name
              )[5]
            ),
          1200
        );
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[6]), 3200);
        setTimeout(() => this.setIsDisabledValue(false), 3200);
        setTimeout(() => this.focusInput(), 3210);
      } else if (this.username == "") {
        this.setIsDisabledValue(true);
        this.setUsernameValue(this.messageToSend);
        setTimeout(
          () =>
            this.addToChatHistory(
              this.getRandomChat(
                this.daypart,
                this.first_name,
                this.last_name,
                this.username
              )[7]
            ),
          1200
        );
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[8]), 3200);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[9]), 7200);
        setTimeout(
          () =>
            this.addToChatHistory(
              this.getRandomChat(
                this.daypart,
                this.first_name,
                this.last_name,
                this.username
              )[10]
            ),
          9200
        );
        setTimeout(() => this.setImageDropValue("active"), 9200);
        setTimeout(() => this.setIsDisabledValue(true), 9200);
        setTimeout(() => this.focusInput(), 9210);
      } else if (this.avatar) {
        saveUserData(this.userData);
        this.removeFromChatHistory(1);
        this.setIsDisabledValue(true);
        setTimeout(
          () =>
            this.addToChatHistory(
              this.getRandomChat(
                this.daypart,
                this.first_name,
                this.last_name,
                this.username
              )[11]
            ),
          60
        );
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[12]), 3200);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[13]), 6400);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[14]), 9600);
        setTimeout(
          () => this.addToChatHistory(this.getRandomChat()[15]),
          12800
        );
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[16]), 1600);
        setTimeout(
          () => this.addToChatHistory(this.getRandomChat()[17]),
          19200
        );
        setTimeout(
          () => this.addToChatHistory(this.getRandomChat()[18]),
          22400
        );
        setTimeout(
          () => this.addToChatHistory(this.getRandomChat()[19]),
          25600
        );
        setTimeout(
          () => this.addToChatHistory(this.getRandomChat()[20]),
          28800
        );
        setTimeout(
          () => this.addToChatHistory(this.getRandomChat()[21]),
          32000
        );
        setTimeout(
          () => this.addToChatHistory(this.getRandomChat()[22]),
          35200
        );
        setTimeout(
          () => this.addToChatHistory(this.getRandomChat()[23]),
          38400
        );
        setTimeout(
          () =>
            saveUserChatHistory(
              this.chatHistoryObject.user_id,
              this.chatHistoryObject.chat_script
            ),
          3841
        );
        setTimeout(() => this.setSuccess(""), 3200);
        setTimeout(() => this.finishOnboarding(this.userId), 41600);
        setTimeout(() => this.setIsDisabledValue(false), 41600);
      }
      this.messageToSend = "";
    },
    removeMessage(chat) {
      this.removeFromChatHistory(1);
      if (this.first_name == "") {
        this.emptyChatHistoryValues();
        this.startMessage(chat);
      } else if (this.last_name == "") {
        this.setFirstNameValue("");
        this.removeFromChatHistory(2);
      } else if (this.username == "") {
        this.setLastNameValue("");
        this.removeFromChatHistory(2);
      } else {
        this.setUsernameValue("");
        this.removeFromChatHistory(4);
        this.setImageDropValue("");
        this.setIsDisabledValue(false);
      }
      this.messageToSend = "";
    },
  },
  components: {
    navBar,
    navFooter,
    chatMessage,
    ImageUpload,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div v-if="session">
      <div class="mainContainer container-fluid bg-light text-white">
        <div
          class="container pt-5 pb-5 d-flex flex-column justify-content-center align-items-center"
        >
          <div
            class="chatCard card w-100 text-bg-white text-primary text-center me-3"
          >
            <div
              class="onboardingWindow card-body scrollable-card-body d-flex flex-column-reverse text-start pt-4 pb-4 px-4"
            >
              <chatMessage
                v-for="item in chatHistory"
                :message="item"
                :class="item.user + 'Chat'"
                :key="item.user"
                :feedback-disabled="true"
                :user-id="userId"
              ></chatMessage>
            </div>
            <div class="card-footer pt-2 pt-1">
              <div class="chatBox form-floating mb-3 d-flex">
                <img v-bind:src="avatar" class="chatAvatar mt-3" />
                <textarea
                  :disabled="isDisabled"
                  class="form-control mt-3 mx-3 shadow-none"
                  v-model="messageToSend"
                  @keydown.enter.stop.prevent="submitMessage()"
                  id="userInput"
                  name="userInput"
                  placeholder="enter your message here..."
                  ref="messageInput"
                  style="min-height: 60px"
                ></textarea>
                <label
                  for="floatingTextarea"
                  class="chatPrompt text-primary mt-2"
                  style="margin-left: 75px"
                  >enter your message here...</label
                >
                <div
                  class="chatButtons d-flex align-items-center mt-3"
                  style="width: 220px"
                >
                  <button
                    :disabled="isDisabled"
                    class="btn btn-secondary btn-lg"
                    id="sendButton"
                    @click="submitMessage()"
                    style="max-height: 60px"
                  >
                    SEND
                  </button>
                  <button
                    class="btn btn-secondary btn-lg ms-3 me-2"
                    id="undoButton"
                    @click="removeMessage()"
                    style="max-height: 60px"
                  >
                    UNDO
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div v-if="imageDrop" class="w-50 text-align-center">
            <ImageUpload
              :user-id="this.userId"
              @image-uploaded.once="submitMessage()"
              :chat-name="chatName"
            ></ImageUpload>
          </div>
          <h5 v-if="success" class="text-primary text-center mt-5">
            Image uploaded successfully!
          </h5>
          <h5 v-if="error" class="text-danger text-center mt-5">
            Error uploading image, please try again.
          </h5>
        </div>
      </div>
    </div>
    <navFooter class="navFooter"></navFooter>
  </main>
</template>

<style scoped>
.chatCard {
  height: 75vh;
  max-width: 830px;
}
.onboardingWindow {
  overflow: scroll;
}
.pandaChat {
  background-color: #ffffff;
  text-align: left;
  display: flex;
  padding-right: 60px;
  flex-direction: row;
  justify-content: left;
  align-items: left;
}
.userChat {
  background-color: #ffffff;
  text-align: left;
  display: flex;
  padding-left: 60px;
  flex-direction: row-reverse;
  justify-content: right;
  align-items: right;
}
.chatAvatar {
  width: 50px;
  height: 50px;
  margin: 5px;
  margin-bottom: 12px;
  border-radius: 10px;
}
@media (max-width: 768px) {
  .chatBox {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .chatBox img {
    display: none;
  }
  .chatBox .chatPrompt {
    margin-left: 0px !important;
  }
  .chatButtons {
    margin-left: 50px;
  }
  .navFooter {
    display: none;
  }
}
</style>
