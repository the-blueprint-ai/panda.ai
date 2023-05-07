<script>
import { mapGetters } from "vuex";

export default {
  props: {
    modalId: String,
    country: String,
    subscriptionPeriod: String,
    planType: String,
  },
  computed: {
    ...mapGetters("userStore", {
      userId: "getStoreUserId",
      email: "getStoreEmail",
      first_name: "getStoreFirstName",
      last_name: "getStoreLastName",
    }),
  },
};
</script>

<template>
  <div
    class="modal fade"
    id="subscriptionModal"
    tabindex="-1"
    aria-labelledby="subscriptionModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header text-bg-light d-flex flex-column">
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
          <h1>🐼</h1>
          <h1 class="text-primary">{{ planType.toUpperCase() }} PLAN</h1>
        </div>
        <div class="modal-body text-primary">
          <h2 v-if="planType == 'free'" class="">
            <span v-if="country == 'uk'">£</span
            ><span v-if="country == 'usa'">$</span>{{ planType.toUpperCase() }}
          </h2>
          <h2 v-if="planType == 'bao'" class="">
            <span v-if="country == 'uk'">£</span>
            <span v-if="country == 'usa'">$</span>
            <span v-if="subscriptionPeriod == 'monthly'">2.99 per month</span>
            <span v-if="subscriptionPeriod == 'annual'">29.99 per year</span>
          </h2>
          <h2 v-if="planType == 'mei'" class="">
            <span v-if="country == 'uk'">£</span>
            <span v-if="country == 'usa'">$</span>
            <span v-if="subscriptionPeriod == 'monthly'">5.99 per month</span>
            <span v-if="subscriptionPeriod == 'annual'">59.99 per year</span>
          </h2>
          <h2 v-if="planType == 'da'" class="">
            <span v-if="country == 'uk'">£</span>
            <span v-if="country == 'usa'">$</span>
            <span v-if="subscriptionPeriod == 'monthly'">14.99 per month</span>
            <span v-if="subscriptionPeriod == 'annual'">149.99 per year</span>
          </h2>
          <div class="text-primary mb-4" v-if="planType == 'free'">
            <p class="lh-1">20 messages</p>
            <p class="lh-1 mt-n2">ALL Integrations</p>
          </div>
          <div class="text-primary mb-4" v-if="planType == 'bao'">
            <p class="lh-1">100 messages a month</p>
            <p class="lh-1 mt-n2">3 Integrations</p>
          </div>
          <div class="text-primary mb-4" v-if="planType == 'mei'">
            <p class="lh-1">300 messages a month</p>
            <p class="lh-1 mt-n2">5 Integrations</p>
          </div>
          <div class="text-primary mb-4" v-if="planType == 'da'">
            <p class="lh-1">1,000 messages a month</p>
            <p class="lh-1 mt-n2">ALL Integrations</p>
          </div>
          <form>
            <div class="d-flex">
              <div class="form-floating mb-3" style="width: 48%">
                <input
                  type="text"
                  class="form-control"
                  id="firstName"
                  placeholder="Po"
                />
                <label for="firstName">{{ this.first_name }}</label>
              </div>
              <div class="form-floating mb-3 ms-3" style="width: 48%">
                <input
                  type="text"
                  class="form-control"
                  id="lastName"
                  placeholder="Ping"
                />
                <label for="lastName">{{ this.last_name }}</label>
              </div>
            </div>
            <div class="form-floating mb-3">
              <input
                type="email"
                class="form-control"
                id="email"
                placeholder="Po.Ping@mypanda.ai"
              />
              <label for="email">{{ this.email }}</label>
            </div>
          </form>
        </div>
        <div class="modal-footer text-bg-light">
          <button type="button" class="btn btn-secondary">NEXT</button>
        </div>
      </div>
    </div>
  </div>
</template>
