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
      // Regex pattern to match URLs not contained in <a>, <img>, or <iframe> tags
      const urlPattern = /(?<!<a\s+(?:[^>]*?\s+)?href=["'])(?<!<img\s+(?:[^>]*?\s+)?src=["'])(?<!<iframe\s+(?:[^>]*?\s+)?src=["'])(https?:\/\/[^\s/$.?#].[^\s]*)/gi;

      // Replace URLs with clickable links
      message = message.replace(urlPattern, '<a href="$1" target="_blank">$1</a>');

      // Add line breaks after links
      message = message.replace(/<a>/g, "<br><a>");

      return message;
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
