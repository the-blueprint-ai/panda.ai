<script>
import { RouterView } from "vue-router";
import { mapState } from "vuex";

export default {
  components: {
    RouterView,
  },
  computed: mapState({
    session: state => state.userStore.session,
    userId: state => state.userStore.userId,
    email: state => state.userStore.email,
    first_name: state => state.userStore.first_name,
    last_name: state => state.userStore.last_name,
    username: state => state.userStore.username,
    typeValue: state => state.typingStore.typeValue,
    typeStatus: state => state.typingStore.typeStatus,
    displayTextArray: state => state.typingStore.displayTextArray,
    typingSpeed: state => state.typingStore.typingSpeed,
    newTextDelay: state => state.typingStore.newTextDelay,
    typingStore: state => state.typingStore.displayTextArrayIndex,
    charIndex: state => state.typingStore.charIndex,
    isOpen: state => state.store.isOpen,
  }),
};
</script>

<template>
  <RouterView />
</template>
