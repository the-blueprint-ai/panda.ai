<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data: () => {
    return {
      country: "uk",
      subscriptionPeriod: "monthly",
      recommendedPlan: "mei",
    };
  },
  components: {
    navBar,
    navFooter,
  },
});
</script>

<template>
  <main style="min-height: 71vh">
    <navBar></navBar>
    <div class="container-fluid h-100 bg-primary text-white">
      <div class="container text-center pt-5 pb-5">
        <div class="ukUSA d-flex justify-content-end">
          <div
            class="btn-group btn-group-lg pb-0 mb-n5 me-5"
            role="group"
            aria-label="UK/USA Prices"
          >
            <input
              type="radio"
              class="btn-check"
              name="ukUSA"
              id="uk"
              autocomplete="on"
              checked
              @change="country = 'uk'"
            />
            <label class="btn btn-outline-light px-2 pt-1 pb-1" for="uk"
              ><img src="../assets/icons/united-kingdom.png" width="30"
            /></label>

            <input
              type="radio"
              class="btn-check"
              name="ukUSA"
              id="usa"
              autocomplete="off"
              @change="country = 'usa'"
            />
            <label class="btn btn-outline-light px-2 pt-1 pb-1" for="usa"
              ><img
                src="../assets/icons/united-states-of-america.png"
                width="30"
            /></label>
          </div>
        </div>
        <h1>🐼</h1>
        <h1>PANDA.AI PRICING</h1>
        <div class="monthlyAnnual">
          <div
            class="btn-group btn-group-lg pt-4"
            role="group"
            aria-label="Monthly/Annual Prices"
          >
            <input
              type="radio"
              class="btn-check"
              name="monthlyAnnual"
              id="monthly"
              autocomplete="on"
              checked
              @change="subscriptionPeriod = 'monthly'"
            />
            <label class="btn btn-outline-secondary" for="monthly"
              >MONTHLY</label
            >

            <input
              type="radio"
              class="btn-check"
              name="monthlyAnnual"
              id="annual"
              autocomplete="off"
              @change="subscriptionPeriod = 'annual'"
            />
            <label class="btn btn-outline-secondary" for="annual">ANNUAL</label>
          </div>
        </div>
        <div class="row mb-5">
          <div class="col mb-5">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 18rem"
            >
              <div class="card-header pt-3 pb-3">
                <h2>🐼</h2>
                <h1>FREE</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <div class="subscriptionPlanDetails">
                  <p>20 messages</p>
                  <p class="mt-n3">ALL Integrations</p>
                </div>
                <div v-if="this.subscriptionPeriod === 'monthly'">
                  <h1 class="mt-5"><span v-if="country == 'uk'">£</span><span v-else-if="country == 'usa'">$</span>FREE</h1>
                  <p class="mt-n2">for one month</p>
                </div>
                <div v-if="this.subscriptionPeriod === 'annual'">
                  <h1 class="mt-5"><span v-if="country == 'uk'">£</span><span v-else-if="country == 'usa'">$</span>FREE</h1>
                  <p class="mt-n2">for one month</p>
                </div>
              </div>
              <div class="card-footer pt-4 pb-4">
                <button class="btn btn-secondary" style="width: 150px">
                  START TRIAL
                </button>
              </div>
            </div>
          </div>
          <div class="col mb-5">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 18rem"
            >
              <div class="card-header pt-3 pb-3">
                <h2>🐼</h2>
                <h1>BAO</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <div class="subscriptionPlanDetails">
                  <p>100 messages a month</p>
                  <p class="mt-n3">3 Integrations</p>
                </div>
                <div v-if="this.subscriptionPeriod === 'monthly'">
                  <h1 class="mt-5"><span v-if="country == 'uk'">£</span><span v-else-if="country == 'usa'">$</span>2.99</h1>
                  <p class="mt-n2">per month</p>
                </div>
                <div v-if="this.subscriptionPeriod === 'annual'">
                  <h1 class="mt-5"><span v-if="country == 'uk'">£</span><span v-else-if="country == 'usa'">$</span>29.99</h1>
                  <p class="mt-n2">per year</p>
                </div>
              </div>
              <div class="card-footer pt-4 pb-4">
                <button class="btn btn-secondary" style="width: 150px">
                  SELECT
                </button>
              </div>
            </div>
          </div>
          <div class="col mb-5">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 18rem"
            >
              <div class="card-header pt-3 pb-3">
                <h2>🐼</h2>
                <h1>MEI</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <div class="subscriptionPlanDetails">
                  <p>300 messages a month</p>
                  <p class="mt-n3">5 Integrations</p>
                </div>
                <div v-if="this.subscriptionPeriod === 'monthly'">
                  <h1 class="mt-5"><span v-if="country == 'uk'">£</span><span v-else-if="country == 'usa'">$</span>5.99</h1>
                  <p class="mt-n2">per month</p>
                </div>
                <div v-if="this.subscriptionPeriod === 'annual'">
                  <h1 class="mt-5"><span v-if="country == 'uk'">£</span><span v-else-if="country == 'usa'">$</span>59.99</h1>
                  <p class="mt-n2">per year</p>
                </div>
              </div>
              <div class="card-footer pt-4 pb-4">
                <button class="btn btn-secondary" style="width: 150px">
                  SELECT
                </button>
              </div>
            </div>
          </div>
          <div class="col mb-5">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 18rem"
            >
              <div class="card-header pt-3 pb-3">
                <h2>🐼</h2>
                <h1>DA</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <div class="subscriptionPlanDetails">
                  <p>1,000 messages a month</p>
                  <p class="mt-n3">ALL Integrations</p>
                </div>
                <div v-if="this.subscriptionPeriod === 'monthly'">
                  <h1 class="mt-5"><span v-if="country == 'uk'">£</span><span v-else-if="country == 'usa'">$</span>14.99</h1>
                  <p class="mt-n2">per month</p>
                </div>
                <div v-if="this.subscriptionPeriod === 'annual'">
                  <h1 class="mt-5"><span v-if="country == 'uk'">£</span><span v-else-if="country == 'usa'">$</span>149.99</h1>
                  <p class="mt-n2">per year</p>
                </div>
              </div>
              <div class="card-footer pt-4 pb-4">
                <button class="btn btn-secondary" style="width: 150px">
                  SELECT
                </button>
              </div>
            </div>
          </div>
        </div>
        <h1 class="mt-5">PANDA.AI INTEGRATIONS</h1>
        <div class="row d-inline-flex justify-content-center">
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>VIDEO</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <img src="../assets/panda.png" width="180" />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>
                  🐼 panda.ai will show you videos from YouTube if it helps them
                  answer your question.
                </p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>WIKIPEDIA</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <img src="../assets/panda.png" width="180" />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>
                  🐼 panda.ai can get information from wikipedia if it helps
                  them answer your question.
                </p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>IMAGES</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <img src="../assets/panda.png" width="180" />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>
                  🐼 panda.ai will show you images if it helps them answer your
                  question.
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="row mt-n5 d-inline-flex justify-content-center">
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>MUSIC</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <img src="../assets/panda.png" width="180" />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>🐼 panda.ai can fetch you music from Spotify.</p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>SEARCH</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <img src="../assets/panda.png" width="180" />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>
                  🐼 panda.ai will show you relevant search results if it helps
                  them answer your question.
                </p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>NEWS</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <img src="../assets/panda.png" width="180" />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>
                  🐼 panda.ai can get you the latest news on any topic you ask
                  them about.
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="row mt-n5 d-inline-flex justify-content-center">
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>WEATHER</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <img src="../assets/panda.png" width="180" />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>
                  🐼 panda.ai can get you the weather for anywhere in the world.
                </p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>BOOKS</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <img src="../assets/panda.png" width="180" />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>
                  🐼 panda.ai can fetch you information about any book you're
                  interested in.
                </p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-light text-center mt-5 mb-3"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>SHOPPING</h1>
              </div>
              <div class="card-body pt-5 pb-4 px-5">
                <img src="../assets/panda.png" width="180" />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>🐼 panda.ai will help you get your shopping done.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
