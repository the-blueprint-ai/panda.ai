<script>
import { defineComponent } from "vue";
import { mapGetters } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { getRoadmap } from "../composables/getRoadmap.js";
import { sendEmail } from "../composables/sendEmail.js";
import roadmap_request_html from "../assets/emails/roadmapRequestEmail.js";
import roadmap_send_html from "../assets/emails/roadmapSendEmail.js";
import SpinnerComponent from "../components/spinnerComponent.vue";
import { useToast } from "vue-toastification";

export default defineComponent({
  data() {
    return {
      roadmapOverlay: false,
      email: "",
      roadmapSuggestion: "",
      emailRoadmapSuggestion: "",
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
      return [...this.notBuiltItems].sort((a, b) =>
        a.name.localeCompare(b.name)
      );
    },
  },
  methods: {
    async sendRoadmapEmails(to_email, message) {
      const toast = useToast();
      this.loading = true;
      const roadmap_message = roadmap_send_html(to_email, message);
      try {
        await sendEmail(
          "support@mypanda.ai",
          to_email,
          "Thank you for your suggestion!",
          roadmap_request_html
        );
        await sendEmail(
          "website@mypanda.ai",
          "support@mypanda.ai",
          "New Roadmap Idea Submitted",
          roadmap_message
        );
        toast.success("Email sent!");
        this.loading = false;
        this.notifyMeButtonText = "SENT!";
      } catch (error) {
        toast.error("An error occurred while sending the emails:", error);
        this.failedSend = true;
        setTimeout(() => (this.failedSend = false), 2000);
      } finally {
        setTimeout(() => (this.buttonText = "NOTIFY ME"), 2000);
        setTimeout(() => (this.email = ""), 2000);
        setTimeout(() => (this.roadmapSuggestion = ""), 2000);
      }
    },
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
      const toast = useToast();
      try {
        const url =
          import.meta.env.VITE_APP_API_URL + "/roadmap/add-idea?idea=" + idea;
        const res = await fetch(url, {
          method: "PUT",
        });

        const data = await res.json(); // get the response data from the server
        this.newIdeaId = data.roadmap_id; // set the newIdeaId to the returned roadmap_id
        this.emailRoadmapSuggestion = this.roadmapSuggestion;
        this.roadmapSuggestion = "";

        if (!res.ok) {
          toast.error(`Server responded with status ${res.status}`);
        }
      } catch (error) {
        toast.error("An error occurred while upvoting the item:", error);
      }
    },
    async addEmail(id, email) {
      const toast = useToast();
      await this.sendRoadmapEmails(email, this.emailRoadmapSuggestion);
      this.emailRoadmapSuggestion = "";
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

        if (!res.ok) {
          toast.error(`Server responded with status ${res.status}`);
        }
      } catch (error) {
        toast.error("An error occurred while upvoting the item:", error);
      }
    },
    async upvoteItem(item) {
      const toast = useToast();
      try {
        const url =
          import.meta.env.VITE_APP_API_URL +
          "/roadmap/upvote?id=" +
          item.roadmap_id;
        const res = await fetch(url, {
          method: "PUT",
        });

        if (!res.ok) {
          toast.error(`Server responded with status ${res.status}`);
        }

        const updatedItem = await res.json();
        const index = this.roadmapData.findIndex(
          (i) => i.roadmap_id === updatedItem.roadmap_id
        );
        this.roadmapData.splice(index, 1, updatedItem);
      } catch (error) {
        toast.error("An error occurred while upvoting the item:", error);
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
  <main>
    <navBar></navBar>
    <div class="container-fluid bg-primary text-white">
      <div
        class="container text-center d-flex flex-column justify-content-center pt-5 pb-5"
      >
        <h1>🐼</h1>
        <h1>PANDA.AI PRODUCT ROADMAP</h1>
        <h4 class="mt-4 mb-5">
          Upvote the features you like and we’ll notify you once they've
          launched...
        </h4>
        <div
          v-if="roadmapData.length > 0"
          class="d-flex flex-row flex-wrap justify-content-around"
        >
          <div
            class="d-flex justify-content-center"
            v-for="item in sortedNotBuiltItems"
            :key="item.name"
          >
            <div
              class="roadMapCard card d-flex text-bg-dark text-center mb-4 border-primary"
            >
              <div class="card-header pt-3 pb-3 border-primary">
                <h2 class="text-uppercase">{{ item.name }}</h2>
                <div
                  class="badge rounded-pill text-bg-secondary mt-2 mb-1 me-3 d-inline-flex justify-content-center align-items-center"
                  v-if="item.tags.includes('built')"
                >
                  <p class="text-uppercase ms-1 pt-2" style="height: 11px">
                    built
                  </p>
                  <img
                    src="../assets/icons/check-circle-fill.svg"
                    class="ms-2 mt-n1"
                  />
                </div>
                <div
                  class="badge rounded-pill text-bg-secondary mt-2 mb-1 me-3 d-inline-flex justify-content-center align-items-center"
                  v-if="item.tags.includes('in progress')"
                >
                  <p class="text-uppercase ms-1 pt-2" style="height: 11px">
                    in progress
                  </p>
                  <img
                    src="../assets/icons/fast-forward-circle-fill.svg"
                    class="ms-2 mt-n1"
                  />
                </div>
                <div
                  class="badge rounded-pill text-bg-secondary d-inline-flex justify-content-center align-items-center"
                  v-if="item.tags.includes('newly added')"
                >
                  <p class="text-uppercase ms-1 pt-2" style="height: 11px">
                    newly added
                  </p>
                  <img src="../assets/icons/star-fill.svg" class="ms-2" />
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
                    <p class="text-uppercase d-inline-flex align-items-center">
                      Upvote
                    </p>
                    <p class="" id="roadmapItemVotes">
                      {{ item.votes }}
                    </p>
                  </button>
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
                ></textarea>
                <label for="floatingTextarea" class="text-primary"
                  >🐼 please submit your ideas here!</label
                >
              </div>
              <button
                v-if="roadmapSuggestion.length > 0"
                class="btn btn-secondary mt-3"
                data-bs-toggle="modal"
                data-bs-target="#addRoadmapModal"
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
                  class="badge rounded-pill text-bg-secondary mt-2 mb-1 me-3 d-inline-flex justify-content-center align-items-center"
                  v-if="item.tags.includes('built')"
                >
                  <p class="text-uppercase ms-1 pt-2" style="height: 11px">
                    built
                  </p>
                  <img
                    src="../assets/icons/check-circle-fill.svg"
                    class="ms-2"
                  />
                </div>
                <div
                  class="badge rounded-pill text-bg-secondary mt-2 mb-1 me-3 d-inline-flex justify-content-center align-items-center"
                  v-if="item.tags.includes('in progress')"
                >
                  <p class="text-uppercase ms-1 pt-2" style="height: 11px">
                    in progress
                  </p>
                  <img
                    src="../assets/icons/fast-forward-circle-fill.svg"
                    class="ms-2"
                  />
                </div>
                <div
                  class="badge rounded-pill text-bg-secondary mt-2 mb-1 d-inline-flex justify-content-center align-items-center"
                  v-if="item.tags.includes('newly added')"
                >
                  <p class="text-uppercase ms-1 pt-2" style="height: 11px">
                    newly added
                  </p>
                  <img src="../assets/icons/star-fill.svg" class="ms-2" />
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
        class="modal fade"
        id="addRoadmapModal"
        tabindex="-1"
        aria-labelledby="addRoadmapModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-dialog-centered" ref="addRoadmapModal">
          <div class="modal-content text-primary">
            <div class="modal-header">
              <h4 class="modal-title" id="addRoadmapModalLabel">
                THANKS FOR THE FEEDBACK!
              </h4>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body text-center">
              <h1>🐼</h1>
              <p>
                We’re doing our best to add the new features you want. Please
                share your email address and we’ll notify you as we make
                progress!
              </p>
              <div class="form-floating mb-2">
                <input
                  type="email"
                  ref="email"
                  v-model="this.email"
                  class="form-control me-2"
                  id="floatingInput"
                  placeholder="kung-fu@panda.ai"
                  autocomplete="email"
                  required
                />
                <label for="floatingInput">Enter your email address...</label>
              </div>
            </div>
            <div class="modal-footer">
              <button
                @click="addEmail(this.newIdeaId, this.email)"
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                <SpinnerComponent
                  :loading="this.loading"
                  :button-text="this.notifyMeButtonText"
                ></SpinnerComponent>
              </button>
            </div>
          </div>
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
@media (min-width: 1200px) {
  .roadMapCard {
    width: 500px;
  }
}
@media (min-width: 576px) {
  .roadMapCard {
    width: 400px;
  }
}
@media (max-width: 576px) {
  .roadMapCard {
    width: 300px;
  }
}
</style>
