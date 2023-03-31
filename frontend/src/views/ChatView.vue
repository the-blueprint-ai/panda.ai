<script>
import { defineComponent } from "vue";
import { mapActions, mapGetters, mapMutations } from "vuex";
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
      historyMenu: true,
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
      userChatHistory: "getStoreUserChatHistory",
    }),
    ...mapMutations("chatStore", {
      emptyChatHistory: "emptyChatHistory",
    }),
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
    isDisabled() {
      return this.$store.state.chatStore.isDisabled;
    },
  },
  async mounted() {
    await this.getSession();
    await this.getUserInfo();
    const { userData } = getUserData(this.$store, this.userId);
    userData(this.userId);
    const { userChatHistory } = getUserChatHistory(this.$store, this.userId);
    userChatHistory(this.userId);
    this.emptyChatHistory;
  },
  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
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
      this.$router.push("/signin");
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
                :history-menu="historyMenu"
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
