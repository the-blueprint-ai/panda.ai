<script>
import { mapGetters } from "vuex";
import { saveIntegrations } from "../composables/saveIntegrations.js";
import videosIcon from "../assets/icons/youtube.svg";
import mapsIcon from "../assets/icons/geo-alt-fill.svg";
import imagesIcon from "../assets/icons/image.svg";
import wikipediaIcon from "../assets/icons/wikipedia.svg";
import searchIcon from "../assets/icons/google.svg";
import newsIcon from "../assets/icons/newspaper.svg";
import musicIcon from "../assets/icons/music-note-list.svg";
import moviesIcon from "../assets/icons/film.svg";
import SpinnerComponent from "../components/spinnerComponent.vue";
import { useToast } from "vue-toastification";

export default {
  data() {
    let date = new Date(); // Get current date
    date.setMonth(date.getMonth() - 1); // Subtract one month
    date.setDate(date.getDate() - 5); // Subtract five days
    let timestamp = date.getTime(); // Get timestamp
    return {
      lastUpdated: timestamp,
      selectedIntegrations: [],
      icons: {
        videosIcon,
        mapsIcon,
        imagesIcon,
        wikipediaIcon,
        searchIcon,
        newsIcon,
        musicIcon,
        moviesIcon,
      },
      loading: false,
      buttonText: "SAVE INTEGRATIONS",
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
    ...mapGetters("userStore", {
      userId: "getStoreUserId",
      currentIntegrations: "getStoreCurrentIntegrations",
    }),
    ...mapGetters("integrationsStore", {
      integrationsList: "getStoreIntegrationsList",
    }),
    integrationsDifference() {
      const difference = this.integrations - this.selectedIntegrations.length;
      return difference > 0 ? difference : 0;
    },
    integrationsWarning() {
      return this.integrationsDifference > 0;
    },
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
  async mounted() {
    if (this.currentIntegrations && this.currentIntegrations.length > 0) {
      // Set selectedIntegrations to the array of integration_id from currentIntegrations
      this.selectedIntegrations = this.currentIntegrations.map(
        (integration) => integration.integration_id
      );

      // Sort currentIntegrations by last_updated in ascending order
      const sortedIntegrations = [...this.currentIntegrations].sort(
        (a, b) => new Date(a.last_updated) - new Date(b.last_updated)
      );

      // Set lastUpdated to the earliest timestamp (i.e., last_updated of the first element in sortedIntegrations)
      this.lastUpdated = new Date(sortedIntegrations[0].last_updated).getTime();
    }
  },
  methods: {
    async saveIntegrationsToDB() {
      this.loading = true;
      const toast = useToast();
      if (this.integrationsDifference > 0) {
        this.loading = false;
        toast.warning(
          `You have ${this.integrationsDifference} more integration(s) to choose.`
        );
      } else {
        const payload = {
          user_id: this.userId, // Update with the actual user ID
          selected_integrations: this.selectedIntegrations,
        };

        try {
          const response = await saveIntegrations(payload);

          // Check if response exists (if it does not, an error would have been thrown)
          this.loading = false;
          toast.success("Integrations saved successfully!");
          return response;
        } catch (error) {
          this.loading = false;
          toast.error(
            "An error occurred while saving the integrations.",
            error
          );
        }
      }
    },
  },
  components: {
    SpinnerComponent,
  },
};
</script>

<template>
  <div class="d-flex justify-content-center" v-if="integrationsMenu">
    <div class="card mt-2 text-center">
      <div class="card-header text-center">
        <h3 class="mt-2">SELECT YOUR {{ integrations }} INTEGRATIONS</h3>
      </div>
      <div
        class="card-body w-100 d-flex flex-column align-items-center mx-auto"
      >
        <div class="align-items-start">
          <div
            class="form-check form-switch"
            v-for="integration in integrationsList"
            :key="integration.integration_id"
          >
            <input
              class="form-check-input active-bg-secondary"
              type="checkbox"
              :value="integration.integration_id"
              v-model="selectedIntegrations"
              :disabled="
                !canUpdate ||
                (selectedIntegrations.length >= integrations &&
                  !selectedIntegrations.includes(integration.integration_id))
              "
            />
            <label class="form-check-label d-flex text-nowrap" for="flexCheckDefault">
              <img
                :src="icons[integration.integration_icon]"
                alt=""
                class="icon ms-2 me-2"
              />
              - {{ integration.integration_name }}
            </label>
          </div>
        </div>
      </div>
      <p v-if="integrationsDifference == 1" class="text-warning text-center">
        You have {{ integrationsDifference }} more integration to select.
      </p>
      <p v-if="integrationsDifference > 1" class="text-warning text-center">
        You have {{ integrationsDifference }} more integrations to select.
      </p>
      <div class="card-footer text-center">
        <button
          class="btn btn-secondary btn-lg d-inline-flex justify-content-center mt-3 mb-3"
          @click="saveIntegrationsToDB"
          :disabled="!canUpdate"
        >
          <SpinnerComponent
            :loading="this.loading"
            :button-text="this.buttonText"
          ></SpinnerComponent>
        </button>
        <p class="lh-0 text-danger" v-if="!canUpdate">
          You can only update your integrations once a month.
        </p>
        <p class="mt-n3 lh-0 text-danger" v-if="!canUpdate">
          Please come back next month to update them.
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
