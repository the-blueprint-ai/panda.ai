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
  <div class="userSubscription" v-if="subscriptionMenu">
    <h1>COMING SOON...</h1>
  </div>
</template>

<style scoped>
.userSubscription {
  display: flex;
  width: 100%;
  justify-content: center;
}
</style>