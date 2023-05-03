<script>
export default {
  data() {
    return {
      isDisabled: true,
      pandaImage: "",
      userImage: "",
      thinkingImage: "",
    };
  },
  props: {
    message: Object,
    searchTerm: String,
    // isDisabled: Boolean,
  },
  async created() {
    const pandaImageModule = await import("../assets/panda.png");
    this.pandaImage = pandaImageModule.default;
    const userImageModule = await import("../assets/user.png");
    this.userImage = userImageModule.default;
    const thinkingImageModule = await import("../assets/thinking.png");
    this.thinkingImage = thinkingImageModule.default;
  },
  computed: {
    avatar() {
      return this.$store.state.userStore.avatar;
    },
    containsSearchTerm() {
      if (this.searchTerm) {
        if (this.searchTerm.trim() === "") return false;
        return this.message.message
          .toLowerCase()
          .includes(this.searchTerm.trim().toLowerCase());
      }
      return null;
    },
    messageClass() {
      return this.containsSearchTerm ? "highlighted" : "";
    },
  },
  methods: {
    formatMessage(message) {
      const urlPattern = /(https?:\/\/[^\s/$.?#].[^\s]*)/gi;

      // Create a temporary DOM element to parse and manipulate the message HTML
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = message;

      // Iterate through all text nodes within the temporary DOM element
      function traverseTextNodes(node) {
        if (node.nodeType === Node.TEXT_NODE) {
          // Replace URLs with clickable links in the text node's content
          node.textContent = node.textContent.replace(urlPattern, (match) => {
            return `<a href="${match}" target="_blank">${match}</a>`;
          });
        } else {
          // Continue traversing child nodes
          for (const child of node.childNodes) {
            traverseTextNodes(child);
          }
        }
      }

      traverseTextNodes(tempDiv);

      // Return the modified HTML
      return tempDiv.innerHTML;
    },
    messageImage() {
      if (this.message.message == "Thinking...") {
        return this.thinkingImage;
      } else if (this.message.user == "panda") {
        return this.pandaImage;
      } else if (!this.avatar) {
        return this.userImage;
      } else if (this.avatar) {
        return this.avatar;
      }
    },
  },
};
</script>

<template>
  <div :class="['chatMessage', message.user, messageClass]">
    <img v-bind:src="messageImage()" class="chatAvatar" />
    <p class="message" v-html="formatMessage(message.message)"></p>
    <span class="messageRating" v-if="message.user == 'panda' && !isDisabled">
      <img class="thumbUp" src="../assets/icons/hand-thumbs-up.svg" />
      <img class="thumbDown" src="../assets/icons/hand-thumbs-down.svg" />
    </span>
  </div>
</template>

<style scoped>
.userChat {
  background-color: #FFFFFF;
  text-align: left;
  display: flex;
  max-width: 785px;
  padding-left: 60px;
  flex-direction: row-reverse;
  justify-content: right;
  align-items: right;
}
.userChat.highlighted {
  position: relative;
  width: 99%;
  margin-top: 5px;
  margin-bottom: 5px;
  background-color: #FFCB4C;
  border-radius: 15px;
  flex-direction: row-reverse;
  justify-content: right;
  align-items: right;
  border: none;
}
.pandaChat {
  background-color: #FFFFFF;
  text-align: left;
  display: flex;
  max-width: 785px;
  padding-right: 60px;
  flex-direction: row;
  justify-content: left;
  align-items: left;
}
.pandaChat.highlighted {
  position: relative;
  width: 99%;
  margin-top: 5px;
  margin-bottom: 5px;
  background-color: #FFCB4C;
  border-radius: 15px;
  border: none;
}
.chatMessage {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #EFEFEF;
}
.message {
  display: flex;
  flex-direction: column;
  align-items: left;
  margin: 10px;
  padding-top: 10px;
  padding-left: 15px;
  padding-right: 15px;
  padding-bottom: 15px;
  width:fit-content;
  word-wrap: break-word;
  border-radius: 15px;
  color: #000000;
}
.message ol li {
  margin-bottom: 10px;
}
.message a {
  color: #000000;
  text-decoration: none;
  text-align: center;
}
.message a:hover {
  color: #FFCB4C;
  text-decoration: none;
}
.chatAvatar {
  width: 50px;
  height: 50px;
  margin: 5px;
  margin-bottom: 12px;
  border-radius: 10px;
}
</style>
