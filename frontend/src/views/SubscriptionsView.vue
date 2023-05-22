<script>
import { defineComponent } from "vue";
import { mapGetters } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data: () => {
    return {
      country: "uk",
      subscriptionPeriod: "monthly",
      currentPlanType: "free",
      formUserId: "",
      formEmail: "",
    };
  },
  mounted() {},
  created() {
    this.formUserId = this.userId;
    this.formEmail = this.email;
  },
  computed: {
    ...mapGetters("userStore", {
      userId: "getStoreUserId",
      email: "getStoreEmail",
    }),
    isOpen() {
      return this.$store.state.isOpen;
    },
  },
  methods: {
    toSignIn() {
      this.$router.push("/signin");
    },
    setPlanType(planType) {
      this.currentPlanType = planType;
    },
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
    <div class="container-fluid bg-primary text-white">
      <div class="container text-center pt-5 pb-5">
        <h1 class="mb-4">PANDA.AI SUBSCRIPTIONS</h1>
        <div class="mb-4">
          <stripe-pricing-table
            pricing-table-id="prctbl_1N5aWJDrmPhl15PToGsdMjEU"
            publishable-key="pk_live_51N1wGGDrmPhl15PTItNKJiYismn8j3Ph21nbhPDUnQMw2vHVLOCal4yxtr0TCrI5aXPOGQFy3UoFzXuUJsDWLbsF0096409MMO"
            :client-reference-id="this.formUserId"
            :customer-email="this.formEmail"
          >
          </stripe-pricing-table>
        </div>
        <h1 class="mt-5 mb-4">PANDA.AI INTEGRATIONS</h1>
        <div class="row d-inline-flex justify-content-center">
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-dark text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>VIDEO</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/screenshots/new-rockstars-video.png"
                  width="100%"
                />
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
              class="card text-bg-dark text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>MAPS</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/screenshots/new-york-map.png"
                  width="100%"
                />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>🐼 panda.ai can get you maps for anywhere in the world.</p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-dark text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>IMAGES</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/screenshots/panda-images.png"
                  width="100%"
                />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>
                  🐼 panda.ai will show you images if it helps them answer your
                  question.
                </p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-dark text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>WIKIPEDIA</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/screenshots/thom-yorke-wikipedia.png"
                  width="100%"
                />
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
              class="card text-bg-dark text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>SEARCH</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/screenshots/openai-search.png"
                  width="100%"
                />
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
              class="card text-bg-dark text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>NEWS</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/screenshots/local-election-news.png"
                  width="100%"
                />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>
                  🐼 panda.ai can get you the latest news on any topic you ask
                  them about.
                </p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-dark text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>MUSIC</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/screenshots/radiohead-music.png"
                  width="100%"
                />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>🐼 panda.ai can fetch you music from Spotify.</p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-dark text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>MOVIES & TV SHOWS</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/screenshots/movie-inception.png"
                  width="80%"
                />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>
                  🐼 panda.ai can fetch you information on any Movie or TV Show.
                </p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-dark text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header pt-4 pb-3">
                <h1>ACTORS</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/screenshots/actor-tom-holland.png"
                  width="80%"
                />
              </div>
              <div class="card-footer pt-4 pb-2">
                <p>🐼 panda.ai can fetch you information on any Actors.</p>
              </div>
            </div>
          </div>
          <div class="col d-inline-flex justify-content-center">
            <div
              class="card text-bg-dark border-secondary text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header text-bg-secondary pt-4 pb-3">
                <h4>COMING SOON</h4>
                <h1>WEATHER</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/panda.png"
                  width="80%"
                />
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
              class="card text-bg-dark border-secondary text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header text-bg-secondary pt-4 pb-3">
                <h4>COMING SOON</h4>
                <h1>BOOKS</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/panda.png"
                  width="80%"
                />
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
              class="card text-bg-dark border-secondary text-center mx-1 mt-1 mb-4"
              style="width: 25rem"
            >
              <div class="card-header text-bg-secondary pt-4 pb-3">
                <h4>COMING SOON</h4>
                <h1>SHOPPING</h1>
              </div>
              <div
                class="card-body pt-4 pb-4 px-3 d-flex justify-content-center align-items-center"
              >
                <img
                  class="img-thumbnail"
                  src="../assets/panda.png"
                  width="80%"
                />
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

<style scoped>
@media (max-width: 576px) {
  .ukUSA {
    justify-content: center !important;
    margin-left: 50px;
  }
}
</style>
