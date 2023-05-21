<script>
import SpinnerComponent from "../components/spinnerComponent.vue";

export default {
  data() {
    return {
      loadingOverlay: true,
    };
  },
  props: {
    loading: Boolean,
  },
  computed: {},
  methods: {},
  components: {
    SpinnerComponent,
  },
};
</script>

<template>
  <div id="loadingOverlay" class="overlay" :class="{ active: loadingOverlay }">
    <SpinnerComponent
      id="loadingSpinner"
      :loading="this.loading"
      spinner-size="80"
    ></SpinnerComponent>
    <h2>loading...</h2>
  </div>
</template>
