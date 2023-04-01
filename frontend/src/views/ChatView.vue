<script>
import { defineComponent } from "vue";
import { mapActions, mapGetters, mapMutations } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import chatMessage from "../components/chatMessage.vue";
import { getUserData } from "../composables/getUserData.js";
import { getUserChatHistory } from "../composables/getUserChatHistory.js";
import ChatUserChatHistory from "../components/chatUserChatHistory.vue";
import { saveUserChatHistory } from "../composables/saveUserChatHistory.js";

export default defineComponent({
  data() {
    return {
      messageToSend: "",
      historyMenu: true,
    };
  },
  watch: {
    userStoreChatHistory(newValue, oldValue) {
      // React to changes in userStoreChatHistory
      this.refreshUserChatHistory();
    },
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
      userStoreChatHistory: "getStoreUserChatHistory",
    }),
    ...mapGetters("chatStore", {
      getChatStoreChatHistory: "getChatStoreChatHistory",
      getIsDisabled: "getIsDisabled",
    }),
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
    this.emptyChatStoreHistory;
  },
  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    ...mapMutations("chatStore", {
      addToChatStoreChatHistory: "setChatStoreChatHistory",
      emptyStoreChatHistory: "emptyChatHistory",
      setIsDisabled: "setIsDisabled",
    }),
    setInputIsVisibleValue(value) {
      this.$store.commit("setInputIsVisible", value);
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
    async startNewChat() {
      if (!this.getIsDisabled) {
        if (this.getChatStoreChatHistory.length > 0) {
          saveUserChatHistory(this.userId, this.getChatStoreChatHistory);
        }
      }
      this.emptyStoreChatHistory();
      getUserChatHistory(this.$store, this.userId);
      this.setIsDisabled(false);
    },
    submitMessage() {
      // Add code to send to chatBot
      this.addToChatStoreChatHistory({ user: "user", message: this.messageToSend });
      this.messageToSend = "";
      // Add code to update the chat history database
    },
  },
  components: {
    navBar,
    navFooter,
    ChatUserChatHistory,
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
          <div v-if="userStoreChatHistory" class="chatHistoryContainer">
            <h2>Chat History</h2>
            <div class="chatHistory">
              <ChatUserChatHistory
                :history-menu="historyMenu"
                :user-store-chat-history="userStoreChatHistory"
                :user-id="userId"
              ></ChatUserChatHistory>
            </div>
            <button class="startNewChat" @click="startNewChat">
              Start new chat
            </button>
          </div>
          <div class="mainChatContainer">
            <div class="chatContainer" id="chatContainer">
              <chatMessage
                v-for="(item, index) in chatHistory"
                :message="item"
                :class="item.user + 'Chat'"
                :key="item.user + '-' + index"
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
