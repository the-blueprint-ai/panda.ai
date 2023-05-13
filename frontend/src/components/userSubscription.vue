<script>
import { DateTime } from "luxon";
import SpinnerComponent from "../components/spinnerComponent.vue";

export default {
  data() {
    return {
      planName: "",
      integrationsMessage: "",
      planPrice: "",
    };
  },
  watch: {},
  props: {
    subscriptionMenu: Boolean,
    email: String,
    subscriber: Boolean,
    subscribed: String,
    integrations: Number,
    messagesPerMonth: Number,
    planID: String,
  },
  created() {
    this.checkIntegrations();
    this.setPlanName();
    this.setPlanPrice();
  },
  computed: {
    updateSubscriptionLink() {
      return `https://checkout.mypanda.ai/p/login/bIY5mGaBeatmdFucMM?prefilled_email=${this.email}`;
    },
    setTime() {
      let dt = DateTime.fromISO(this.subscribed);
      return dt.toLocaleString(DateTime.DATE_MED_WITH_WEEKDAY);
    },
  },
  methods: {
    setPlanName() {
      if (this.messagesPerMonth == 100) {
        this.planName = "Bao";
      } else if (this.messagesPerMonth == 300) {
        this.planName = "Mei";
      } else if (this.messagesPerMonth == 1000) {
        this.planName = "Da";
      } else {
        this.planName = "No";
      }
    },
    checkIntegrations() {
      if (this.integrations > 5) {
        this.integrationsMessage = "Access to ALL integrations";
      } else {
        this.integrationsMessage = `Access to ${this.integrations} integrations`;
      }
    },
    setPlanPrice() {
      if (this.planID == "price_1N5ZxSDrmPhl15PT1btIcShL") {
        this.planPrice = "£29.99 per year";
      } else if (this.planID == "price_1N5alADrmPhl15PTFLAFBxTj") {
        this.planPrice = "$29.99 per year";
      } else if (this.planID == "price_1N5ZxSDrmPhl15PTyUrmbeWI") {
        this.planPrice = "£2.99 per month";
      } else if (this.planID == "price_1N5alADrmPhl15PTf8m7V3I2") {
        this.planPrice = "$2.99 per month";
      } else if (this.planID == "price_1N5ZzgDrmPhl15PThFxj0mfm") {
        this.planPrice = "£59.99 per year";
      } else if (this.planID == "price_1N5akmDrmPhl15PT6Rw7OYom") {
        this.planPrice = "$59.99 per year";
      } else if (this.planID == "price_1N5ZzgDrmPhl15PTlkZWtVN7") {
        this.planPrice = "£5.99 per month";
      } else if (this.planID == "price_1N5akmDrmPhl15PToXSoKFUJ") {
        this.planPrice = "$5.99 per month";
      } else if (this.planID == "price_1N5a0sDrmPhl15PTaunA98bh") {
        this.planPrice = "£149.99 per year";
      } else if (this.planID == "price_1N5akRDrmPhl15PTDgdDCmPZ") {
        this.planPrice = "$149.99 per year";
      } else if (this.planID == "price_1N5a0sDrmPhl15PT8n9RF5eI") {
        this.planPrice = "£14.99 per month";
      } else if (this.planID == "price_1N5akRDrmPhl15PTAek44nms") {
        this.planPrice = "$14.99 per month";
      } else {
        this.planPrice = "£N/A";
      }
    },
  },
  components: {
    SpinnerComponent,
  },
};
</script>

<template>
  <div
    class="d-flex flex-column justify-content-center align-items-center text-center"
    v-if="subscriptionMenu"
  >
    <div v-if="this.subscriber == true" class="card mt-2 w-50">
      <div class="card-header">
        <h3 class="mt-2">CURRENT SUBSCRIPTION PACKAGE:</h3>
      </div>
      <div class="card-body">
        <div
          v-if="
            !planName || !messagesPerMonth || !integrationsMessage || !setTime
          "
          class="d-flex flex-column align-items-center"
        >
          <SpinnerComponent :loading="true" class="mt-4"></SpinnerComponent>
          <h3 class="mt-4">LOADING...</h3>
        </div>
        <div v-else>
          <img src="../assets/panda.png" style="width: 100px" />
          <h2 class="mb-4">{{ planName }} Plan</h2>
          <h5>{{ messagesPerMonth }} messages per month</h5>
          <h5 class="mb-4">{{ integrationsMessage }}</h5>
          <h2>{{ planPrice }}</h2>
          <p>You have been a subscriber since {{ setTime }}.</p>
        </div>
      </div>
      <div class="card-footer">
        <a :href="updateSubscriptionLink" target="_blank">
          <button
            class="btn btn-secondary btn-lg mt-3 mb-3 mx-auto"
            style="width: 300px"
          >
            UPDATE SUBSCRIPTION
          </button>
        </a>
      </div>
    </div>
    <div v-else>
      <h1>🐼</h1>
      <h3 class="mt-2 mb-3">
        You are not currently a subscriber, please chose from one of our
        packages below to subscribe:
      </h3>
      <div class="pt-5 pb-5 px-5 w-100 bg-primary" style="border-radius: 20px">
        <stripe-pricing-table
          pricing-table-id="prctbl_1N5aWJDrmPhl15PToGsdMjEU"
          publishable-key="pk_live_51N1wGGDrmPhl15PTItNKJiYismn8j3Ph21nbhPDUnQMw2vHVLOCal4yxtr0TCrI5aXPOGQFy3UoFzXuUJsDWLbsF0096409MMO"
          :client-reference-id="this.formUserId"
          :customer-email="this.formEmail"
        >
        </stripe-pricing-table>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
