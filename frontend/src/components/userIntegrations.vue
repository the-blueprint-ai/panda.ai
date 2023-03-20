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
  <div className="userIntegrations" v-if="integrationsMenu">
    <h1>USER INTEGRATIONS</h1>
  </div>
</template>
