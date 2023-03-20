<script>
import chatMessage from "../components/chatMessage.vue";

export default {
  data() {
    return {
      ready: false,
      isVisible: false,
      selectedChat: null,
      chatHistorySearch: "",
      userChatHistory: [
        {
          date: "Yesterday",
          chats: [
            {
              time: "14:18",
              title: "Good Afternoon Private!🫡",
              content: [
                {
                  user: "panda",
                  message:
                    "With all that said, let’s get on with the mission. Eyes forward, soldier! 👀",
                },
                {
                  user: "panda",
                  message:
                    "You can ask me at any time what data I have on you and I’ll give you a detailed summary. 💽",
                },
                {
                  user: "panda",
                  message:
                    "Your data is your data - it sits isolated in your account and can be deleted by you at any time. ❌",
                },
                {
                  user: "panda",
                  message:
                    "Being a Private means I’m very disciplined with your data - I will never use it in my training, I only use the text from the conversations we have. 🙏",
                },
                {
                  user: "panda",
                  message:
                    "I’m just a Private, and in beta right now, but I’ve got lots of plans of how I can train and get promoted. One day I want to be a Colonel! 🤓",
                },
                {
                  user: "panda",
                  message:
                    "This means I can help you find answers to questions you have, make personalised recommendations, help you learn by gathering and summarising information and lots of other tasks.💪",
                },
                {
                  user: "panda",
                  message:
                    "I can learn from lots of different things, like: 👩‍💻 How you browse the internet, 🤷‍♀️ Who your friends are, 🎧 What music you listen to, 📺 What you like watching, 💰 What you spend your money on, 🤓 What you’re interested in",
                },
                {
                  user: "panda",
                  message:
                    "There are lots of things I can help you with and the more you share, the better I can do my job! 🐼",
                },
                {
                  user: "panda",
                  message:
                    "I’m a personalised AI assistant that learns from you and your data. You’re welcome.🙄",
                },
                {
                  user: "panda",
                  message:
                    "To get us there we’re going to have to go through hell and back, but Panda Bootcamp will get you ready for the fight! 🥷",
                },
                {
                  user: "panda",
                  message:
                    "The objective of our mission is make you and I best friends. 😇",
                },
                {
                  user: "panda",
                  message:
                    "Right, form up and I’ll take you through our mission. Ten-hut! 🫡",
                },
                {
                  user: "panda",
                  message: "Ugh, Private Kranos - You is one ugly mother! 🤮",
                },
                {
                  user: "panda",
                  message:
                    "Ok, let me get a good look at you Private Kranos! Upload a photo of yourself by dropping it below… 📸",
                },
                {
                  user: "panda",
                  message:
                    "I can’t hear you, sound off like you’ve got a pair!🥜",
                },
                {
                  user: "panda",
                  message:
                    "Everywhere we go-oh... Everywhere we go-oh… People wanna know-oh… Who we are… Where we come from… So we tell them… We are Pandas!… Mighty mighty Pandas!📣",
                },
                {
                  user: "panda",
                  message:
                    "That’s more like it! Right then Private Kranos! If it ain't raining, we ain't training - move out!🌧️",
                },
                {
                  user: "user",
                  message: "Kranos",
                },
                {
                  user: "panda",
                  message:
                    "What would you like your CODENAME to be here at Panda Bootcamp? 🥸",
                },
                {
                  user: "panda",
                  message:
                    "Ok, Private Betts. We’re going to have to pick this up a bit if you’re to make it through Panda Bootcamp.⛺️",
                },
                {
                  user: "user",
                  message: "Betts",
                },
                {
                  user: "panda",
                  message:
                    "We don't use first names at Panda Bootcamp! I meant, what’s your SURNAME?! 🫡",
                },
                {
                  user: "panda",
                  message: "What is your major malfunction Private Sean?!😳",
                },
                {
                  user: "user",
                  message: "Sean",
                },
                {
                  user: "panda",
                  message: "What’s your FIRST NAME? 🫡",
                },
                {
                  user: "panda",
                  message: "Welcome to Panda Bootcamp!⛺️",
                },
                {
                  user: "panda",
                  message: "Good Afternoon Private!🫡",
                },
              ],
            },
            {
              time: "14:20",
              title: "Good Afternoon Private!🫡",
              content: [
                {
                  user: "panda",
                  message:
                    "With all that said, let’s get on with the mission. Eyes forward, soldier! 👀",
                },
                {
                  user: "panda",
                  message:
                    "You can ask me at any time what data I have on you and I’ll give you a detailed summary. 💽",
                },
                {
                  user: "panda",
                  message:
                    "Your data is your data - it sits isolated in your account and can be deleted by you at any time. ❌",
                },
                {
                  user: "panda",
                  message:
                    "Being a Private means I’m very disciplined with your data - I will never use it in my training, I only use the text from the conversations we have. 🙏",
                },
                {
                  user: "panda",
                  message:
                    "I’m just a Private, and in beta right now, but I’ve got lots of plans of how I can train and get promoted. One day I want to be a Colonel! 🤓",
                },
                {
                  user: "panda",
                  message:
                    "This means I can help you find answers to questions you have, make personalised recommendations, help you learn by gathering and summarising information and lots of other tasks.💪",
                },
                {
                  user: "panda",
                  message:
                    "I can learn from lots of different things, like: 👩‍💻 How you browse the internet, 🤷‍♀️ Who your friends are, 🎧 What music you listen to, 📺 What you like watching, 💰 What you spend your money on, 🤓 What you’re interested in",
                },
                {
                  user: "panda",
                  message:
                    "There are lots of things I can help you with and the more you share, the better I can do my job! 🐼",
                },
                {
                  user: "panda",
                  message:
                    "I’m a personalised AI assistant that learns from you and your data. You’re welcome.🙄",
                },
                {
                  user: "panda",
                  message:
                    "To get us there we’re going to have to go through hell and back, but Panda Bootcamp will get you ready for the fight! 🥷",
                },
                {
                  user: "panda",
                  message:
                    "The objective of our mission is make you and I best friends. 😇",
                },
                {
                  user: "panda",
                  message:
                    "Right, form up and I’ll take you through our mission. Ten-hut! 🫡",
                },
                {
                  user: "panda",
                  message: "Ugh, Private Kranos - You is one ugly mother! 🤮",
                },
                {
                  user: "panda",
                  message:
                    "Ok, let me get a good look at you Private Kranos! Upload a photo of yourself by dropping it below… 📸",
                },
                {
                  user: "panda",
                  message:
                    "I can’t hear you, sound off like you’ve got a pair!🥜",
                },
                {
                  user: "panda",
                  message:
                    "Everywhere we go-oh... Everywhere we go-oh… People wanna know-oh… Who we are… Where we come from… So we tell them… We are Pandas!… Mighty mighty Pandas!📣",
                },
                {
                  user: "panda",
                  message:
                    "That’s more like it! Right then Private Kranos! If it ain't raining, we ain't training - move out!🌧️",
                },
                {
                  user: "user",
                  message: "Kranos",
                },
                {
                  user: "panda",
                  message:
                    "What would you like your CODENAME to be here at Panda Bootcamp? 🥸",
                },
                {
                  user: "panda",
                  message:
                    "Ok, Private Betts. We’re going to have to pick this up a bit if you’re to make it through Panda Bootcamp.⛺️",
                },
                {
                  user: "user",
                  message: "Betts",
                },
                {
                  user: "panda",
                  message:
                    "We don't use first names at Panda Bootcamp! I meant, what’s your SURNAME?! 🫡",
                },
                {
                  user: "panda",
                  message: "What is your major malfunction Private Sean?!😳",
                },
                {
                  user: "user",
                  message: "Sean",
                },
                {
                  user: "panda",
                  message: "What’s your FIRST NAME? 🫡",
                },
                {
                  user: "panda",
                  message: "Welcome to Panda Bootcamp!⛺️",
                },
                {
                  user: "panda",
                  message: "Good Afternoon Private!🫡",
                },
              ],
            },
            {
              time: "14:22",
              title: "Good Afternoon Private!🫡",
              content: [
                {
                  user: "panda",
                  message:
                    "With all that said, let’s get on with the mission. Eyes forward, soldier! 👀",
                },
                {
                  user: "panda",
                  message:
                    "You can ask me at any time what data I have on you and I’ll give you a detailed summary. 💽",
                },
                {
                  user: "panda",
                  message:
                    "Your data is your data - it sits isolated in your account and can be deleted by you at any time. ❌",
                },
                {
                  user: "panda",
                  message:
                    "Being a Private means I’m very disciplined with your data - I will never use it in my training, I only use the text from the conversations we have. 🙏",
                },
                {
                  user: "panda",
                  message:
                    "I’m just a Private, and in beta right now, but I’ve got lots of plans of how I can train and get promoted. One day I want to be a Colonel! 🤓",
                },
                {
                  user: "panda",
                  message:
                    "This means I can help you find answers to questions you have, make personalised recommendations, help you learn by gathering and summarising information and lots of other tasks.💪",
                },
                {
                  user: "panda",
                  message:
                    "I can learn from lots of different things, like: 👩‍💻 How you browse the internet, 🤷‍♀️ Who your friends are, 🎧 What music you listen to, 📺 What you like watching, 💰 What you spend your money on, 🤓 What you’re interested in",
                },
                {
                  user: "panda",
                  message:
                    "There are lots of things I can help you with and the more you share, the better I can do my job! 🐼",
                },
                {
                  user: "panda",
                  message:
                    "I’m a personalised AI assistant that learns from you and your data. You’re welcome.🙄",
                },
                {
                  user: "panda",
                  message:
                    "To get us there we’re going to have to go through hell and back, but Panda Bootcamp will get you ready for the fight! 🥷",
                },
                {
                  user: "panda",
                  message:
                    "The objective of our mission is make you and I best friends. 😇",
                },
                {
                  user: "panda",
                  message:
                    "Right, form up and I’ll take you through our mission. Ten-hut! 🫡",
                },
                {
                  user: "panda",
                  message: "Ugh, Private Kranos - You is one ugly mother! 🤮",
                },
                {
                  user: "panda",
                  message:
                    "Ok, let me get a good look at you Private Kranos! Upload a photo of yourself by dropping it below… 📸",
                },
                {
                  user: "panda",
                  message:
                    "I can’t hear you, sound off like you’ve got a pair!🥜",
                },
                {
                  user: "panda",
                  message:
                    "Everywhere we go-oh... Everywhere we go-oh… People wanna know-oh… Who we are… Where we come from… So we tell them… We are Pandas!… Mighty mighty Pandas!📣",
                },
                {
                  user: "panda",
                  message:
                    "That’s more like it! Right then Private Kranos! If it ain't raining, we ain't training - move out!🌧️",
                },
                {
                  user: "user",
                  message: "Kranos",
                },
                {
                  user: "panda",
                  message:
                    "What would you like your CODENAME to be here at Panda Bootcamp? 🥸",
                },
                {
                  user: "panda",
                  message:
                    "Ok, Private Betts. We’re going to have to pick this up a bit if you’re to make it through Panda Bootcamp.⛺️",
                },
                {
                  user: "user",
                  message: "Betts",
                },
                {
                  user: "panda",
                  message:
                    "We don't use first names at Panda Bootcamp! I meant, what’s your SURNAME?! 🫡",
                },
                {
                  user: "panda",
                  message: "What is your major malfunction Private Sean?!😳",
                },
                {
                  user: "user",
                  message: "Sean",
                },
                {
                  user: "panda",
                  message: "What’s your FIRST NAME? 🫡",
                },
                {
                  user: "panda",
                  message: "Welcome to Panda Bootcamp!⛺️",
                },
                {
                  user: "panda",
                  message: "Good Afternoon Private!🫡",
                },
              ],
            },
          ],
        },
        {
          date: "Today",
          chats: [
            {
              time: "15:06",
              title: "Good Afternoon Private!🫡",
              content: [
                {
                  user: "panda",
                  message:
                    "With all that said, let’s get on with the mission. Eyes forward, soldier! 👀",
                },
                {
                  user: "panda",
                  message:
                    "You can ask me at any time what data I have on you and I’ll give you a detailed summary. 💽",
                },
                {
                  user: "panda",
                  message:
                    "Your data is your data - it sits isolated in your account and can be deleted by you at any time. ❌",
                },
                {
                  user: "panda",
                  message:
                    "Being a Private means I’m very disciplined with your data - I will never use it in my training, I only use the text from the conversations we have. 🙏",
                },
                {
                  user: "panda",
                  message:
                    "I’m just a Private, and in beta right now, but I’ve got lots of plans of how I can train and get promoted. One day I want to be a Colonel! 🤓",
                },
                {
                  user: "panda",
                  message:
                    "This means I can help you find answers to questions you have, make personalised recommendations, help you learn by gathering and summarising information and lots of other tasks.💪",
                },
                {
                  user: "panda",
                  message:
                    "I can learn from lots of different things, like: 👩‍💻 How you browse the internet, 🤷‍♀️ Who your friends are, 🎧 What music you listen to, 📺 What you like watching, 💰 What you spend your money on, 🤓 What you’re interested in",
                },
                {
                  user: "panda",
                  message:
                    "There are lots of things I can help you with and the more you share, the better I can do my job! 🐼",
                },
                {
                  user: "panda",
                  message:
                    "I’m a personalised AI assistant that learns from you and your data. You’re welcome.🙄",
                },
                {
                  user: "panda",
                  message:
                    "To get us there we’re going to have to go through hell and back, but Panda Bootcamp will get you ready for the fight! 🥷",
                },
                {
                  user: "panda",
                  message:
                    "The objective of our mission is make you and I best friends. 😇",
                },
                {
                  user: "panda",
                  message:
                    "Right, form up and I’ll take you through our mission. Ten-hut! 🫡",
                },
                {
                  user: "panda",
                  message: "Ugh, Private Kranos - You is one ugly mother! 🤮",
                },
                {
                  user: "panda",
                  message: "What’s your FIRST NAME? 🫡",
                },
                {
                  user: "panda",
                  message: "Welcome to Panda Bootcamp!⛺️",
                },
                {
                  user: "panda",
                  message: "Good Afternoon Private!🫡",
                },
              ],
            },
          ],
        },
      ],
    };
  },
  watch: {
    userChatHistory: {
      deep: true,
      handler(newVal, oldVal) {
        if (newVal.length > 0) {
          this.ready = true;
        }
      },
    },
  },
  props: {
    historyMenu: Boolean,
    // userChatHistory: Array,
  },
  created() {
    if (this.userChatHistory && this.userChatHistory.length > 0) {
      // Select the first chat in the first date item by default
      this.selectedChat = this.userChatHistory[0].chats[0];
    }
  },
  computed: {
    reversedChatData() {
      return this.userChatHistory.slice().reverse();
    },
  },
  methods: {
    toggleVisibility(index) {
      this.reversedChatData[index].isVisible =
        !this.reversedChatData[index].isVisible;
    },
  },
  components: {
    chatMessage,
  },
};
</script>

<template>
  <div className="userChatHistory" v-if="this.userChatHistory && historyMenu">
    <div className="userChatHistoryDates">
      <div className="chatHistorySearch">
        <input className="chatHistorySearchBox" type="text" v-model="chatHistorySearch" placeholder="Search chat history..." />
      </div>
      <ul>
        <li
          className="chatHistoryDay"
          v-for="(item, index) in reversedChatData"
          :key="index"
        >
          <span @click="toggleVisibility(index)">{{
            item.isVisible ? "- " : "+ "
          }}</span>
          <span @click="toggleVisibility(index)">{{ item.date }}</span>
          <ul v-show="item.isVisible">
            <li
              className="chatHistoryTimeTitle"
              v-for="(chat, chatIndex) in item.chats"
              :key="chatIndex"
            >
              <span className="chatHistoryTime" @click="selectedChat = chat">{{ chat.time }}:</span>
              <span className="chatHistoryTitle" @click="selectedChat = chat">{{chat.title}}</span>
            </li>
          </ul>
        </li>
      </ul>
    </div>
    <div className="userChatHistoryContent" id="chatContainer">
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
