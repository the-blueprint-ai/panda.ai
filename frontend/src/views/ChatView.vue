<script type="text/javascript">
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";
import { mapActions } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import chatMessage from "../components/chatMessage.vue";
import { getUserData } from "../composables/getUserData.js";
import { getUserChatHistory } from "../composables/getUserChatHistory.js";
import UserChatHistory from "../components/userChatHistory.vue";

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
    chatHistory() {
      return this.$store.state.chatStore.chatHistory;
    },
    userChatHistory() {
      return this.$store.state.userStore.chatHistory;
    },
    isDisabled() {
      return this.$store.state.chatStore.isDisabled;
    },
  },
  async mounted() {
    await this.getSession();
    if (this.sesison) {
      await this.getUserInfo();
    }
    if (this.userId) {
      const { userData } = getUserData(this.userId, this.$store);
      userData(this.userId);
      const { userChatHistory } = getUserChatHistory(this.userId, this.$store);
      userChatHistory(this.userId);
    }
  },
  methods: {
    ...mapActions(["getSession", "getUserInfo"]),
    setInputIsVisibleValue(value) {
      this.$store.commit("setInputIsVisible", value);
    },
    addToChatHistory(value) {
      this.$store.commit("setChatHistory", value);
    },
    setIsDisabledValue(value) {
      this.$store.commit("setIsDisabled", value);
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
    submitMessage() {
      // Add code to send to chatBot
      this.addToChatHistory({ user: "user", message: this.messageToSend });
      this.messageToSend = "";
      // Add code to update the chat history database
    },
    saveChatHistory: async function () {
      try {
        const url = import.meta.env.VITE_APP_API_URL + "/chats/save/";
        const res = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.chatHistoryObject),
        });

        // Check if the response status indicates an error
        if (!res.ok) {
          throw new Error(`Server responded with status ${res.status}`);
        }
      } catch (error) {
        // Handle the error
        console.log("An error occurred while saving the file:", error);
        this.setSuccess("");
      }
    },
  },
  components: {
    navBar,
    navFooter,
    UserChatHistory,
    chatMessage,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div class="bodyG">
      <div>
        <div class="mainContainer">
          <div v-if="userChatHistory" class="chatHistoryContainer">
            <h2>Chat History</h2>
            <div class="chatHistory">
              <UserChatHistory
                :user-chat-history="userChatHistory"
              ></UserChatHistory>
            </div>
            <button
              :disabled="isDisabled"
              class="startNewChat"
              @click="startNewChat"
            >
              Start new chat
            </button>
          </div>
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
              </div>
            </div>
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
