<script>
import { mapActions, mapMutations, mapGetters } from "vuex";
import { saveUserChatHistory } from "../composables/saveUserChatHistory.js";

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
    userStoreChatHistory: {
      type: Array,
      required: true,
    },
    userId: String,
  },
  watch: {
    userStoreChatHistory: {
      deep: true,
      immediate: true,
      handler(newVal) {
        if (newVal && newVal.length > 0 && newVal[0].length > 0) {
          // Initialize isVisible property for each item in userStoreChatHistory
          this.visibilityStates = newVal[0].map(() => false);

          // Set the first item's visibility to true (expand the most recent date)
          this.visibilityStates[0] = true;
        }
      },
    },
  },
  computed: {
    ...mapGetters("chatStore", {
      getChatStoreChatHistory: "getChatStoreChatHistory",
      getIsDisabled: "getIsDisabled",
    }),
    ...mapGetters("userStore", {
      getUserStoreChatHistory: "getStoreUserChatHistory",
    }),
    reversedChatData() {
      if (
        this.userStoreChatHistory &&
        this.userStoreChatHistory.length > 0 &&
        this.userStoreChatHistory[0].length > 0
      ) {
        return this.userStoreChatHistory[0].slice().reverse();
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
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    ...mapMutations("chatStore", {
      addToStoreChatHistory: "setMultiChatHistory",
      emptyStoreChatHistory: "emptyChatHistory",
      setIsDisabled: "setIsDisabled",
    }),
    toggleVisibility(index) {
      this.visibilityStates[index] = !this.visibilityStates[index];
    },
    saveUnsavedChats() {
      if (this.getChatStoreChatHistory.length > 0) {
        saveUserChatHistory(this.userId, this.getChatStoreChatHistory);
      }
    },
    showSelectedChat(dayIndex, chatIndex) {
      if (!this.getIsDisabled) {
        this.saveUnsavedChats();
      }
      this.setIsDisabled(true);
      const selectedDay = this.filteredChatData[dayIndex];
      this.selectedChat = selectedDay.chats[chatIndex];

      const searchTerm = this.chatHistorySearch.trim().toLowerCase();

      // Add highlighted property to each chat message
      this.selectedChat.content.forEach((contentItem) => {
        contentItem.highlighted = contentItem.message.toLowerCase().includes(searchTerm);
      });

      this.activeChat = this.selectedChat;
      this.emptyStoreChatHistory();
      this.addToStoreChatHistory(this.selectedChat.content);
    },
  },
  components: {},
};
</script>

<template>
  <div
    class="chatUserChatHistory"
    v-if="this.userStoreChatHistory && historyMenu"
  >
    <div class="chatUserChatHistoryDates">
      <div class="chatUserChatHistorySearch">
        <input
          class="chatUserChatHistorySearchBox"
          type="text"
          v-model="chatHistorySearch"
          @input="$emit('update-search-term', chatHistorySearch)"
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
                @click="showSelectedChat(index, chatIndex)"
                >{{ chat.time }}:</span
              >
              <span
                class="chatHistoryTitle"
                :class="{ active: chat === activeChat }"
                @click="showSelectedChat(index, chatIndex)"
                >{{ chat.title }}</span
              >
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>
