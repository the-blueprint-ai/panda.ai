<script>
import videosIcon from "../assets/icons/youtube.svg";
import mapsIcon from "../assets/icons/geo-alt-fill.svg";
import imagesIcon from "../assets/icons/image.svg";
import wikipediaIcon from "../assets/icons/wikipedia.svg";
import searchIcon from "../assets/icons/google.svg";
import newsIcon from "../assets/icons/newspaper.svg";
import musicIcon from "../assets/icons/music-note-list.svg";
import moviesIcon from "../assets/icons/film.svg";

export default {
  data() {
    let date = new Date(); // Get current date
    date.setMonth(date.getMonth() - 1); // Subtract one month
    date.setDate(date.getDate() - 5); // Subtract five days
    let timestamp = date.getTime(); // Get timestamp
    return {
      integrationsList: [
        { id: 1, name: "VIDEO", icon: videosIcon },
        {
          id: 2,
          name: "MAPS",
          icon: mapsIcon,
        },
        {
          id: 3,
          name: "IMAGES",
          icon: imagesIcon,
        },
        {
          id: 4,
          name: "WIKIPEDIA",
          icon: wikipediaIcon,
        },
        {
          id: 5,
          name: "SEARCH",
          icon: searchIcon,
        },
        { id: 6, name: "NEWS", icon: newsIcon },
        {
          id: 7,
          name: "MUSIC",
          icon: musicIcon,
        },
        {
          id: 8,
          name: "MOVIES/TV SHOWS",
          icon: moviesIcon,
        },
      ],
      lastUpdated: timestamp,
      selectedIntegrations: [],
    };
  },
  watch: {
    selectedIntegrations(newVal) {
      if (newVal.length > this.integrations) {
        this.selectedIntegrations.pop(); // Remove the last added integration
      }
    },
    integrations(newVal) {
      if (newVal >= this.integrationsList.length) {
        this.selectedIntegrations = this.integrationsList.map((i) => i.id);
      }
    },
  },
  props: {
    integrationsMenu: Boolean,
    integrations: Number,
  },
  created() {
    if (this.integrations >= this.integrationsList.length) {
      this.selectedIntegrations = this.integrationsList.map((i) => i.id);
    }
  },
  computed: {
    canUpdate() {
      let lastUpdatedDate = new Date(this.lastUpdated);
      let currentDate = new Date();

      // Check if lastUpdatedDate is in the previous month
      return (
        lastUpdatedDate.getFullYear() < currentDate.getFullYear() ||
        lastUpdatedDate.getMonth() < currentDate.getMonth()
      );
    },
  },
  components: {},
};
</script>

<template>
  <div class="d-flex justify-content-center" v-if="integrationsMenu">
    <div class="card mt-2 w-50">
      <div class="card-header text-center">
        <h3 class="mt-2">SELECT YOUR INTEGRATIONS</h3>
      </div>
      <div class="card-body d-flex flex-column mx-auto">
        <div
          class="form-check form-switch"
          v-for="integration in integrationsList"
          :key="integration.id"
        >
          <input
            class="form-check-input active-bg-secondary"
            type="checkbox"
            :value="integration.id"
            v-model="selectedIntegrations"
            :disabled="
              !canUpdate ||
              (selectedIntegrations.length >= integrations &&
                !selectedIntegrations.includes(integration.id))
            "
          />
          <label class="form-check-label d-flex" for="flexCheckDefault">
            <img :src="integration.icon" alt="" class="icon ms-2 me-2" />
            - {{ integration.name }}
          </label>
        </div>
      </div>
      <p
        v-if="selectedIntegrations.length >= integrations"
        class="text-warning mx-auto"
      >
        You have reached your maximum number of integrations.
      </p>
      <p
        v-if="selectedIntegrations.length >= integrations"
        class="lh-0 mt-n3 text-warning mx-auto"
      >
        If you would like to add another, please deselect one first.
      </p>
      <div class="card-footer text-center">
        <button
          class="btn btn-secondary btn-lg mt-3 mb-3"
          @click="saveIntegrations"
          :disabled="!canUpdate"
        >
          SAVE INTEGRATIONS
        </button>
        <p class="lh-0 text-danger" v-if="!canUpdate">
          You can only update your integrations once a month.
        </p>
        <p class="mt-n3 lh-0 text-danger" v-if="!canUpdate">
          Please come back next month.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
