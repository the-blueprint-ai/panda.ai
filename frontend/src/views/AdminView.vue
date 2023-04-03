<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {
      tab: "users",
    };
  },
  watch: {},
  mounted() {},
  computed: {
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
          <p :class="{ 'selected': tab === 'users', 'unselected': tab !== 'users' }" @click="adminTabSelector('users')">
            <img src="../assets/icons/person-circle.svg" />USERS
          </p>
          <p :class="{ 'selected': tab === 'analytics', 'unselected': tab !== 'analytics' }" @click="adminTabSelector('analytics')">
            <img src="../assets/icons/clipboard-data-fill.svg" />ANALYTICS
          </p>
          <p :class="{ 'selected': tab === 'roadmap', 'unselected': tab !== 'roadmap' }" @click="adminTabSelector('roadmap')">
            <img src="../assets/icons/signpost-2-fill.svg" />ROADMAP
          </p>
          <p :class="{ 'selected': tab === 'logs', 'unselected': tab !== 'logs' }" @click="adminTabSelector('logs')">
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
            <h2>panda.ai Roadmap</h2>
            <p>Coming soon...</p>
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
