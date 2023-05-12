<script>
export default {
  data() {
    return {};
  },
  watch: {},
  props: {
    integrationsMenu: Boolean,
  },
  created() {},
  components: {},
};
</script>

<template>
  <div class="d-flex flex-column justify-content-center text-center" v-if="integrationsMenu">
    <h1>COMING SOON...</h1>
    <p>Add number of integrations</p>
    <p>Add list of integrations for selection</p>
    <p>Only allow update once a month</p>
  </div>
</template>

<style scoped>
</style>
