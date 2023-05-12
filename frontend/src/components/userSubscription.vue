<script>
export default {
  data() {
    return {};
  },
  watch: {},
  props: {
    subscriptionMenu: Boolean,
    email: String,
  },
  created() {},
  computed: {
    updateSubscriptionLink() {
      return `https://checkout.mypanda.ai/p/login/bIY5mGaBeatmdFucMM?prefilled_email=${this.email}`;
    },
  },
  components: {},
};
</script>

<template>
  <div
    class="d-flex flex-column justify-content-center text-center"
    v-if="subscriptionMenu"
  >
    <h3 class="mt-4">To update your subscription, please click below:</h3>
    <p>Add current subscripton details...</p>
    <a :href="updateSubscriptionLink" target="_blank">
      <button
        class="btn btn-secondary btn-lg mt-4 mx-auto"
        style="width: 300px"
      >
        UPDATE SUBSCRIPTION
      </button>
    </a>
  </div>
</template>

<style scoped></style>
