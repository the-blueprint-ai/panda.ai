<script>
export default {
  props: {
    message: Object,
  },
  computed: {
    avatar() {
      return this.$store.state.userStore.avatar;
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
  <div>
    <img v-bind:src="messageImage()" class="chatAvatar" />
    <p class="message">{{ message.message }}</p>
  </div>
</template>
