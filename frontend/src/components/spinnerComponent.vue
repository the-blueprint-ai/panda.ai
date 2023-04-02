<script>
import { HalfCircleSpinner } from "epic-spinners";

export default {
  data() {},
  props: {
    loading: Boolean,
    buttonText: String,
  },
  components: {
    HalfCircleSpinner,
  },
};
</script>

<template>
  <span>
    <half-circle-spinner v-if="loading" :animation-duration="1000" :size="25" color="#000000" />
    <span v-if="!loading">{{ buttonText }}</span>
  </span>
</template>
