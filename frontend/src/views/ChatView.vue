<script>
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import chatMessage from "../components/chatMessage.vue";
import { daypartFunc } from "../components/daypart.js";
import ImageUpload from "../components/imageUpload.vue";

export default defineComponent({
  data() {
    return {
      session: false,
      userId: "",
      messageToSend: "",
    };
  },
  computed: {
    inputIsVisible() {
      return this.$store.state.chatStore.inputIsVisible;
    },
    imageDrop() {
      return this.$store.state.chatStore.imageDrop;
    },
    avatar() {
      return this.$store.state.userStore.avatar;
    },
    daypart() {
      return this.$store.state.chatStore.daypart;
    },
    chatHistory() {
      return this.$store.state.chatStore.chatHistory;
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
    isDisabled() {
      return this.$store.state.chatStore.isDisabled;
    },
  },
  mounted() {
    this.getUserInfo();
    this.startMessage();
    this.getDaypart();
  },
  methods: {
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
    getDaypart() {
      const dp = daypartFunc();
      this.setDaypartValue(dp);
    },
    redirectToLogin() {
      window.location.href = "/auth";
    },
    async getUserInfo() {
      this.session = await Session.doesSessionExist();
      if (this.session) {
        this.userId = await Session.getUserId();
      }
    },
    async onLogout() {
      await Session.signOut();
      window.location.href = "/";
    },
    focusInput() {
      this.$refs.messageInput.focus();
    },
    startNewChat() {
      window.location.reload();
    },
    submitMessage() {
      // Add code to send to chatBot
      this.addToChatHistory({ user: "user", message: this.messageToSend });
      if (this.first_name == "") {
        this.setIsDisabledValue(true);
        this.setFirstNameValue(this.messageToSend);
        setTimeout(() => this.addToChatHistory({ user: "panda", message: "What is your major malfunction Private " + this.first_name + "?!😳" }), 1200);
        setTimeout(() => this.addToChatHistory({ user: "panda", message: "We don't use first names at Panda Bootcamp! I meant, what’s your SURNAME Private?! 🫡" }), 3200);
        setTimeout(() => this.setIsDisabledValue(false), 3200);
        setTimeout(() => this.focusInput(), 3210);
      } else if (this.last_name == "") {
        this.setIsDisabledValue(true);
        this.setLastNameValue(this.messageToSend);
        setTimeout(() => this.addToChatHistory({ user: "panda", message: "Ok, Private " + this.last_name + ". We’re going to have to pick this up a bit if you’re to make it through Panda Bootcamp.⛺️" }), 1200);
        setTimeout(() => this.addToChatHistory({ user: "panda", message: "What would you like your CODENAME to be here at Panda Bootcamp? 🥸" }), 3200);
        setTimeout(() => this.setIsDisabledValue(false), 3200);
        setTimeout(() => this.focusInput(), 3210);
      } else if (this.username == "") {
        this.setIsDisabledValue(true);
        this.setUsernameValue(this.messageToSend);
        setTimeout(() => this.addToChatHistory({ user: "panda", message: "That’s more like it! Right then Private " + this.username + "! If it ain't raining, we ain't training - move out!🌧️" }), 1200);
        setTimeout(() => this.addToChatHistory({ user: "panda", message: "Everywhere we go-oh... Everywhere we go-oh… People wanna know-oh… Who we are… Where we come from… So we tell them… We are Pandas!… Mighty mighty Pandas!📣" }), 3200);
        setTimeout(() => this.addToChatHistory({ user: "panda", message: "I can’t hear you, sound off like you’ve got a pair!🥜" }), 7200);
        setTimeout(() => this.addToChatHistory({ user: "panda", message: "Ok, let me get a good look at you Private " + this.username + "! Upload a photo of yourself by dropping it below… 📸" }), 9200);
        setTimeout(() => this.setImageDropValue("active"), 9200);
        setTimeout(() => this.setIsDisabledValue(false), 9200);
        setTimeout(() => this.focusInput(), 9210);
      }
      this.messageToSend = "";
      // Add code to update the chat history database
    },
    removeMessage() {
      this.removeFromChatHistory(1);
      if (this.first_name == "") {
        this.emptyChatHistoryValues();
        this.startMessage();
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
    startMessage() {
      this.setIsDisabledValue(true);
      setTimeout(() => this.addToChatHistory({ user: "panda", message: "Good " + this.daypart + " Private!🫡" }), 1200);
      setTimeout(() => this.addToChatHistory({ user: "panda", message: "Welcome to Panda Bootcamp!⛺️" }), 3200);
      setTimeout(() => this.addToChatHistory({ user: "panda", message: "What’s your FIRST NAME Private? 🫡" }), 5200);
      setTimeout(() => this.setIsDisabledValue(false), 5200);
      setTimeout(() => this.focusInput(), 5210);
    },
  },
  components: {
    navBar,
    chatMessage,
    ImageUpload,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div className="body">
      <div v-if="session">
        <div className="mainContainer">
          <div className="chatHistoryContainer">
            <h2>Chat History</h2>
            <div className="chatHistory">
              <p className="history">+ Today</p>
              <p className="history">+ Yesterday</p>
              <p className="history">+ Day before</p>
              <p className="history">+ Day before that</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ scroll...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
            </div>
            <button :disabled='isDisabled' className="startNewChat" @click="startNewChat">
              Start new chat
            </button>
          </div>
          <div className="mainChatContainer">
            <div className="chatContainer" id="chatContainer">
              <chatMessage
                v-for="item in chatHistory"
                :message="item"
                :class="item.user + 'Chat'"
                :key="item.user"
              ></chatMessage>
            </div>
            <div className="userInputContainer">
              <img v-bind:src="avatar" class="avatar" />
              <div className="userInput">
                <textarea
                  :disabled='isDisabled'
                  className="input"
                  v-model="messageToSend"
                  @keydown.enter.stop.prevent="submitMessage"
                  id="userInput"
                  name="userInput"
                  placeholder="enter your message here"
                  ref="messageInput"
                ></textarea>
                <button :disabled='isDisabled' className="chatButton" id="sendButton"  @click="submitMessage">
                  Send
                </button>
                <button :disabled='isDisabled' className="chatButton" id="undoButton" @click="removeMessage">
                  Undo
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-if="imageDrop">
          <ImageUpload></ImageUpload>
        </div>
      </div>
    </div>
  </main>
</template>
<style scoped>
@import "../assets/styles/panda-main.css";
</style>
