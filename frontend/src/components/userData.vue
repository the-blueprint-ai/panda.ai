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
    await getEntities(this.$store, 'e00ca46a-16df-4844-bd4f-d8c37b2ce08a');
  },
  computed: {
    ...mapGetters("userStore", {
      getStoreUserId: "getStoreUserId",
      getStoreEntities: "getStoreEntities",
    }),
    entitiesData() {
      return this.getStoreEntities[0] || [];
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
        <table class="entitiesTable">
          <thead>
            <tr>
              <th>Entity</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entity in entitiesData" :key="entity.entity">
              <td>{{ entity.entity }}</td>
              <td>{{ entity.description }}</td>
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
