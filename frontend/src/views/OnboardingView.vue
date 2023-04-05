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

export default defineComponent({
  data() {
    return {
      messageToSend: "",
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
      chatHistory: "getChatHistory",
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
      addToChatHistory: "setChatHistory",
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
    getRandomChat(daypart = '', first_name = '', last_name = '', username = '') {
      const chatFunctions = [privatePanda, piratePanda, streetPanda, pandaWeather];
      if (!this.getRandomChat.previousFunction) {
        // if no previous function has been selected, select a random one
        this.getRandomChat.previousFunction =
          chatFunctions[Math.floor(Math.random() * chatFunctions.length)];
      }
      const chat = this.getRandomChat.previousFunction(daypart, first_name, last_name, username);
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
    goToAccount() {
      this.$router.push("/auth/" + this.userId + "/account");
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
              this.getRandomChat(this.daypart, this.first_name, this.last_name)[5]
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
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[12]), 320);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[13]), 640);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[14]), 960);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[15]), 1280);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[16]), 1600);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[17]), 1920);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[18]), 2240);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[19]), 2560);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[20]), 2880);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[21]), 3200);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[22]), 3520);
        setTimeout(() => this.addToChatHistory(this.getRandomChat()[23]), 3840);
        setTimeout(
          () =>
            saveUserChatHistory(
              this.chatHistoryObject.user_id,
              this.chatHistoryObject.chat_script
            ),
          3841
        );
        setTimeout(() => this.goToAccount(), 4160);
        setTimeout(() => this.setSuccess(""), 3200);
        setTimeout(() => this.setIsDisabledValue(false), 4160);
      }
      this.messageToSend = "";
      // Add code to update the chat history database
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
      }
      this.messageToSend = "";
      // Add code to update the chat history database
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
    <div class="bodyG">
      <div v-if="session">
        <div class="mainContainer">
          <div class="mainChatContainer">
            <div class="chatContainer" id="chatContainer">
              <chatMessage
                v-for="item in chatHistory"
                :message="item"
                :class="item.user + 'Chat'"
                :key="item.user"
              ></chatMessage>
            </div>
            <div class="userInputContainer">
              <img v-bind:src="avatar" class="chatAvatar" />
              <div class="userInput">
                <textarea
                  :disabled="isDisabled"
                  class="input"
                  v-model="messageToSend"
                  @keydown.enter.stop.prevent="submitMessage()"
                  id="userInput"
                  name="userInput"
                  placeholder="enter your message here"
                  ref="messageInput"
                ></textarea>
                <button
                  :disabled="isDisabled"
                  class="chatButton"
                  id="sendButton"
                  @click="submitMessage()"
                >
                  Send
                </button>
                <button
                  :disabled="isDisabled"
                  class="chatButton"
                  id="undoButton"
                  @click="removeMessage()"
                >
                  Undo
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-if="imageDrop">
          <ImageUpload
            :user-id="this.userId"
            @image-uploaded.once="submitMessage()"
          ></ImageUpload>
        </div>
        <h3 v-if="success">Image uploaded successfully!</h3>
        <h3 v-if="error">Error uploading image, please try again.</h3>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
<style scoped>
@import "../assets/styles/panda-main.css";
</style>
