<script>
import { mapGetters } from "vuex";
import { getEntities } from "../composables/getEntities.js";

export default {
  data() {
    return {
      tab: "entities",
    };
  },
  watch: {},
  props: {
    dataMenu: Boolean,
  },
  async mounted() {
    await getEntities(this.$store, this.getStoreUserId);
  },
  computed: {
    ...mapGetters("userStore", {
      getStoreUserId: "getStoreUserId",
      getStoreEntities: "getStoreEntities",
    }),
    entitiesData() {
      return this.getStoreEntities || [];
    },
    entitiesDataClasses() {
      return {
        selected: this.tab === "entities",
      };
    },
    documentsDataClasses() {
      return {
        selected: this.tab === "documents",
      };
    },
    socialDataClasses() {
      return {
        selected: this.tab === "social",
      };
    },
    browsingDataClasses() {
      return {
        selected: this.tab === "browsing",
      };
    },
  },
  created() {},
  methods: {
    dataTabSelector(tabName) {
      this.tab = tabName;
    },
  },
  components: {},
};
</script>

<template>
  <div class="userData" v-if="dataMenu">
    <div class="userDataTypes">
      <h2
        :class="{
          selected: tab === 'entities',
          unselected: tab !== 'entities',
        }"
        @click="dataTabSelector('entities')"
      >
        <img src="../assets/icons/list-ul.svg" />ENTITIES
      </h2>
      <h2
        :class="{
          selected: tab === 'documents',
          unselected: tab !== 'documents',
        }"
        @click="dataTabSelector('documents')"
      >
        <img src="../assets/icons/files.svg" />DOCUMENTS
      </h2>
      <h2
        :class="{ selected: tab === 'social', unselected: tab !== 'social' }"
        @click="dataTabSelector('social')"
      >
        <img src="../assets/icons/chat-right-text-fill.svg" />SOCIAL
      </h2>
      <h2
        :class="{
          selected: tab === 'browsing',
          unselected: tab !== 'browsing',
        }"
        @click="dataTabSelector('browsing')"
      >
        <img src="../assets/icons/browser-safari.svg" />BROWSING
      </h2>
    </div>
    <div class="userDataContent">
      <div v-if="tab === 'entities'" class="entitiesData">
        <h2>Entities Data</h2>
        <p>Coming soon...</p>
        <h2>Table goes here</h2>
        <table class="roadmapTable">
          <thead>
            <tr v-for="entity in entitiesData" :key="index">
              <th>{{ entity.entity }}</th>
              <th>{{ entity.description }}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>entity 1</td>
              <td>description 1</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="tab === 'documents'" class="documentsData">
        <h2>Documents Data</h2>
        <p>Coming soon...</p>
      </div>
      <div v-if="tab === 'social'" class="socialData">
        <h2>Social Data</h2>
        <p>Coming soon...</p>
      </div>
      <div v-if="tab === 'browsing'" class="browsingData">
        <h2>Browsing Data</h2>
        <p>Coming soon...</p>
      </div>
    </div>
  </div>
</template>
