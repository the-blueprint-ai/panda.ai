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
      selectedDate: null,
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
          // this.selectedDate = newVal[0][0].date;
          // this.resetSelectedChat();

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
    allChats() {
      return this.filteredChatData.reduce((accumulator, day) => {
        return accumulator.concat(day.chats);
      }, []);
    },
    chatsBySelectedDate() {
      if (!this.selectedDate) {
        return [];
      }

      const selectedDateData = this.filteredChatData.find(
        (item) => item.date === this.selectedDate
      );

      return selectedDateData ? selectedDateData.chats : [];
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
    <div class="chatHistorySideBar">
      <div class="input-group sticky-top">
        <input
          v-model="chatHistorySearch"
          type="text"
          class="form-control shadow-none"
          id="searchInput"
          placeholder="🐼 search chat history..."
        />
        <button
          v-if="typing"
          class="btn btn-warning pb-2"
          @click="clearSearch"
          type="button"
          id="button-addon2"
        >
          <img src="../assets/icons/x-circle.svg" />
        </button>
      </div>
      <div class="chatHistoryDateListAccount">
        <ul class="list-unstyled mt-3">
          <li
            class="mt-2"
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
                  ><strong>{{ chat.time }}: </strong></span
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
    <div class="chatSelector">
      <select
        v-model="selectedDate"
        @change="resetSelectedChat"
        class="form-select"
        aria-label="Default select example"
      >
        <option
          selected
          v-for="(item, index) in filteredChatData"
          :key="index"
          :value="item.date"
        >
          {{ item.date }}
        </option>
      </select>
      <select
        v-model="selectedChat"
        @change="activeChat = selectedChat"
        class="form-select mt-2"
        aria-label="Default select example"
      >
        <option
          v-for="(chat, chatIndex) in chatsBySelectedDate"
          :key="chatIndex"
          :value="chat"
        >
          {{ chat.title }} ({{ chat.time }})
        </option>
      </select>
    </div>
    <div class="userChatHistoryContent" id="chatContainer">
      <span v-if="selectedChat">
        <chatMessage
          v-for="(contentItem, contentIndex) in selectedChat.content
            .slice()
            .reverse()"
          :message="contentItem"
          :class="contentItem.user === 'panda' ? 'pandaChat' : 'userChat'"
          :key="contentIndex"
          :searchTerm="chatHistorySearch"
          :feedback-disabled="true"
        ></chatMessage>
      </span>
    </div>
  </div>
</template>

<style scoped>
.userChatHistory {
  display: flex;
  width: 100%;
  justify-content: flex-start;
  overflow-x: hidden;
}
.chatHistorySideBar {
  min-width: 400px;
  max-width: 400px;
  padding: 10px;
  margin: 0px;
  display: flex;
  flex-direction: column;
  text-align: left;
  border-right: 1px solid lightgray;
}
.list-unstyled li {
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow-x: hidden;
}
.list-unstyled:hover {
  cursor: pointer;
}
.userChatHistoryContent {
  display: flex;
  flex-direction: column-reverse;
  min-width: 790px;
  margin: 10px;
  margin-left: 40px;
}
.mobileAccountChatPickers {
  display: none;
}
.chatSelector {
  display: none;
}
@media (max-width: 1440px) {
  .chatHistorySideBar {
    min-width: 250px;
    max-width: 250px;
  }
}
@media (max-width: 1200px) {
  .userChatHistoryContent {
    min-width: 600px;
    margin-left: 10px;
  }
}
@media (max-width: 992px) {
  .userChatHistoryContent {
    min-width: 410px;
  }
}
@media (max-width: 768px) {
  .userChatHistory {
    display: flex;
    flex-direction: column;
  }
  .chatHistorySideBar {
    display: none;
  }
  .mobileAccountChatPickers {
    display: block;
  }
  .userChatHistoryContent {
    min-width: 480px;
    margin-left: 0px;
  }
  .chatSelector {
    display: block;
    padding-bottom: 10px;
    border-bottom: 1px solid #efefef;
  }
}
@media (max-width: 576px) {
}
</style>
