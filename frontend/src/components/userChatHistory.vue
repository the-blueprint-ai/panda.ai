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
  props: {
    historyMenu: Boolean,
    userChatHistory: {
      type: Array,
      required: true,
    },
  },
  watch: {
    userChatHistory: {
      deep: true,
      immediate: true,
      handler(newVal) {
        console.log("Received user chat history:", newVal);
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
    filteredChatData() {
      if (this.chatHistorySearch.trim() === "") {
        return this.reversedChatData;
      }

      const searchTerm = this.chatHistorySearch.trim().toLowerCase();

      return this.reversedChatData
        .map((day) => {
          const filteredChats = day.chats.filter((chat) =>
            chat.content.some((contentItem) =>
              contentItem.message.toLowerCase().includes(searchTerm)
            )
          );

          if (filteredChats.length > 0) {
            return {
              ...day,
              chats: filteredChats,
            };
          }
        })
        .filter((item) => item);
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
          v-for="(item, index) in filteredChatData"
          :key="index"
        >
          <span @click="toggleVisibility(index)">{{
            visibilityStates[index] ? "- " : "+ "
          }}</span>
          <span @click="toggleVisibility(index)">{{ item.date }}</span>
          <ul v-show="visibilityStates[index]">
            <li
              class="chatHistoryTimeTitle"
              :class="{ active: activeChat === chat }"
              v-for="(chat, chatIndex) in item.chats"
              :key="chatIndex"
            >
              <span
                class="chatHistoryTime"
                @click="activeChat = selectedChat = chat"
                >{{ chat.time }}:</span
              >
              <span
                class="chatHistoryTitle"
                :class="{ active: chat === activeChat }"
                @click="activeChat = selectedChat = chat"
                >{{ chat.title }}</span
              >
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
          :searchTerm="chatHistorySearch"
        ></chatMessage>
      </span>
    </div>
  </div>
</template>
