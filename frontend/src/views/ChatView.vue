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
      buttonText: "SEND",
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
  <main style="height: 71vh">
    <navBar></navBar>
    <div v-if="session">
      <div class="container-fluid bg-light text-white">
        <div class="container d-flex pt-5 pb-5">
          <div
            v-if="userStoreChatHistory"
            class="card text-bg-white text-primary text-center me-3"
            style="width: 24rem"
          >
            <div class="card-header pt-3 pb-2">
              <h3>CHAT HISTORY</h3>
            </div>
            <div class="card-body scrollable-card-body text-start pt-4 pb-4 px-4">
              <ChatUserChatHistory
                v-if="historyMenu"
                :history-menu="historyMenu"
                :user-store-chat-history="userStoreChatHistory"
                :user-id="userId"
                @update-search-term="currentSearchTerm = $event"
              ></ChatUserChatHistory>
            </div>
            <div class="card-footer pt-3 pb-3">
              <button
                class="btn btn-secondary btn-lg"
                @click="startNewChat"
                style="height: 57px; width: 300px"
              >
                START NEW CHAT
              </button>
            </div>
          </div>
          <div
            v-if="userStoreChatHistory"
            class="card text-bg-white text-primary text-center me-3"
            style="width: 48rem"
          >
            <div class="card-body scrollable-card-body text-start pt-4 pb-4 px-4">
              <chatMessage
                v-for="(item, index) in chatHistory"
                :message="item"
                :class="item.user === 'panda' ? 'pandaChat' : 'userChat'"
                :key="item.user + '-' + index"
                :search-term="currentSearchTerm"
                :is-disabled="this.isDisabled"
              ></chatMessage>
            </div>
            <div class="card-footer pt-2 pt-1">
              <div class="form-floating mb-2 d-flex">
                <img
                  v-if="this.loading"
                  src="../assets/thinking.png"
                  class="chatAvatar mt-2"
                />
                <img v-else v-bind:src="avatar" class="chatAvatar mt-2" />
                <textarea
                  :disabled="this.loading || isDisabled"
                  class="form-control mt-1 mx-3"
                  v-model="messageToSend"
                  @keydown.enter.stop.prevent="submitMessage(this.username)"
                  id="userInput"
                  name="userInput"
                  placeholder="enter your message here..."
                  ref="messageInput"
                  style="min-height: 60px"
                ></textarea>
                <label
                  for="floatingTextarea"
                  class="text-primary"
                  style="margin-left: 65px"
                  >enter your message here...</label
                >
                <button
                  :disabled="this.loading || isDisabled"
                  class="btn btn-secondary btn-lg mt-2"
                  id="sendButton"
                  @click="submitMessage(this.username)"
                  style="max-height: 60px"
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
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
.scrollable-card-body {
  height: 900px;
  overflow-y: auto;
}
.chatAvatar {
  width: 50px;
  height: 50px;
  border-radius: 10px;
}
</style>
