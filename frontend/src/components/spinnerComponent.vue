<script>
import { HalfCircleSpinner } from "epic-spinners";

export default {
  data() {},
  props: {
    loading: Boolean,
    buttonText: String,
    spinnerSize: {
      type: Number,
      default: 25, // or whatever default value you want to use
    },
  },
  mounted() {
    console.log(this.spinnerSize);
  },
  computed: {},
  components: {
    HalfCircleSpinner,
  },
};
</script>

<template>
  <span>
    <half-circle-spinner v-if="loading" :animation-duration="1000" :size="spinnerSize" color="#000000" />
    <span v-if="!loading">{{ buttonText }}</span>
  </span>
</template>
