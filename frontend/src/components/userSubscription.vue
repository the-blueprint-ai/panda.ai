<script>
export default {
  data() {
    return {};
  },
  watch: {},
  props: {
    subscriptionMenu: Boolean,
  },
  created() {},
  components: {},
};
</script>

<template>
  <div className="userSubscription" v-if="subscriptionMenu">
    <h1>USER SUBSCRIPTION</h1>
  </div>
</template>
