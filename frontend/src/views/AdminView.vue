<script>
import { defineComponent } from "vue";
import { mapGetters } from "vuex";
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
      editingItem: null,
      updating: false,
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
            :class="{ selected: tab === 'users', unselected: tab !== 'users' }"
            @click="adminTabSelector('users')"
          >
            <img src="../assets/icons/person-circle.svg" />USERS
          </p>
          <p
            :class="{ selected: tab === 'onboarding', unselected: tab !== 'onboarding' }"
            @click="adminTabSelector('onboarding')"
          >
            <img src="../assets/icons/arrow-up-right-circle-fill.svg" />ONBOARDING
          </p>
          <p
            :class="{ selected: tab === 'chats', unselected: tab !== 'chats' }"
            @click="adminTabSelector('chats')"
          >
            <img src="../assets/icons/chat-right-text-fill.svg" />CHATS
          </p>
          <p
            :class="{ selected: tab === 'entities', unselected: tab !== 'entities' }"
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
            <table class="roadmapTable">
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
                  <td>{{ faq.title }}</td>
                  <td>{{ faq.question }}</td>
                  <td>{{ faq.answer }}</td>
                  <td class="centered">{{ faq.visible }}</td>
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
