<script>
import { mapGetters } from "vuex";
import { getEntities } from "../composables/getEntities.js";
import { updateEntityDescription } from "../composables/updateEntityDescription.js";
import { deleteEntity } from "../composables/deleteEntity.js";

export default {
  data() {
    return {
      tab: "entities",
      selectedOption: null,
      accountDataOptions: [
        { text: "Entities", value: "entities" },
        { text: "Documents", value: "documents" },
        { text: "Social", value: "social" },
        { text: "Browsing", value: "browsing" },
      ],
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
    deleteEntity,
    dataTabSelector(tabName) {
      this.tab = tabName;
    },
    redirectToChat() {
      this.$router.push("/" + this.userId + "/chat");
    },
    onTabChange(event) {
      this.tab = event.target.value;
    },
  },
  components: {},
};
</script>

<template>
  <div class="userData" v-if="dataMenu">
    <div class="userDataTypes">
      <h4
        :class="{
          selected: tab === 'entities',
          unselected: tab !== 'entities',
        }"
        @click="dataTabSelector('entities')"
      >
        <img src="../assets/icons/list-ul.svg" />ENTITIES
      </h4>
      <h4
        :class="{
          selected: tab === 'documents',
          unselected: tab !== 'documents',
        }"
        @click="dataTabSelector('documents')"
      >
        <img src="../assets/icons/files.svg" />DOCUMENTS
      </h4>
      <h4
        :class="{ selected: tab === 'social', unselected: tab !== 'social' }"
        @click="dataTabSelector('social')"
      >
        <img src="../assets/icons/chat-right-text-fill.svg" />SOCIAL
      </h4>
      <h4
        :class="{
          selected: tab === 'browsing',
          unselected: tab !== 'browsing',
        }"
        @click="dataTabSelector('browsing')"
      >
        <img src="../assets/icons/browser-safari.svg" />BROWSING
      </h4>
    </div>
    <div class="accountCardSelector">
      <select v-model="tab" class="form-select mb-2" @change="onTabChange">
        <option
          v-for="accountDataOption in accountDataOptions"
          :key="accountDataOption.value"
          :value="accountDataOption.value"
        >
          {{ accountDataOption.text }}
        </option>
      </select>
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
        <table
          v-if="entitiesData.length != 0"
          class="table table-bordered table-striped table-hover"
        >
          <thead class="table-dark">
            <tr>
              <th>Entity</th>
              <th>Description</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entity, index) in entitiesData" :key="entity.entity">
              <td><strong>{{ entity.entity }}</strong></td>
              <td
                contenteditable="true"
                @blur="
                  updateEntityDescription($event, this.entitiesData, index)
                "
              >
                {{ entity.description }}
              </td>
              <td class="align-middle">
                <img src="../assets/icons/x-circle-fill.svg" @click="deleteEntity(userId, entity)" />
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

<style scoped>
.userData {
  display: flex;
  width: 100%;
  justify-content: flex-start;
}
.accountCardSelector {
  display: none;
}
.userDataTypes {
  min-width: 180px;
  margin: 0px;
  display: flex;
  flex-direction: column;
  text-align: left;
  border-right: 1px solid lightgray;
}
.userDataTypes h4 {
  width: 195px;
  padding-top: 10px;
  padding-left: 20px;
  padding-bottom: 10px;
  margin-top: 20px;
  margin-bottom: 0px;
  margin-left: -16px;
  font-size: 20px;
}
.userDataTypes h4:hover {
  cursor: pointer;
  background-color: #ffcb4c;
}
.userDataTypes h4 img {
  height: 20px;
  margin-right: 15px;
}
.userDataContent {
  display: flex;
  padding: 20px;
  text-align: left;
  flex-wrap: wrap;
}
.align-middle img {
  cursor: pointer;
}
@media (max-width: 768px) {
  .accountCardSelector {
    display: block;
  }
  .userData {
    flex-direction: column;
  }
  .userDataTypes {
    display: none;
  }
}
</style>
