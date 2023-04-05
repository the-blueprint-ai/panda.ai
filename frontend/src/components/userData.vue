<script>
import { mapGetters } from "vuex";
import { getEntities } from "../composables/getEntities.js";
import { updateEntityDescription } from "../composables/updateEntityDescription.js";

export default {
  data() {
    return {
      tab: "entities",
    };
  },
  watch: {
    userId: {
      immediate: true,
      handler: async function (newUserId) {
        if (newUserId) {
          await getEntities(this.$store, newUserId);
        }
      },
    },
  },
  props: {
    dataMenu: Boolean,
    userId: String,
  },
  async mounted() {},
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
    updateEntityDescription,
    dataTabSelector(tabName) {
      this.tab = tabName;
    },
    redirectToChat() {
      this.$router.push("/" + this.userId + "/chat");
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
        <p>
          Below are all the different 'entities' that 🐼 panda.ai has knowledge
          of from all the chats you've had. They are created by 🐼 panda.ai by
          identifying individual items, such as people, pets, places, and then
          summarising the information provided about each of them. The entities
          are added to over time as 🐼 panda.ai learns more about them.
        </p>
        <p>
          If you see anything wrong in the description of any of your entities
          below you can click on the description in the table to edit it and
          that will update 🐼 panda.ai's memory 🤓.
        </p>
        <table v-if="entitiesData.length != 0" class="entitiesTable">
          <thead>
            <tr>
              <th>Entity</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entity, index) in entitiesData" :key="entity.entity">
              <td>{{ entity.entity }}</td>
              <td
                contenteditable="true"
                @blur="
                  updateEntityDescription($event, this.entitiesData, index)
                "
              >
                {{ entity.description }}
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="noEntityData">
          <h2>No entities data available</h2>
          <p style="text-align: center">
            Please have more chats with 🐼 panda.ai so that it can learn more
            about you.
          </p>
          <button class="chatButton" @click="redirectToChat">Let's Chat</button>
        </div>
      </div>
      <div v-if="tab === 'documents'" class="documentsData">
        <p>Your shared documents coming soon...</p>
      </div>
      <div v-if="tab === 'social'" class="socialData">
        <p>Your shared social data coming soon...</p>
      </div>
      <div v-if="tab === 'browsing'" class="browsingData">
        <p>Your shared browsing data coming soon...</p>
      </div>
    </div>
  </div>
</template>
