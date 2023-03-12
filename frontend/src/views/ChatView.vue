<script lang="ts">
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import chatMessage from "../components/chatMessage.vue";
import { daypart } from "../components/daypart.js";

export default defineComponent({
  data() {
    return {
      session: false,
      userId: "",
      messageToSend: "",
      daypart: "",
      chatHistory: [],
      first_name: "",
      last_name: "",
      username: "",
      isDisabled: false,
    };
  },
  mounted() {
    this.getUserInfo();
    this.startMessage();
  },
  methods: {
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
      window.location.href = "/"
    },
    startNewChat() {
      window.location.reload();
    },
    submitMessage() {
      // Add code to send to chatBot
      this.chatHistory.unshift({ user: "user", message: this.messageToSend });
      if (this.first_name == "") {
        this.isDisabled = true;
        this.first_name = this.messageToSend;
        setTimeout(() => this.chatHistory.unshift({ user: "panda", message: "What is your major malfunction Private " + this.first_name + "?!😳" }), 1200);
        setTimeout(() => this.chatHistory.unshift({ user: "panda", message: "We don't use first names at Panda Bootcamp! I meant, what’s your SURNAME Private?! 🫡" }), 3200);
        setTimeout(() => this.isDisabled = false, 3200);
      } else if (this.last_name =="") {
        this.isDisabled = true;
        this.last_name = this.messageToSend;
        setTimeout(() => this.chatHistory.unshift({ user: "panda", message: "Ok, Private " + this.last_name + ". We’re going to have to pick this up a bit if you’re to make it through Panda Bootcamp.⛺️" }), 1200);
        setTimeout(() => this.chatHistory.unshift({ user: "panda", message: "What would you like your CODENAME to be here at Panda Bootcamp? 🥸" }), 3200);
        setTimeout(() => this.isDisabled = false, 3200);
      } else if (this.username =="") {
        this.isDisabled = true;
        this.username = this.messageToSend;
        setTimeout(() => this.chatHistory.unshift({ user: "panda", message: "That’s more like it! Right then Private " + this.username + "! If it ain't raining, we ain't training - move out!🌧️" }), 1200);
        setTimeout(() => this.chatHistory.unshift({ user: "panda", message: "Everywhere we go-oh... Everywhere we go-oh… People wanna know-oh… Who we are… Where we come from… So we tell them… We are Pandas!… Mighty mighty Pandas!📣" }), 3200);
        setTimeout(() => this.chatHistory.unshift({ user: "panda", message: "I can’t hear you, sound off like you’ve got a pair!🥜" }), 7200);
        setTimeout(() => this.chatHistory.unshift({ user: "panda", message: "Ok, let me get a good look at you Private " + this.username + "! Upload a photo of yourself by dropping it below… 📸" }), 9200);
        setTimeout(() => this.isDisabled = false, 9200);
      }
      this.messageToSend = "";
      // Add code to update the chat history database
    },
    removeMessage() {
      this.chatHistory.splice(0, 1);
      if (this.first_name == "") {
        this.chatHistory = [];
        this.startMessage();
      } else if (this.last_name == "") {
        this.first_name = "";
        this.chatHistory.splice(0, 2);
      } else if (this.username == "") {
        this.last_name = "";
        this.chatHistory.splice(0, 2);
      } else {
        this.username = "";
        this.chatHistory.splice(0, 4);
      }
      this.messageToSend = "";
      // Add code to update the chat history database
    },
    startMessage() {
      this.isDisabled = true;
      setTimeout(() => this.chatHistory.unshift({ user: "panda", message: "Good " + daypart() + " Private!🫡" }), 1200);
      setTimeout(() => this.chatHistory.unshift({ user: "panda", message: "Welcome to Panda Bootcamp!⛺️" }), 3200);
      setTimeout(() => this.chatHistory.unshift({ user: "panda", message: "What’s your FIRST NAME Private? 🫡" }), 5200);
      setTimeout(() => this.isDisabled = false, 5200);
    },
  },
  components: {
    navBar,
    chatMessage,
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
              <img src="../../src/assets/user.png" class="chatImage" />
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
        <button className="authButton-login" @click="onLogout">Logout</button>
      </div>
      <div v-else>
        <img src="../../src/assets/panda.png" width="200" />
        <h1>Welcome to panda.ai</h1>
        <button className="authButton" @click="redirectToLogin">Log In</button>
      </div>
    </div>
  </main>
</template>
<style scoped>
@import "../assets/styles/panda-main.css";
</style>
