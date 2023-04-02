<script>
export default {
  data() {
    return {};
  },
  watch: {},
  props: {
    settingsMenu: Boolean,
  },
  created() {},
  components: {},
};
</script>

<template>
  <div class="userSettings" v-if="settingsMenu">
    <h1>COMING SOON...</h1>
    <h2>CHANGE PASSWORD</h2>
    <h2>DELETE ACCOUNT</h2>
  </div>
</template>
