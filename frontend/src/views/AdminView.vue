<script>
import { defineComponent } from "vue";
import { mapGetters, mapMutations } from "vuex";
import { DateTime } from "luxon";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { getRoadmap } from "../composables/getRoadmap.js";
import { getFAQs } from "../composables/getFAQs.js";
import BarChart from "../components/barChart.vue";

export default defineComponent({
  data() {
    return {
      tab: "faqs",
      updating: false,
      editedData: {},
      newRoadmapName: "",
      newRoadmapDescription: "",
      newFAQTitle: "",
      newFAQQuestion: "",
      newFAQAnswer: "",
    };
  },
  watch: {},
  async mounted() {
    await getRoadmap(this.$store, "admin");
    await getFAQs(this.$store);
  },
  computed: {
    ...mapGetters("roadmapStore", {
      getRoadmapData: "getRoadmapData",
    }),
    ...mapGetters("faqsStore", {
      getStoreFAQs: "getStoreUnsortedFAQs",
    }),
    roadmapData() {
      return this.getRoadmapData || [];
    },
    faqsData() {
      return this.getStoreFAQs || [];
    },
  },
  methods: {
    ...mapMutations("faqsStore", {
      setStoreFAQs: "setStoreUnsortedFAQs",
    }),
    adminTabSelector(tabName) {
      this.tab = tabName;
    },
    formatDateTime(dateTimeString) {
      const dt = dateTimeString;
      const formattedDateTime = DateTime.fromISO(dt).toLocaleString(
        DateTime.DATETIME_MED
      );
      return formattedDateTime;
    },
    async updateRoadmapData(event, index, key, roadmap_id) {
      if (this.updating) {
        console.log("Function is already being executed");
        return;
      }
      this.updating = true;
      const newValue = event.target.innerText;
      const roadmap = this.roadmapData[index];
      roadmap[key] = newValue;
      const manualRoadmap = {
        roadmap_id: roadmap_id,
        created_at: roadmap.created_at,
        name: roadmap.name,
        description: roadmap.description,
        tags: JSON.parse(roadmap.tags),
        votes: roadmap.votes,
        reviewed: roadmap.reviewed,
        email: roadmap.email,
      };
      try {
        const url =
          import.meta.env.VITE_APP_API_URL +
          "/admin/update-roadmap?roadmap_id=" +
          roadmap_id;
        const response = await fetch(url, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(manualRoadmap),
        });
        if (!response.ok) {
          throw new Error("Error updating roadmap data.");
        }
        // Update the roadmap data in the Vuex store
        this.$store.commit("roadmapStore/setRoadmapData", {
          index,
          key,
          newValue,
        });
      } catch (error) {
        console.error(error);
      } finally {
        this.updating = false;
      }
    },
    updateFAQField(field, index, value, e) {
      const faq = this.faqsData[index];
      if (faq) {
        if (field === "visible") {
          faq[field] = e.target.checked;
        } else if (faq[field] !== value) {
          faq[field] = value;
        }
        this.editedData = {
          ...faq,
          visible: faq.visible ? "true" : "false",
        };
        this.updateFAQs();
      } else {
        console.log("updateFAQField skipped");
      }
    },
    async updateFAQs() {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_APP_API_URL}/faqs/update`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.editedData),
          }
        );
        const data = await response.json();
        console.log(data.message);
      } catch (error) {
        console.error(error);
      }
    },
    async saveRoadmapItem(name, description) {
      const url =
        import.meta.env.VITE_APP_API_URL +
        "/admin/add-roadmap-idea?name=" +
        name +
        "&description=" +
        description;
      try {
        const response = await fetch(url, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
        });
        const data = await response.json();
        console.log(data.message);
      } catch (error) {
        console.error(error);
      }
    },
  },
  components: {
    navBar,
    navFooter,
    BarChart,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div class="bodyG">
      <div class="adminPanel">
        <div class="sidePanel">
          <h2>ADMIN PANEL</h2>
          <p
            :class="{
              selected: tab === 'trending',
              unselected: tab !== 'trending',
            }"
            @click="adminTabSelector('trending')"
          >
            <img src="../assets/icons/graph-up-arrow.svg" />TRENDING
          </p>
          <p
            :class="{ selected: tab === 'users', unselected: tab !== 'users' }"
            @click="adminTabSelector('users')"
          >
            <img src="../assets/icons/person-circle.svg" />USERS
          </p>
          <p
            :class="{
              selected: tab === 'onboarding',
              unselected: tab !== 'onboarding',
            }"
            @click="adminTabSelector('onboarding')"
          >
            <img
              src="../assets/icons/arrow-up-right-circle-fill.svg"
            />ONBOARDING
          </p>
          <p
            :class="{ selected: tab === 'chats', unselected: tab !== 'chats' }"
            @click="adminTabSelector('chats')"
          >
            <img src="../assets/icons/chat-right-text-fill.svg" />CHATS
          </p>
          <p
            :class="{
              selected: tab === 'entities',
              unselected: tab !== 'entities',
            }"
            @click="adminTabSelector('entities')"
          >
            <img src="../assets/icons/list-ul.svg" />ENTITIES
          </p>
          <p
            :class="{
              selected: tab === 'analytics',
              unselected: tab !== 'analytics',
            }"
            @click="adminTabSelector('analytics')"
          >
            <img src="../assets/icons/clipboard-data-fill.svg" />SITE ANALYTICS
          </p>
          <p
            :class="{
              selected: tab === 'roadmap',
              unselected: tab !== 'roadmap',
            }"
            @click="adminTabSelector('roadmap')"
          >
            <img src="../assets/icons/signpost-2-fill.svg" />ROADMAP
          </p>
          <p
            :class="{
              selected: tab === 'faqs',
              unselected: tab !== 'faqs',
            }"
            @click="adminTabSelector('faqs')"
          >
            <img src="../assets/icons/question-circle-fill.svg" />FAQs
          </p>
          <p
            :class="{ selected: tab === 'logs', unselected: tab !== 'logs' }"
            @click="adminTabSelector('logs')"
          >
            <img src="../assets/icons/database-fill-exclamation.svg" />LOGS
          </p>
        </div>
        <div class="adminContent">
          <div v-if="tab === 'trending'" class="trendingAdmin">
            <div class="usersTopLine">
              <div class="displayNumber" id="totalUsersRegistered">
                <h2>Top Entities</h2>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h2>Top Topics</h2>
              </div>
            </div>
            <div class="usersChart">
              <BarChart />
            </div>
            <div class="usersChart">
              <BarChart />
            </div>
          </div>
          <div v-if="tab === 'users'" class="usersAdmin">
            <div class="usersTopLine">
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>2</h1>
                <p># Total Users Registered</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>3</h1>
                <p># Daily Active Users</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>4</h1>
                <p># Weekly Active Users</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>5</h1>
                <p># Monthly Active Users</p>
              </div>
            </div>
            <div class="usersChart">
              <BarChart />
            </div>
            <div class="usersChart">
              <BarChart />
            </div>
          </div>
          <div v-if="tab === 'onboarding'" class="onboardingAdmin">
            <div class="usersTopLine">
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>2</h1>
                <p># Total Users Onboarded</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>3</h1>
                <p># Daily Onboards</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>4</h1>
                <p># Weekly Onboards</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>5</h1>
                <p># Monthly Onboards</p>
              </div>
            </div>
            <div class="usersChart">
              <BarChart />
            </div>
            <div class="usersChart">
              <BarChart />
            </div>
          </div>
          <div v-if="tab === 'chats'" class="chatsAdmin">
            <div class="usersTopLine">
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>2</h1>
                <p># Total Chats Started</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>3</h1>
                <p># Daily Entites Started</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>4</h1>
                <p># Weekly Entites Started</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>5</h1>
                <p># Monthly Entites Started</p>
              </div>
            </div>
            <div class="usersChart">
              <BarChart />
            </div>
            <div class="usersChart">
              <BarChart />
            </div>
          </div>
          <div v-if="tab === 'entities'" class="entitiesAdmin">
            <div class="usersTopLine">
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>2</h1>
                <p># Total Entities Created</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>3</h1>
                <p># Daily Entites Created</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>4</h1>
                <p># Weekly Entites Created</p>
              </div>
              <div class="displayNumber" id="totalUsersRegistered">
                <h1>5</h1>
                <p># Monthly Entites Created</p>
              </div>
            </div>
            <div class="usersChart">
              <BarChart />
            </div>
            <div class="usersChart">
              <BarChart />
            </div>
          </div>
          <div v-if="tab === 'analytics'" class="analyticsAdmin">
            <h2>panda.ai Site Analytics</h2>
            <p>Coming soon...</p>
          </div>
          <div v-if="tab === 'roadmap'" class="roadmapAdmin">
            <h2>ADD NEW ROADMAP ITEM</h2>
            <div class="newRoadmapItem">
              <div class="newRoadmapName">
                <p>Name</p>
                <form>
                  <input v-model="newRoadmapName" />
                </form>
              </div>
              <div class="newRoadmapDescription">
                <p>Description</p>
                <form>
                  <input v-model="newRoadmapDescription" />
                </form>
              </div>
              <div class="newRoadmapItemSave">
                <button
                  class="chatButton"
                  id="saveRoadmapButton"
                  @click="
                    saveRoadmapItem(
                      this.newRoadmapName,
                      this.newRoadmapDescription
                    )
                  "
                >
                  SAVE
                </button>
              </div>
            </div>
            <table class="roadmapTable">
              <thead>
                <tr>
                  <th>Roadmap ID</th>
                  <th class="centered">Created At</th>
                  <th>Name</th>
                  <th>Description</th>
                  <th class="centered">Tags</th>
                  <th class="centered">Votes</th>
                  <th class="centered">Reviewed</th>
                  <th>Email</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(roadmap, index) in roadmapData" :key="roadmap.id">
                  <td>{{ roadmap.roadmap_id }}</td>
                  <td class="centered">
                    {{ formatDateTime(roadmap.created_at) }}
                  </td>
                  <td
                    contenteditable="true"
                    @blur="
                      updateRoadmapData(
                        $event,
                        index,
                        'name',
                        roadmap.roadmap_id
                      )
                    "
                    v-text="roadmap.name"
                  ></td>
                  <td
                    contenteditable="true"
                    @blur="
                      updateRoadmapData(
                        $event,
                        index,
                        'description',
                        roadmap.roadmap_id
                      )
                    "
                    v-text="roadmap.description"
                  ></td>
                  <td
                    class="centered"
                    contenteditable="true"
                    @blur="
                      updateRoadmapData(
                        $event,
                        index,
                        'tags',
                        roadmap.roadmap_id
                      )
                    "
                    v-text="JSON.parse(roadmap.tags).toString()"
                  ></td>
                  <td
                    class="centered"
                    contenteditable="true"
                    @blur="
                      updateRoadmapData(
                        $event,
                        index,
                        'votes',
                        roadmap.roadmap_id
                      )
                    "
                    v-text="parseInt(roadmap.votes)"
                  ></td>
                  <td
                    class="centered"
                    contenteditable="true"
                    @blur="
                      updateRoadmapData(
                        $event,
                        index,
                        'reviewed',
                        roadmap.roadmap_id
                      )
                    "
                    v-text="roadmap.reviewed"
                  ></td>
                  <td
                    contenteditable="true"
                    @blur="
                      updateRoadmapData(
                        $event,
                        index,
                        'email',
                        roadmap.roadmap_id
                      )
                    "
                    v-text="roadmap.email"
                  ></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="tab === 'faqs'" class="faqsAdmin">
            <h2>ADD NEW FAQ ITEM</h2>
            <div class="newFAQItem">
              <div class="faqInput">
                <div class="newFAQTitle">
                  <p>Title</p>
                  <form>
                    <input v-model="newFAQTitle" />
                  </form>
                </div>
                <div class="newFAQQuestion">
                  <p>Question</p>
                  <form>
                    <input v-model="newFAQQuestion" />
                  </form>
                </div>
                <div class="newFAQAnswer">
                  <p>Answer</p>
                  <form>
                    <input v-model="newFAQAnswer" />
                  </form>
                </div>
              </div>
              <div class="newFAQItemSave">
                <button
                  class="chatButton"
                  id="saveFAQButton"
                  @click="
                    saveRoadmapItem(
                      this.newRoadmapName,
                      this.newRoadmapDescription
                    )
                  "
                >
                  SAVE
                </button>
              </div>
            </div>
            <table class="faqTable">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Question</th>
                  <th>Answer</th>
                  <th class="centered">Visible</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(faq, index) in faqsData" :key="index">
                  <td
                    contenteditable="true"
                    v-text="faq.title"
                    @blur="
                      updateFAQField('title', index, $event.target.innerText)
                    "
                  ></td>
                  <td
                    contenteditable="true"
                    v-text="faq.question"
                    @blur="
                      updateFAQField('question', index, $event.target.innerText)
                    "
                  ></td>
                  <td
                    contenteditable="true"
                    v-text="faq.answer"
                    @blur="
                      updateFAQField('answer', index, $event.target.innerText)
                    "
                  ></td>
                  <td class="checkBox">
                    <input
                      type="checkbox"
                      v-model="faq.visible"
                      @change="
                        updateFAQField('visible', index, faq.visible, $event)
                      "
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="tab === 'logs'" class="logsAdmin">
            <h2>Server Logs</h2>
            <p>Coming soon...</p>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style>
@import "../assets/styles/panda-main.css";
</style>
