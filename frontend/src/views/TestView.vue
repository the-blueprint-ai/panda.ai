<script lang="ts">
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import ImageUpload from "../components/imageUpload.vue";

export default defineComponent({
  data() {
    return {};
  },
  mounted() {},

  methods: {},

  components: {
    navBar,
    ImageUpload,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div class="body">
      <h1>TESTING</h1>
      <ImageUpload></ImageUpload>
    </div>
  </main>
</template>

<style>
@import "../assets/styles/panda-main.css";
</style>
