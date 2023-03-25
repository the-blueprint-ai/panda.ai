<script>
export default {
  props: {
    message: Object,
    searchTerm: String,
  },
  computed: {
    avatar() {
      return this.$store.state.userStore.avatar;
    },
    containsSearchTerm() {
      if (this.searchTerm.trim() === "") return false;
      return this.message.message
        .toLowerCase()
        .includes(this.searchTerm.trim().toLowerCase());
    },
    messageClass() {
      return this.containsSearchTerm ? "highlighted" : "";
    },
  },
  methods: {
    messageImage() {
      if (this.message.user == "panda") {
        return "/src/assets/panda.png";
      } else if (!this.avatar) {
        return "/src/assets/user.png";
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
  </div>
</template>
