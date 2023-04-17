<script>
import { defineComponent } from "vue";
import { mapGetters, mapMutations } from "vuex";
import { DateTime } from "luxon";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { getRoadmap } from "../composables/getRoadmap.js";
import { getFAQs } from "../composables/getFAQs.js";
import { getUserStats } from "../composables/getUserStats.js";
import BarChart from "../components/barChart.vue";

export default defineComponent({
  data() {
    return {
      tab: "users",
      userStats: {
        totalUsers: 0,
        dailyUsers: 0,
        weeklyUsers: 0,
        monthlyUsers: 0,
      },
      onboardingStats: {
        totalOnboards: 0,
        dailyOnboards: 0,
        weeklyOnboards: 0,
        monthlyOnboards: 0,
      },
      chatStats: {
        totalChats: 0,
        dailyChats: 0,
        weeklyChats: 0,
        monthlyChats: 0,
      },
      entityStats: {
        totalEntities: 0,
        dailyEntities: 0,
        weeklyEntities: 0,
        monthlyEntities: 0,
      },
      usersByDay: {},
      onboardingByDay: {},
      chatsByDay: {},
      entitiesByDay: {},
      updating: false,
      editedData: {},
      newRoadmapName: "",
      newRoadmapDescription: "",
      newFAQTitle: "",
      newFAQQuestion: "",
      newFAQAnswer: "",
      roadmapAdded: false,
      faqAdded: false,
    };
  },
  watch: {},
  async mounted() {
    await getRoadmap(this.$store, "admin");
    await getFAQs(this.$store);
    const {
      totalUsers,
      dailyUsers,
      weeklyUsers,
      monthlyUsers,
      totalOnboards,
      dailyOnboards,
      weeklyOnboards,
      monthlyOnboards,
      totalChats,
      dailyChats,
      weeklyChats,
      monthlyChats,
      totalEntities,
      dailyEntities,
      weeklyEntities,
      monthlyEntities,
      usersByDay,
      onboardingByDay,
      chatsByDay,
      entitiesByDay,
    } = await getUserStats(this.$store);
    this.userStats = {
      totalUsers,
      dailyUsers,
      weeklyUsers,
      monthlyUsers,
    };
    this.onboardingStats = {
      totalOnboards,
      dailyOnboards,
      weeklyOnboards,
      monthlyOnboards,
    };
    this.chatStats = {
      totalChats,
      dailyChats,
      weeklyChats,
      monthlyChats,
    };
    this.entityStats = {
      totalEntities,
      dailyEntities,
      weeklyEntities,
      monthlyEntities,
    };
    this.usersByDay = usersByDay;
    this.onboardingByDay = onboardingByDay;
    this.chatsByDay = chatsByDay;
    this.entitiesByDay = entitiesByDay;
  },
  computed: {
    ...mapGetters("roadmapStore", {
      getRoadmapData: "getRoadmapData",
    }),
    ...mapGetters("faqsStore", {
      getStoreFAQs: "getStoreUnsortedFAQs",
    }),
    ...mapGetters("userStatsStore", {
      getStoreToplineUsersStats: "getStoreToplineUsersStats",
      getStoreDailyUsersStats: "getStoreDailyUsersStats",
      getStoreToplineOnboardingStats: "getStoreToplineOnboardingStats",
      getStoreDailyOnboardingStats: "getStoreDailyOnboardingStats",
      getStoreToplineChatsStats: "getStoreToplineChatsStats",
      getStoreDailyChatsStats: "getStoreDailyChatsStats",
      getStoreToplineEntitiesStats: "getStoreToplineEntitiesStats",
      getStoreDailyEntitiesStats: "getStoreDailyEntitiesStats",
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
        await getRoadmap(this.$store, "admin");
        this.roadmapData;
        this.roadmapAdded = true;
        this.newRoadmapName = "";
        this.newRoadmapDescription = "";
        setTimeout(() => {
          this.roadmapAdded = false;
        }, 5000);

        console.log(data.message);
      } catch (error) {
        console.error(error);
      }
    },
    async saveFAQItem(title, question, answer) {
      const url = import.meta.env.VITE_APP_API_URL + "/faqs/add";
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: title,
            question: question,
            answer: answer,
            visible: false,
          }),
        });
        const data = await response.json();
        await getFAQs(this.$store);
        this.faqsData;
        this.faqAdded = true;
        this.newFAQTitle = "";
        this.newFAQQuestion = "";
        this.newFAQAnswer = "";
        setTimeout(() => {
          this.faqAdded = false;
        }, 5000);

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
              selected: tab === 'promptlayer',
              unselected: tab !== 'promptlayer',
            }"
            @click="adminTabSelector('promptlayer')"
          >
            <img src="../assets/icons/cake.png" />PROMPTLAYER
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
              <div class="displayNumber">
                <h2>Top Entities</h2>
              </div>
              <div class="displayNumber">
                <h2>Top Topics</h2>
              </div>
              <div class="displayNumber">
                <h2>Top 10 chatters</h2>
              </div>
              <div class="displayNumber">
                <h2>Top 10 entity creators</h2>
              </div>
              <div class="displayNumber">
                <h2>Top 10 entity updaters</h2>
              </div>
            </div>
          </div>
          <div v-if="tab === 'users'" class="usersAdmin">
            <div class="usersTopLine">
              <div class="displayNumber">
                <h1 v-text="userStats.totalUsers"></h1>
                <p># Total Users</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="userStats.dailyUsers"></h1>
                <p># Daily New Users</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="userStats.weeklyUsers"></h1>
                <p># Weekly New Users</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="userStats.monthlyUsers"></h1>
                <p># Monthly New Users</p>
              </div>
            </div>
            <div class="usersChart">
              <BarChart
                v-if="this.usersByDay.length > 0"
                :data-by-day="this.usersByDay"
                :axis-name="'# New Users'"
              />
            </div>
          </div>
          <div v-if="tab === 'onboarding'" class="onboardingAdmin">
            <div class="usersTopLine">
              <div class="displayNumber">
                <h1 v-text="onboardingStats.totalOnboards"></h1>
                <p># Total Users Onboarded</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="onboardingStats.dailyOnboards"></h1>
                <p># Daily Onboards</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="onboardingStats.weeklyOnboards"></h1>
                <p># Weekly Onboards</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="onboardingStats.monthlyOnboards"></h1>
                <p># Monthly Onboards</p>
              </div>
            </div>
            <div class="usersChart">
              <BarChart
                v-if="this.onboardingByDay.length > 0"
                :data-by-day="this.onboardingByDay"
                :axis-name="'# New Onboards'"
              />
            </div>
          </div>
          <div v-if="tab === 'chats'" class="chatsAdmin">
            <div class="usersTopLine">
              <div class="displayNumber">
                <h1 v-text="chatStats.totalChats"></h1>
                <p># Total Chats</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="chatStats.dailyChats"></h1>
                <p># Daily Chats</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="chatStats.weeklyChats"></h1>
                <p># Chats This Week</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="chatStats.monthlyChats"></h1>
                <p># Chats This Month</p>
              </div>
            </div>
            <div class="usersChart">
              <BarChart
                v-if="this.chatsByDay.length > 0"
                :data-by-day="this.chatsByDay"
              />
            </div>
            <div class="usersBottomLine">
              <div class="displayNumber">
                <h1>4</h1>
                <p>Static</p>
                <p>Average chat length (msgs)</p>
              </div>
              <div class="displayNumber">
                <h1>4</h1>
                <p>Static</p>
                <p>Average chat length (time)</p>
              </div>
            </div>
          </div>
          <div v-if="tab === 'entities'" class="entitiesAdmin">
            <div class="usersTopLine">
              <div class="displayNumber">
                <h1 v-text="entityStats.totalEntities"></h1>
                <p># Total Entities Created</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="entityStats.dailyEntities"></h1>
                <p># Daily Entities Created</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="entityStats.weeklyEntities"></h1>
                <p># Weekly Entities Created</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="entityStats.monthlyEntities"></h1>
                <p># Monthly Entities Created</p>
              </div>
            </div>
            <div class="usersChart">
              <BarChart
                v-if="this.entitiesByDay.length > 0"
                :data-by-day="this.entitiesByDay"
                :axis-name="'# New Entities'"
              />
            </div>
            <div class="usersBottomLine">
              <div class="displayNumber">
                <h1 v-text="entityStats.totalEntities"></h1>
                <p># Total Entities Updated</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="entityStats.dailyEntities"></h1>
                <p># Daily Entities Updated</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="entityStats.weeklyEntities"></h1>
                <p># Weekly Entities Updated</p>
              </div>
              <div class="displayNumber">
                <h1 v-text="entityStats.monthlyEntities"></h1>
                <p># Monthly Entities Updated</p>
              </div>
            </div>
            <div class="usersChart">
              <BarChart />
            </div>
          </div>
          <div v-if="tab === 'promptlayer'" class="promptlayerAdmin">
            <h2>PromptLayer</h2>
            <p>Coming soon...</p>
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
                <form
                  @submit.prevent="
                    saveRoadmapItem(
                      this.newRoadmapName,
                      this.newRoadmapDescription
                    )
                  "
                >
                  <input v-model="newRoadmapName" />
                </form>
              </div>
              <div class="newRoadmapDescription">
                <p>Description</p>
                <form
                  @submit.prevent="
                    saveRoadmapItem(
                      this.newRoadmapName,
                      this.newRoadmapDescription
                    )
                  "
                >
                  <input
                    v-model="newRoadmapDescription"
                    @keyup.enter="
                      saveRoadmapItem(
                        this.newRoadmapName,
                        this.newRoadmapDescription
                      )
                    "
                  />
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
            <p v-if="roadmapAdded" class="roadmapSuccess" style="color: green">
              new roadmap item saved to database
            </p>
            <table class="roadmapTable" :key="roadmapData.length">
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
            <h2>ADD NEW FAQ</h2>
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
                  <form
                    @keyup.enter.prevent="
                      saveFAQItem(
                        this.newFAQTitle,
                        this.newFAQQuestion,
                        this.newFAQAnswer
                      )
                    "
                  >
                    <input
                      v-model="newFAQAnswer"
                      @keyup.enter="
                        saveFAQItem(
                          this.newFAQTitle,
                          this.newFAQQuestion,
                          this.newFAQAnswer
                        )
                      "
                    />
                  </form>
                </div>
              </div>
              <div class="newFAQItemSave">
                <button
                  class="chatButton"
                  id="saveFAQButton"
                  @click="
                    saveFAQItem(
                      this.newFAQTitle,
                      this.newFAQQuestion,
                      this.newFAQAnswer
                    )
                  "
                >
                  SAVE
                </button>
              </div>
            </div>
            <p v-if="faqAdded" class="faqSuccess" style="color: green">
              new faq saved to database
            </p>
            <div class="faqTableContainer">
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
                        updateFAQField(
                          'question',
                          index,
                          $event.target.innerText
                        )
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
