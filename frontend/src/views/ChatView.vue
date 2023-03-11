<script lang="ts">
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import chatMessage from "../components/chatMessage.vue";

export default defineComponent({
  data() {
    return {
      session: false,
      userId: "",
      messageToSend: "",
      chatHistory: [],
    };
  },
  mounted() {
    this.getUserInfo();
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
      window.location.reload();
    },
    submitMessage() {
      // Add code to send to chatBot
      this.chatHistory.push({ user: "user", message: this.messageToSend });
      this.messageToSend = "";
      // Add code to update the chat history database
    },
    removeMessage() {
      this.chatHistory.splice(0, 1);
      this.messageToSend = "";
      // Add code to update the chat history database
    },
  },
  components: {
    chatMessage,
  },
});
</script>

<template>
  <main>
    <div className="body">
      <div v-if="session">
        <div>
          <h1>CHAT VIEW</h1>
        </div>
        <div className="mainContainer">
          <div className="chatHistoryContainer">
            <h2>Chat History</h2>
            <div className="chatHistory">
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
              <p className="history">+ ...</p>
              <p className="history">+ scroll...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
              <p className="history">+ ...</p>
            </div>
            <button className="startNewChat" @click="startNewChat">
              Start new chat
            </button>
          </div>
          <div className="mainChatContainer">
            <div className="chatContainer">
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
                  className="input"
                  v-model="messageToSend"
                  @keydown.enter.stop.prevent="submitMessage"
                  id="userInput"
                  name="userInput"
                  placeholder="enter your message here"
                  ref="messageInput"
                ></textarea>
                <button className="chatButton" @click="submitMessage">Send</button>
                <button className="chatButton" @click="removeMessage">Undo</button>
              </div>
            </div>
          </div>
        </div>
        <button className="authButton" @click="onLogout">Sign Out</button>
      </div>
      <div v-else>
        <img src="../../src/assets/panda.png" width="200"/>
        <h1>Welcome to panda.ai</h1>
        <button className="authButton" @click="redirectToLogin">Sign In</button>
      </div>
    </div>
  </main>
</template>
<style scoped>
@import "../assets/styles/panda-main.css";
</style>
