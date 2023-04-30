<script>
import { defineComponent } from "vue";
import { mapGetters } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { getRoadmap } from "../composables/getRoadmap.js";
import SpinnerComponent from "../components/spinnerComponent.vue";

export default defineComponent({
  data() {
    return {
      roadmapOverlay: false,
      email: "",
      roadmapSuggestion: "",
      newIdeaId: 0,
      displayBuiltItemsCount: 6,
      loading: false,
      notifyMeButtonText: "NOTIFY ME",
    };
  },
  async mounted() {
    await getRoadmap(this.$store, "roadmap");
  },
  computed: {
    ...mapGetters("roadmapStore", {
      getRoadmapData: "getRoadmapData",
    }),
    roadmapData() {
      return this.getRoadmapData || [];
    },
    builtItems() {
      return this.roadmapData
        .filter((item) => item.tags.includes("built"))
        .reverse();
    },
    displayedBuiltItems() {
      return this.builtItems.slice(0, this.displayBuiltItemsCount);
    },
    notBuiltItems() {
      return this.roadmapData.filter((item) => !item.tags.includes("built"));
    },
    sortedNotBuiltItems() {
      return [...this.notBuiltItems].sort((a, b) => b.votes - a.votes);
    },
  },
  methods: {
    activateOverlay() {
      this.roadmapOverlay = !this.roadmapOverlay;
    },
    showMoreItems() {
      this.displayBuiltItemsCount += 4;
    },
    showLessItems() {
      this.displayBuiltItemsCount = 6;
    },
    async addIdea(idea) {
      try {
        const url =
          import.meta.env.VITE_APP_API_URL + "/roadmap/add-idea?idea=" + idea;
        const res = await fetch(url, {
          method: "PUT",
        });

        const data = await res.json(); // get the response data from the server
        this.newIdeaId = data.roadmap_id; // set the newIdeaId to the returned roadmap_id
        this.roadmapSuggestion = "";
        this.activateOverlay();

        if (!res.ok) {
          throw new Error(`Server responded with status ${res.status}`);
        }
      } catch (error) {
        console.log("An error occurred while upvoting the item:", error);
      }
    },
    async addEmail(id, email) {
      try {
        const url =
          import.meta.env.VITE_APP_API_URL +
          "/roadmap/add-email?id=" +
          id +
          "&email=" +
          email;
        const res = await fetch(url, {
          method: "PUT",
        });

        this.email = "";
        this.activateOverlay();

        if (!res.ok) {
          throw new Error(`Server responded with status ${res.status}`);
        }
      } catch (error) {
        console.log("An error occurred while upvoting the item:", error);
      }
    },
    async upvoteItem(item) {
      try {
        const url =
          import.meta.env.VITE_APP_API_URL +
          "/roadmap/upvote?id=" +
          item.roadmap_id;
        const res = await fetch(url, {
          method: "PUT",
        });

        if (!res.ok) {
          throw new Error(`Server responded with status ${res.status}`);
        }

        const updatedItem = await res.json();
        const index = this.roadmapData.findIndex(
          (i) => i.id === updatedItem.id
        );
        this.roadmapData[index] = updatedItem;
      } catch (error) {
        console.log("An error occurred while upvoting the item:", error);
      }
    },
  },
  components: {
    navBar,
    navFooter,
    SpinnerComponent,
  },
});
</script>

<template>
  <main style="min-height: 71vh">
    <navBar></navBar>
    <div class="container-fluid h-100 bg-primary text-white">
      <div
        class="container text-center d-flex flex-column justify-content-center pt-5 pb-5"
      >
        <h1>🐼</h1>
        <h1>PANDA.AI PRODUCT ROADMAP</h1>
        <h4 class="mt-4">
          Upvote the features you like and we’ll notify you once they've
          launched...
        </h4>
        <div v-if="roadmapData.length > 0" class="">
          <div class="row mt-5">
            <div
              class="col d-flex justify-content-center"
              v-for="item in sortedNotBuiltItems"
              :key="item.name"
            >
              <div
                class="card text-bg-dark text-center mb-3 border-primary"
                style="width: 35rem"
              >
                <div class="card-header pt-3 pb-3 border-primary">
                  <h2 class="text-uppercase">{{ item.name }}</h2>
                  <div
                    class="btn btn-secondary mt-2 mb-1 me-3 d-inline-flex justify-content-center align-items-center"
                    v-if="item.tags.includes('built')"
                  >
                    <p class="text-uppercase" style="height: 10px">built</p>
                    <img
                      src="../assets/icons/check-circle-fill.svg"
                      class="ms-3 mt-n1"
                    />
                  </div>
                  <div
                    class="btn btn-secondary mt-2 mb-1 me-3 d-inline-flex justify-content-center align-items-center"
                    v-if="item.tags.includes('in progress')"
                  >
                    <p class="text-uppercase" style="height: 10px">
                      in progress
                    </p>
                    <img
                      src="../assets/icons/fast-forward-circle-fill.svg"
                      class="ms-3 mt-n1"
                    />
                  </div>
                  <div
                    class="btn btn-secondary mt-2 mb-1 d-inline-flex justify-content-center align-items-center"
                    v-if="item.tags.includes('newly added')"
                  >
                    <p class="text-uppercase" style="height: 10px">
                      newly added
                    </p>
                    <img
                      src="../assets/icons/star-fill.svg"
                      class="ms-3 mt-n1"
                    />
                  </div>
                </div>
                <div class="card-body pt-4 pb-2 px-3 border-primary">
                  <p>{{ item.description }}</p>
                </div>
                <div class="card-footer pt-4 pb-4 border-primary">
                  <div
                    v-if="!item.tags.includes('built')"
                    class="d-flex align-items-center justify-content-center"
                  >
                    <button
                      class="btn btn-secondary btn-lg d-inline-flex justify-content-between px-3"
                      @click="upvoteItem(item)"
                      style="height: 50px; width: 200px"
                    >
                      <img
                        src="../assets/icons/arrow-up-circle-fill.svg"
                        class="mt-1"
                        width="26"
                      />
                      <p
                        class="text-uppercase d-inline-flex align-items-center"
                      >
                        Upvote
                      </p>
                      <p class="" id="roadmapItemVotes">
                        <strong>{{ item.votes }}</strong>
                      </p>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row mt-5 d-flex justify-content-center">
          <div
            class="card text-bg-dark text-center mb-3 border-primary"
            style="width: 45rem"
          >
            <div class="card-header pt-3 pb-3 border-primary">
              <h2>OTHER</h2>
            </div>
            <div class="card-body pt-4 pb-2 px-3 border-primary">
              <p>
                If you have any great ideas and would like something added to
                our roadmap, please type in the field below. We’ll notify you
                once it is available.
              </p>
            </div>
            <div class="card-footer pt-4 pb-4 border-primary">
              <div class="form-floating">
                <textarea
                  class="form-control"
                  id="floatingTextarea"
                  v-model="roadmapSuggestion"
                  placeholder="🐼 please submit your ideas here!"
                  @keyup.enter="addIdea(roadmapSuggestion)"
                ></textarea>
                <label for="floatingTextarea" class="text-primary"
                  >🐼 please submit your ideas here!</label
                >
              </div>
              <button
                v-if="roadmapSuggestion.length > 0"
                class="btn btn-secondary mt-3"
                @click="addIdea(roadmapSuggestion)"
              >
                Submit
              </button>
              <button v-else class="btn btn-secondary btn-lg mt-3">
                Submit
              </button>
            </div>
          </div>
        </div>
        <h1 class="text-center mt-5">BUILT FEATURES</h1>
        <div class="row mt-5">
          <div
            class="col d-flex justify-content-center"
            v-for="item in displayedBuiltItems"
            :key="item.name"
          >
            <div
              class="card text-bg-dark text-center mb-3 border border-secondary"
              style="width: 35rem"
            >
              <div class="card-header pt-3 pb-3">
                <h2 class="text-uppercase">{{ item.name }}</h2>
                <div
                  class="btn btn-secondary mt-2 mb-1 me-3 d-inline-flex justify-content-center align-items-center"
                  v-if="item.tags.includes('built')"
                >
                  <p class="text-uppercase" style="height: 10px">built</p>
                  <img
                    src="../assets/icons/check-circle-fill.svg"
                    class="ms-3 mt-n1"
                  />
                </div>
                <div
                  class="btn btn-secondary mt-2 mb-1 me-3 d-inline-flex justify-content-center align-items-center"
                  v-if="item.tags.includes('in progress')"
                >
                  <p class="text-uppercase" style="height: 10px">in progress</p>
                  <img
                    src="../assets/icons/fast-forward-circle-fill.svg"
                    class="ms-3 mt-n1"
                  />
                </div>
                <div
                  class="btn btn-secondary mt-2 mb-1 d-inline-flex justify-content-center align-items-center"
                  v-if="item.tags.includes('newly added')"
                >
                  <p class="text-uppercase" style="height: 10px">newly added</p>
                  <img src="../assets/icons/star-fill.svg" class="ms-3 mt-n1" />
                </div>
              </div>
              <div class="card-body pt-4 pb-2 px-3">
                <p>{{ item.description }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="d-inline-flex justify-content-center">
          <button
            class="btn btn-secondary btn-lg mt-5"
            v-if="displayBuiltItemsCount < builtItems.length"
            @click="showMoreItems"
            style="width: 800px"
          >
            SEE MORE...
          </button>
          <button
            class="btn btn-secondary btn-lg mt-5"
            v-if="displayBuiltItemsCount == builtItems.length"
            @click="showLessItems"
            style="width: 800px"
          >
            SEE LESS...
          </button>
        </div>
      </div>
      <div
        id="roadmapOverlay"
        class="roadmapOverlay"
        :class="{ active: roadmapOverlay }"
      >
        <div
          class="card text-bg-dark text-center mb-3 border-secondary"
          style="height: 450px; width: 35rem"
        >
          <div class="card-header pt-3 pb-3 border-primary">
            <h1>🐼</h1>
            <h2>THANKS FOR THE FEEDBACK!</h2>
          </div>
          <div class="card-body pt-4 px-3 border-primary">
            <p>
              We’re doing our best to add the new features you want. Please
              share your email address and we’ll notify you as we make progress!
            </p>
          </div>
          <div
            class="card-footer pt-4 pb-4 border-primary d-inline-flex justify-content-center align-items-center"
          >
            <div class="form-floating mb-3">
              <input
                type="email"
                ref="email"
                v-model="this.email"
                class="form-control me-2"
                id="floatingInput"
                placeholder="kung-fu@panda.ai"
                @keyup.enter="addEmail(this.newIdeaId, this.email)"
                autocomplete="email"
                required
                style="width: 350px"
              />
              <label for="floatingInput" class="text-primary"
                >Enter your email address</label
              >
            </div>
            <button
              class="btn btn-secondary ms-2 mt-n3 d-inline-flex justify-content-center"
              @click="addEmail(this.newIdeaId, this.email)"
            >
              <SpinnerComponent
                :loading="this.loading"
                :button-text="this.notifyMeButtonText"
              ></SpinnerComponent>
            </button>
          </div>
          <button
            class="btn btn-outline-secondary mb-5 mt-n2 mx-auto"
            @click="this.activateOverlay()"
            style="width: 200px"
          >
            CLOSE
          </button>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
.roadmapOverlay {
  display: none;
}
.roadmapOverlay.active {
  display: flex;
  justify-content: center;
  padding-top: 200px;
  height: 100%;
  width: 100%;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  background-color: rgba(255, 255, 255, 0.8);
  overflow: hidden;
}
</style>
