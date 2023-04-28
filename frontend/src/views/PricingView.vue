<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data: () => {
    return {
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
  <main>
    <navBar></navBar>
    <div class="body">
      <div class="pricingView">
        <div>
          <h2>🐼</h2>
          <h1>PANDA.AI PRICING</h1>
        </div>
        <div class="subscriptionPeriod">
          <h2
            class="subscriptionPeriodMonthly"
            @click="this.subscriptionPeriod = 'monthly'"
            :class="{ selected: subscriptionPeriod === 'monthly' }"
          >
            Monthly
          </h2>
          <h2
            class="subscriptionPeriodAnnual"
            @click="this.subscriptionPeriod = 'annual'"
            :class="{ selected: subscriptionPeriod === 'annual' }"
          >
            Annual
          </h2>
        </div>
        <div class="pricingContainer">
          <div class="subscriptionPlan">
            <h2 v-if="this.recommendedPlan === 'free'" class="recommendedPlan">
              RECOMMENDED
            </h2>
            <div
              class="subscriptionPlanContainer"
              :class="{ recommended: recommendedPlan === 'free' }"
            >
              <h2>🐼</h2>
              <h1>FREE</h1>
              <div class="subscriptionPlanDetails">
                <p>20 messages</p>
                <p>ALL Integrations</p>
              </div>
              <div v-if="this.subscriptionPeriod === 'monthly'">
                <h1>£FREE</h1>
                <p>for one month</p>
              </div>
              <div v-if="this.subscriptionPeriod === 'annual'">
                <h1>£FREE</h1>
                <p>for one month</p>
              </div>
              <div v-if="session">
                <router-link :to="'/auth/' + userId + '/chat'">
                  <button class="subscriptionSelect">START TRIAL</button>
                </router-link>
              </div>
              <div v-else>
                <router-link :to="'/signin'">
                  <button class="subscriptionSelect">START TRIAL</button>
                </router-link>
              </div>
            </div>
          </div>
          <div class="subscriptionPlan">
            <h2 v-if="this.recommendedPlan === 'bao'" class="recommendedPlan">
              RECOMMENDED
            </h2>
            <div
              class="subscriptionPlanContainer"
              :class="{ recommended: recommendedPlan === 'bao' }"
            >
              <h2>🐼</h2>
              <h1>BAO</h1>
              <div class="subscriptionPlanDetails">
                <p>100 messages a month</p>
                <p>3 Integrations</p>
              </div>
              <div v-if="this.subscriptionPeriod === 'monthly'">
                <h1>£2.99</h1>
                <p>per month</p>
              </div>
              <div v-if="this.subscriptionPeriod === 'annual'">
                <h1>£29.99</h1>
                <p>per year</p>
              </div>
              <div v-if="session">
                <router-link :to="'/auth/' + userId + '/chat'">
                  <button class="subscriptionSelect">SELECT</button>
                </router-link>
              </div>
              <div v-else>
                <router-link :to="'/signin'">
                  <button class="subscriptionSelect">SELECT</button>
                </router-link>
              </div>
            </div>
          </div>
          <div class="subscriptionPlan">
            <h2 v-if="this.recommendedPlan === 'mei'" class="recommendedPlan">
              RECOMMENDED
            </h2>
            <div
              class="subscriptionPlanContainer"
              :class="{ recommended: recommendedPlan === 'mei' }"
            >
              <h2>🐼</h2>
              <h1>MEI</h1>
              <div class="subscriptionPlanDetails">
                <p>300 messages a month</p>
                <p>5 Integrations</p>
              </div>
              <div v-if="this.subscriptionPeriod === 'monthly'">
                <h1>£5.99</h1>
                <p>per month</p>
              </div>
              <div v-if="this.subscriptionPeriod === 'annual'">
                <h1>£59.99</h1>
                <p>per year</p>
              </div>
              <div v-if="session">
                <router-link :to="'/auth/' + userId + '/chat'">
                  <button class="subscriptionSelect">SELECT</button>
                </router-link>
              </div>
              <div v-else>
                <router-link :to="'/signin'">
                  <button class="subscriptionSelect">SELECT</button>
                </router-link>
              </div>
            </div>
          </div>
          <div class="subscriptionPlan">
            <h2 v-if="this.recommendedPlan === 'da'" class="recommendedPlan">
              RECOMMENDED
            </h2>
            <div
              class="subscriptionPlanContainer"
              :class="{ recommended: recommendedPlan === 'da' }"
            >
              <h2>🐼</h2>
              <h1>DA</h1>
              <div class="subscriptionPlanDetails">
                <p>1,000 messages a month</p>
                <p>ALL Integrations</p>
              </div>
              <div v-if="this.subscriptionPeriod === 'monthly'">
                <h1>£14.99</h1>
                <p>per month</p>
              </div>
              <div v-if="this.subscriptionPeriod === 'annual'">
                <h1>£149.99</h1>
                <p>per year</p>
              </div>
              <div v-if="session">
                <router-link :to="'/auth/' + userId + '/chat'">
                  <button class="subscriptionSelect">SELECT</button>
                </router-link>
              </div>
              <div v-else>
                <router-link :to="'/signin'">
                  <button class="subscriptionSelect">SELECT</button>
                </router-link>
              </div>
            </div>
          </div>
        </div>
        <div class="integrationsContainer">
          <h1>PANDA.AI INTEGRATIONS</h1>
          <div class="integrationsRow">
            <div class="integrationsItem">
              <h1>VIDEO</h1>
              <img src="../assets/panda.png" />
              <p>
                🐼 panda.ai will show you videos from YouTube if it helps them
                answer your question
              </p>
            </div>
            <div class="integrationsItem">
              <h1>WIKIPEDIA</h1>
              <img src="../assets/panda.png" />
              <p>
                🐼 panda.ai can get information from wikipedia if it helps them
                answer your question
              </p>
            </div>
            <div class="integrationsItem">
              <h1>IMAGES</h1>
              <img src="../assets/panda.png" />
              <p>
                🐼 panda.ai will show you images if it helps them answer your
                question
              </p>
            </div>
          </div>
          <div class="integrationsRow">
            <div class="integrationsItem">
              <h1>MUSIC</h1>
              <img src="../assets/panda.png" />
              <p>🐼 panda.ai can fetch you music from Spotify</p>
            </div>
            <div class="integrationsItem">
              <h1>SEARCH</h1>
              <img src="../assets/panda.png" />
              <p>
                🐼 panda.ai will show you relevant search results if it helps
                them answer your question
              </p>
            </div>
            <div class="integrationsItem">
              <h1>NEWS</h1>
              <img src="../assets/panda.png" />
              <p>
                🐼 panda.ai can get you the latest news on any topic you ask
                them about
              </p>
            </div>
          </div>
          <div class="integrationsRow">
            <div class="integrationsItem">
              <h2 class="comingSoon">COMING SOON</h2>
              <h1>WEATHER</h1>
              <img src="../assets/panda.png" />
              <p>
                🐼 panda.ai can get you the weather for anywhere in the world
              </p>
            </div>
            <div class="integrationsItem">
              <h2 class="comingSoon">COMING SOON</h2>
              <h1>BOOKS</h1>
              <img src="../assets/panda.png" />
              <p>
                🐼 panda.ai can fetch you information about any book you're
                interested in
              </p>
            </div>
            <div class="integrationsItem">
              <h2 class="comingSoon">COMING SOON</h2>
              <h1>SHOPPING</h1>
              <img src="../assets/panda.png" />
              <p>🐼 panda.ai will help you get your shopping done</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
