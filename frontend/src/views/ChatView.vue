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
import SpinnerComponent from "../components/spinnerComponent.vue";

export default defineComponent({
  data() {
    return {
      messageToSend: "",
      chat_id: null,
      historyMenu: true,
      currentSearchTerm: null,
      activeChat: null,
      thinkingAvatar: "../../assets/user.png",
      loading: false,
      buttonText: "Send",
    };
  },
  watch: {},
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
      isDisabled: "getIsDisabled",
    }),
    inputIsVisible() {
      return this.$store.state.chatStore.inputIsVisible;
    },
    chatHistory() {
      return this.$store.state.chatStore.chatHistory;
    },
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
      const tempMessage = this.messageToSend;
      this.loading = true;
      this.messageToSend = "🐼 thinking...";
      this.setIsDisabledValue(true);
      this.addToChatStoreChatHistory({
        user: username,
        message: tempMessage,
      });
      const waitForResponse = async () => {
        return new Promise((resolve) => {
          const pandaResponse = pandaChat(
            this.userId,
            this.first_name,
            this.last_name,
            this.username,
            tempMessage
          );
          resolve(pandaResponse);
        });
      };

      Promise.resolve().then(() => {});

      const pandaResponse = await waitForResponse();
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
      this.messageToSend = "";
      this.setIsDisabledValue(false);
      this.loading = false;
    },
  },
  components: {
    navBar,
    navFooter,
    ChatUserChatHistory,
    chatMessage,
    SpinnerComponent,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div class="bodyG">
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
              :is-disabled="this.loading"
            ></chatMessage>
          </div>
          <div class="userInputContainer">
            <img v-if="this.loading" src="../assets/thinking.png" class="chatAvatar" />
            <img v-else v-bind:src="avatar" class="chatAvatar" />
            <div class="userInput">
              <textarea
                :disabled="this.loading"
                class="input"
                v-model="messageToSend"
                @keydown.enter.stop.prevent="submitMessage(this.username)"
                id="userInput"
                name="userInput"
                placeholder="enter your message here"
                ref="messageInput"
              ></textarea>
              <button
                :disabled="this.loading"
                class="chatButton"
                id="sendButton"
                @click="submitMessage(this.username)"
              >
                <SpinnerComponent
                  :loading="this.loading"
                  :button-text="this.buttonText"
                ></SpinnerComponent>
              </button>
            </div>
          </div>
        </div>
      </div>
      <button class="startNewChatSmall" @click="startNewChat">
        Start new chat
      </button>
    </div>
    <navFooter></navFooter>
  </main>
</template>
