<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {
      roadmapOverlay: false,
      email: "",
      roadmapSuggestion: "",
      roadmapData: [
        {
          name: "Feature 1",
          description: "This is a description for Feature 1.",
          votes: 15,
          tags: ["built"],
          createdAt: "2023-03-22T18:30:00.000Z",
        },
        {
          name: "Feature 2",
          description: "This is a description for Feature 2.",
          votes: 32,
          tags: ["newly added"],
          createdAt: "2023-03-25T10:45:00.000Z",
        },
        {
          name: "Feature 3",
          description: "This is a description for Feature 3.",
          votes: 8,
          tags: ["in progress", "newly added"],
          createdAt: "2023-03-20T12:15:00.000Z",
        },
        {
          name: "Feature 4",
          description: "This is a description for Feature 4.",
          votes: 47,
          tags: ["built"],
          createdAt: "2023-03-28T16:00:00.000Z",
        },
        {
          name: "Feature 5",
          description: "This is a description for Feature 5.",
          votes: 26,
          tags: ["built"],
          createdAt: "2023-03-18T20:30:00.000Z",
        },
      ],
    };
  },
  computed: {
    builtItems() {
      return this.roadmapData.filter((item) => item.tags.includes("built"));
    },
    notBuiltItems() {
      return this.roadmapData.filter((item) => !item.tags.includes("built"));
    },
  },
  methods: {
    activateOverlay() {
      this.roadmapOverlay = !this.roadmapOverlay;
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
    <div class="body">
      <div>
        <h1>🐼</h1>
        <div class="roadmapTitle">
          <h1>panda.ai Product Roadmap</h1>
          <h2>
            Upvote the features you like and we’ll notify you once they've
            launched...
          </h2>
        </div>
        <div class="roadmapContainer">
          <div
            class="roadmapItem"
            v-for="item in notBuiltItems"
            :key="item.name"
          >
            <div class="roadmapItemRow1">
              <div class="roadmapItemTitle">
                <h2>{{ item.name }}</h2>
              </div>
              <div class="roadmapItemTags">
                <div class="roadmapItemTag" v-if="item.tags.includes('built')">
                  <p>built</p>
                  <img src="../assets/icons/check-circle-fill.svg" />
                </div>
                <div
                  class="roadmapItemTag"
                  v-if="item.tags.includes('in progress')"
                >
                  <p>in progress</p>
                  <img src="../assets/icons/fast-forward-circle-fill.svg" />
                </div>
                <div
                  class="roadmapItemTag"
                  v-if="item.tags.includes('newly added')"
                >
                  <p>newly added</p>
                  <img src="../assets/icons/star-fill.svg" />
                </div>
              </div>
            </div>
            <div class="roadmapItemRow2">
              <div class="roadmapItemDescription">
                <p>{{ item.description }}</p>
              </div>
            </div>
            <div v-if="!item.tags.includes('built')" class="roadmapItemRow3">
              <div class="roadmapItemVote">
                <button>
                  <img src="../assets/icons/arrow-up-circle-fill.svg" />
                  <p>Upvote</p>
                  <p id="roadmapItemVotes">{{ item.votes }}</p>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="roadmapContainer">
          <div class="roadmapItem">
            <div class="roadmapItemRow1">
              <div class="roadmapItemTitle">
                <h2>Other</h2>
              </div>
            </div>
            <div class="roadmapItemRow2">
              <div class="roadmapItemDescription">
                <p>
                  If you have any great ideas and would like something added to
                  our roadmap, please type in the field below. We’ll notify you
                  once it is available.
                </p>
              </div>
            </div>
            <div class="roadmapItemRow3">
              <div class="roadmapItemSubmit">
                <input v-model="roadmapSuggestion" placeholder="please submit your ideas here!" />
                <button v-if="roadmapSuggestion.length > 0" @click="activateOverlay">Submit</button>
                <button v-else>Submit</button>
              </div>
            </div>
          </div>
        </div>
        <div class="roadmapContainer">
          <h2>Built Features</h2>
          <div
            class="roadmapItem"
            v-for="item in builtItems"
            :key="item.name"
            :class="{ 'roadmapItem-built': item.tags.includes('built') }"
          >
            <div class="roadmapItemRow1">
              <div class="roadmapItemTitle">
                <h2>{{ item.name }}</h2>
              </div>
              <div class="roadmapItemTags">
                <div class="roadmapItemTag" v-if="item.tags.includes('built')">
                  <p>built</p>
                  <img src="../assets/icons/check-circle-fill.svg" />
                </div>
                <div
                  class="roadmapItemTag"
                  v-if="item.tags.includes('in progress')"
                >
                  <p>in progress</p>
                  <img src="../assets/icons/fast-forward-circle-fill.svg" />
                </div>
                <div
                  class="roadmapItemTag"
                  v-if="item.tags.includes('newly added')"
                >
                  <p>newly added</p>
                  <img src="../assets/icons/star-fill.svg" />
                </div>
              </div>
            </div>
            <div class="roadmapItemRow2">
              <div class="roadmapItemDescription">
                <p>{{ item.description }}</p>
              </div>
            </div>
            <div v-if="!item.tags.includes('built')" class="roadmapItemRow3">
              <div class="roadmapItemVote">
                <button>
                  <img src="../assets/icons/arrow-up-circle-fill.svg" />
                  <p>Upvote</p>
                  <p id="roadmapItemVotes">{{ item.votes }}</p>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        id="roadmapOverlay"
        class="roadmapOverlay"
        :class="{ active: roadmapOverlay }"
      >
        <div class="roadmapOverlayContent">
          <img
            src="../assets/icons/x.svg"
            class="roadmapOverlayCloseButton"
            @click="activateOverlay"
          />
          <h1>🐼</h1>
          <h2>Thanks for the feedback!</h2>
          <p>
            We’re doing our best to add the new features you want. Please share
            your email address and we’ll notify you as we make progress!
          </p>
          <div class="roadmapOverlayForm">
            <input
              id="email"
              ref="email"
              v-model="email"
              placeholder="your email address"
              type="email"
              name="email"
            />
            <button
              class="roadmapOverlayButton"
              @click="submitRoadmapSuggestion()"
            >
              Notify Me
            </button>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
@import "../assets/styles/panda-main.css";
</style>
