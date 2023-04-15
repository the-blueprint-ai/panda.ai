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
      typing: false,
      isDisabled: true,
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
        if (newVal && newVal.length > 0 && newVal[0].length > 0) {
          // Initialize isVisible property for each item in userChatHistory
          this.visibilityStates = newVal[0].map(() => false);

          // Set the first item's visibility to true (expand the most recent date)
          this.visibilityStates[0] = true;

          // Find the most recent chat
          let latestChat = null;
          for (let day of newVal[0]) {
            for (let chat of day.chats) {
              if (!latestChat || chat.timestamp > latestChat.timestamp) {
                latestChat = chat;
              }
            }
          }

          // Select the most recent chat on page load
          this.selectedChat = latestChat;

          // Set the activeChat
          this.activeChat = this.selectedChat;
        }
      },
    },
    chatHistorySearch: {
      deep: true,
      immediate: true,
      handler(newVal) {
        if (this.chatHistorySearch == "") {
          this.typing = false;
        } else {
          this.typing = true;
        }
      },
    },
  },
  computed: {
    filteredChatData() {
      if (this.chatHistorySearch.trim() === "") {
        return this.userChatHistory[0];
      }

      const searchTerm = this.chatHistorySearch.trim().toLowerCase();

      return this.userChatHistory[0]
        .map((day) => {
          const filteredChats = day.chats.filter((chat) =>
            chat.content.some(
              (contentItem) =>
                contentItem &&
                contentItem.message &&
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
    clearSearch() {
      this.chatHistorySearch = "";
      this.typing = false;
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
          placeholder="🐼 search chat history..."
        />
      </div>
      <img
        v-if="typing"
        class="clearAccountSearch"
        src="../assets/icons/x-circle.svg"
        @click="clearSearch"
      />
      <div class="chatHistoryDateList">
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
    </div>
    <div class="userChatHistoryContent" id="chatContainer">
      <span v-if="selectedChat">
        <chatMessage
          v-for="(contentItem, contentIndex) in selectedChat.content"
          :message="contentItem"
          :class="contentItem.user === 'panda' ? 'pandaChat' : 'userChat'"
          :key="contentIndex"
          :searchTerm="chatHistorySearch"
          :is-disabled="this.isDisabled"
        ></chatMessage>
      </span>
    </div>
  </div>
</template>
