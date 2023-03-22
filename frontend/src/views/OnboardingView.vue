<script type="text/javascript">
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import { mapActions } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import chatMessage from "../components/chatMessage.vue";
import ImageUpload from "../components/imageUpload.vue";
import { daypartFunc } from "../composables/daypart.js";
import { privatePanda } from "../data/chat/privatePanda.js";
import { saveUserData } from "../composables/saveUserData.js";
import { saveUserChatHistory } from "../composables/saveUserChatHistory.js";

export default defineComponent({
  data() {
    return {
      messageToSend: "",
    };
  },
  computed: {
    session() {
      return this.$store.state.userStore.session;
    },
    userId() {
      return this.$store.state.userStore.userId;
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
    email() {
      return this.$store.state.userStore.email;
    },
    avatar() {
      return this.$store.state.userStore.avatar;
    },
    userData() {
      return {
        user_id: this.userId,
        first_name: this.first_name,
        last_name: this.last_name,
        username: this.username,
        email: this.email,
        avatar: this.avatar,
      };
    },
    chatHistoryObject() {
      const chatHistoryObj = {
        user_id: this.userId,
        chat_script: this.chatHistory,
      };
      return chatHistoryObj;
    },
    inputIsVisible() {
      return this.$store.state.chatStore.inputIsVisible;
    },
    imageDrop() {
      return this.$store.state.chatStore.imageDrop;
    },
    daypart() {
      return this.$store.state.chatStore.daypart;
    },
    chatHistory() {
      return this.$store.state.chatStore.chatHistory;
    },
    isDisabled() {
      return this.$store.state.chatStore.isDisabled;
    },
    success() {
      return this.$store.state.imageUploadStore.success;
    },
    error() {
      return this.$store.state.imageUploadStore.error;
    },
  },
  async mounted() {
    await this.getSession();
    await this.getUserInfo();
    this.startMessage();
    this.getDaypart();
  },
  methods: {
    ...mapActions(['getSession', 'getUserInfo']),
    setInputIsVisibleValue(value) {
      this.$store.commit('setInputIsVisible', value)
    },
    setImageDropValue(value) {
      this.$store.commit('setImageDrop', value)
    },
    setAvatarValue(value) {
      this.$store.commit('setAvatar', value)
    },
    setDaypartValue(value) {
      this.$store.commit('setDaypart', value)
    },
    addToChatHistory(value) {
      this.$store.commit('setChatHistory', value)
    },
    emptyChatHistoryValues() {
      this.$store.commit('emptyChatHistory')
    },
    removeFromChatHistory(value) {
      this.$store.commit('removeChatHistory', value)
    },
    setFirstNameValue(value) {
      this.$store.commit('setFirstName', value)
    },
    setLastNameValue(value) {
      this.$store.commit('setLastName', value)
    },
    setUsernameValue(value) {
      this.$store.commit('setUsername', value)
    },
    setIsDisabledValue(value) {
      this.$store.commit('setIsDisabled', value)
    },
    setSuccess(value) {
      this.$store.commit("setSuccess", value);
    },
    getDaypart() {
      const dp = daypartFunc();
      this.setDaypartValue(dp);
    },
    redirectToLogin() {
      window.location.href = "/auth";
    },
    async onLogout() {
      await Session.signOut();
      window.location.href = "/";
    },
    focusInput() {
      if (this.$refs.messageInput) {
        this.$refs.messageInput.focus();
      }
    },
    startNewChat() {
      window.location.reload();
    },
    randomChat(chat) {
      return chat[Math.floor(Math.random() * chat.length)];
    },
    goToAccount(){
      window.location.href = "/" + this.userId + "/account";
    },
    startMessage() {
      this.setIsDisabledValue(true);
      setTimeout(() => this.addToChatHistory(privatePanda(this.daypart)[0]), 1200);
      setTimeout(() => this.addToChatHistory(privatePanda()[1]), 3200);
      setTimeout(() => this.addToChatHistory(privatePanda()[2]), 5200);
      setTimeout(() => this.setIsDisabledValue(false), 5200);
      setTimeout(() => this.focusInput(), 5210);
    },
    submitMessage() {
      // Add code to send to chatBot
      this.addToChatHistory({ user: "user", message: this.messageToSend });
      if (this.first_name == "") {
        this.setIsDisabledValue(true);
        this.setFirstNameValue(this.messageToSend);
        setTimeout(() => this.addToChatHistory(privatePanda(this.daypart, this.first_name)[3]), 1200);
        setTimeout(() => this.addToChatHistory(privatePanda()[4]), 3200);
        setTimeout(() => this.setIsDisabledValue(false), 3200);
        setTimeout(() => this.focusInput(), 3210);
      } else if (this.last_name == "") {
        this.setIsDisabledValue(true);
        this.setLastNameValue(this.messageToSend);
        setTimeout(() => this.addToChatHistory(privatePanda(this.daypart, this.first_name, this.last_name)[5]), 1200);
        setTimeout(() => this.addToChatHistory(privatePanda()[6]), 3200);
        setTimeout(() => this.setIsDisabledValue(false), 3200);
        setTimeout(() => this.focusInput(), 3210);
      } else if (this.username == "") {
        this.setIsDisabledValue(true);
        this.setUsernameValue(this.messageToSend);
        setTimeout(() => this.addToChatHistory(privatePanda(this.daypart, this.first_name, this.last_name, this.username)[7]), 1200);
        setTimeout(() => this.addToChatHistory(privatePanda()[8]), 3200);
        setTimeout(() => this.addToChatHistory(privatePanda()[9]), 7200);
        setTimeout(() => this.addToChatHistory(privatePanda(this.daypart, this.first_name, this.last_name, this.username)[10]), 9200);
        setTimeout(() => this.setImageDropValue("active"), 9200);
        setTimeout(() => this.setIsDisabledValue(true), 9200);
        setTimeout(() => this.focusInput(), 9210);
      } else if (this.avatar) {
        this.saveUserData(this.userData);
        this.removeFromChatHistory(1);
        this.setIsDisabledValue(true);
        setTimeout(() => this.addToChatHistory(privatePanda(this.daypart, this.first_name, this.last_name, this.username)[11]), 60);
        setTimeout(() => this.addToChatHistory(privatePanda()[12]), 320);
        setTimeout(() => this.addToChatHistory(privatePanda()[13]), 640);
        setTimeout(() => this.addToChatHistory(privatePanda()[14]), 960);
        setTimeout(() => this.addToChatHistory(privatePanda()[15]), 1280);
        setTimeout(() => this.addToChatHistory(privatePanda()[16]), 1600);
        setTimeout(() => this.addToChatHistory(privatePanda()[17]), 1920);
        setTimeout(() => this.addToChatHistory(privatePanda()[18]), 2240);
        setTimeout(() => this.addToChatHistory(privatePanda()[19]), 2560);
        setTimeout(() => this.addToChatHistory(privatePanda()[20]), 2880);
        setTimeout(() => this.addToChatHistory(privatePanda()[21]), 3200);
        setTimeout(() => this.addToChatHistory(privatePanda()[22]), 3520);
        setTimeout(() => this.addToChatHistory(privatePanda()[23]), 3840);
        setTimeout(() => this.saveUserChatHistory(this.chatHistoryObject), 3841);
        // setTimeout(() => this.goToAccount(), 41600);
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
    // saveUserData: async function () {
    //   try {
    //     const url = "http://localhost:3001/save-user-data/";
    //     const res = await fetch(url, {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify(this.userData),
    //     });

    //     // Check if the response status indicates an error
    //     if (!res.ok) {
    //       throw new Error(`Server responded with status ${res.status}`);
    //     }
    //   } catch (error) {
    //     // Handle the error
    //     console.log("An error occurred while saving the file:", error);
    //     this.setSuccess("");
    //   }
    // },
    // saveChatHistory: async function () {
    //   console.log(JSON.stringify(this.chatHistoryObject));
    //   try {
    //     const url = "http://localhost:3001/save-user-chat-history/";
    //     const res = await fetch(url, {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify(this.chatHistoryObject),
    //     });

    //     // Check if the response status indicates an error
    //     if (!res.ok) {
    //       throw new Error(`Server responded with status ${res.status}`);
    //     }
    //   } catch (error) {
    //     // Handle the error
    //     console.log("An error occurred while saving the file:", error);
    //     this.setSuccess("");
    //   }
    // },
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
                  :disabled='isDisabled'
                  class="input"
                  v-model="messageToSend"
                  @keydown.enter.stop.prevent="submitMessage()"
                  id="userInput"
                  name="userInput"
                  placeholder="enter your message here"
                  ref="messageInput"
                ></textarea>
                <button :disabled='isDisabled' class="chatButton" id="sendButton"  @click="submitMessage()">
                  Send
                </button>
                <button :disabled='isDisabled' class="chatButton" id="undoButton" @click="removeMessage()">
                  Undo
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-if="imageDrop">
          <ImageUpload :user-id=this.userId @image-uploaded.once="submitMessage()"></ImageUpload>
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
