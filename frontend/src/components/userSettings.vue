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
  <div className="userSettings" v-if="settingsMenu">
    <h1>USER SETTINGS</h1>
  </div>
</template>
