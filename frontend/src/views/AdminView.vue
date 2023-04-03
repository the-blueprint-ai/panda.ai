<script>
import { defineComponent } from "vue";
import { mapGetters } from "vuex";
import { DateTime } from "luxon";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import { getRoadmap } from "../composables/getRoadmap.js";

export default defineComponent({
  data() {
    return {
      tab: "roadmap",
      editingItem: null,
      updating: false,
    };
  },
  watch: {},
  async mounted() {
    await getRoadmap(this.$store, "admin");
  },
  computed: {
    ...mapGetters("roadmapStore", {
      getRoadmapData: "getRoadmapData",
    }),
    roadmapData() {
      return this.getRoadmapData || [];
    },
    userAdminClasses() {
      return {
        selected: this.tab === "users",
      };
    },
    analyticsAdminClasses() {
      return {
        selected: this.tab === "analytics",
      };
    },
    roadmapAdminClasses() {
      return {
        selected: this.tab === "roadmap",
      };
    },
    logsAdminClasses() {
      return {
        selected: this.tab === "logs",
      };
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
      console.log("updateRoadmapData called");
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
            :class="{
              selected: tab === 'analytics',
              unselected: tab !== 'analytics',
            }"
            @click="adminTabSelector('analytics')"
          >
            <img src="../assets/icons/clipboard-data-fill.svg" />ANALYTICS
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
            :class="{ selected: tab === 'logs', unselected: tab !== 'logs' }"
            @click="adminTabSelector('logs')"
          >
            <img src="../assets/icons/database-fill-exclamation.svg" />LOGS
          </p>
        </div>
        <div class="adminContent">
          <div v-if="tab === 'users'" class="userAdmin">
            <h2>User Admin</h2>
            <p>Coming soon...</p>
          </div>
          <div v-if="tab === 'analytics'" class="analyticsAdmin">
            <h2>panda.ai Analytics</h2>
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
