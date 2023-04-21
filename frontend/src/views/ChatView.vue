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
import { updateUserChatHistory } from "../composables/updateUserChatHistory.js";
import { pandaChat } from "../composables/pandaChat.js";

export default defineComponent({
  data() {
    return {
      messageToSend: "",
      chat_id: null,
      historyMenu: true,
      currentSearchTerm: null,
      activeChat: null,
    };
  },
  watch: {},
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
    this.startNewChat();
  },
  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    ...mapMutations("chatStore", {
      addToChatStoreChatHistory: "setChatStoreChatHistory",
      removeChatHistory: "removeChatHistory",
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
      this.emptyStoreChatHistory();
      this.setIsDisabled(false);
      this.focusInput();
    },
    async submitMessage(username) {
      this.addToChatStoreChatHistory({
        user: username,
        message: this.messageToSend,
      });
      setTimeout(
        () =>
          this.addToChatStoreChatHistory({
            user: "panda",
            message: "Thinking...",
          }),
        1200
      );
      const waitForResponse = async () => {
        return new Promise((resolve) => {
          const pandaResponse = pandaChat(
            this.userId,
            this.first_name,
            this.last_name,
            this.username,
            this.messageToSend
          );
          resolve(pandaResponse);
        });
      };

      Promise.resolve().then(() => {
        this.messageToSend = "";
      });

      const pandaResponse = await waitForResponse();
      this.removeChatHistory(1);
      this.addToChatStoreChatHistory({ user: "panda", message: pandaResponse });

      // Add code to update the chat history database
      const chatHistory = this.getChatStoreChatHistory;

      if (this.chat_id === null) {
        // Save chat history for the first time
        try {
          const savedChatId = await saveUserChatHistory(
            this.userId,
            chatHistory
          );
          this.chat_id = savedChatId;
        } catch (error) {
          console.error("Failed to save chat history:", error);
        }
      } else {
        // Update chat history with the existing chat_id
        try {
          await updateUserChatHistory(this.chat_id, chatHistory);
        } catch (error) {
          console.error("Failed to update chat history:", error);
        }
      }
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
                v-if="historyMenu"
                :history-menu="historyMenu"
                :user-store-chat-history="userStoreChatHistory"
                :user-id="userId"
                @update-search-term="currentSearchTerm = $event"
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
                :class="item.user === 'panda' ? 'pandaChat' : 'userChat'"
                :key="item.user + '-' + index"
                :search-term="currentSearchTerm"
                :is-disabled="this.isDisabled"
              ></chatMessage>
            </div>
            <div class="userInputContainer">
              <img v-bind:src="avatar" class="chatAvatar" />
              <div class="userInput">
                <textarea
                  :disabled="isDisabled"
                  class="input"
                  v-model="messageToSend"
                  @keydown.enter.stop.prevent="submitMessage(this.username)"
                  id="userInput"
                  name="userInput"
                  placeholder="enter your message here"
                  ref="messageInput"
                ></textarea>
                <button
                  :disabled="isDisabled"
                  class="chatButton"
                  id="sendButton"
                  @click="submitMessage(this.username)"
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