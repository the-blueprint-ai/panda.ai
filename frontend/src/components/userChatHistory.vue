<script>
import chatMessage from "../components/chatMessage.vue";

export default {
  data() {
    return {
      ready: false,
      isVisible: false,
      visibilityStates: [],
      activeChat: null,
      selectedChat: null,
      chatHistorySearch: "",
    };
  },
  watch: {
    userChatHistory: {
      deep: true,
      immediate: true,
      handler(newVal) {
        if (newVal && newVal.length > 0 && newVal[0].length > 0) {
          // Initialize isVisible property for each item in userChatHistory
          this.visibilityStates = newVal[0].map(() => false);

          // Set the first item's visibility to true (expand the most recent date)
          this.visibilityStates[0] = true;

          // Select the most recent chat on page load
          this.selectedChat = newVal[0][newVal[0].length - 1].chats[0];

          // Set the activeChat
          this.activeChat = this.selectedChat;
        }
      },
    },
  },
  props: {
    historyMenu: Boolean,
    userChatHistory: Array,
  },
  computed: {
    reversedChatData() {
      if (
        this.userChatHistory &&
        this.userChatHistory.length > 0 &&
        this.userChatHistory[0].length > 0
      ) {
        return this.userChatHistory[0].slice().reverse();
      }
      return [];
    },
  },
  methods: {
    toggleVisibility(index) {
      this.visibilityStates[index] = !this.visibilityStates[index];
    },
  },
  components: {
    chatMessage,
  },
};
</script>

<template>
  <div class="userChatHistory" v-if="this.userChatHistory && historyMenu">
    <div class="userChatHistoryDates">
      <div class="chatHistorySearch">
        <input
          class="chatHistorySearchBox"
          type="text"
          v-model="chatHistorySearch"
          placeholder="Search chat history..."
        />
      </div>
      <ul>
        <li
          class="chatHistoryDay"
          v-for="(item, index) in reversedChatData"
          :key="index"
        >
          <span @click="toggleVisibility(index)">{{
            visibilityStates[index] ? "- " : "+ "
          }}</span>
          <span @click="toggleVisibility(index)">{{ item.date }}</span>
          <ul v-show="visibilityStates[index]">
            <li
              class="chatHistoryTimeTitle"
              v-for="(chat, chatIndex) in item.chats"
              :key="chatIndex"
            >
              <span class="chatHistoryTime" @click="selectedChat = chat"
                >{{ chat.time }}:</span
              >
              <span class="chatHistoryTitle" @click="selectedChat = chat; activeChat = chat;">{{ chat.title }}</span>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="userChatHistoryContent" id="chatContainer">
      <span v-if="selectedChat">
        <chatMessage
          v-for="(contentItem, contentIndex) in selectedChat.content"
          :message="contentItem"
          :class="contentItem.user + 'Chat'"
          :key="contentIndex"
        ></chatMessage>
      </span>
    </div>
  </div>
</template>
