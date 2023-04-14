<script>
export default {
  data() {
    return {
      isDisabled: true,
      pandaImage: "",
      userImage: "",
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
    messageImage() {
      if (this.message.user == "panda") {
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
    <p class="message">{{ message.message }}</p>
    <span class="messageRating" v-if="message.user == 'panda' && !isDisabled">
      <img class="thumbUp" src="../assets/icons/hand-thumbs-up.svg" />
      <img class="thumbDown" src="../assets/icons/hand-thumbs-down.svg" />
    </span>
  </div>
</template>
