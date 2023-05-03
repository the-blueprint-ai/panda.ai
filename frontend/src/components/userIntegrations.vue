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
  <div class="userIntegrations" v-if="integrationsMenu">
    <h1>COMING SOON...</h1>
  </div>
</template>

<style scoped>
.userIntegrations {
  display: flex;
  width: 100%;
  justify-content: center;
}
</style>
