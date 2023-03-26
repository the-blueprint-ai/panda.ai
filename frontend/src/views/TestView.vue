<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import ImageUpload from "../components/imageUpload.vue";

export default defineComponent({
  data() {
    return {};
  },
  mounted() {},

  methods: {},

  components: {
    navBar,
    navFooter,
    ImageUpload,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div class="bodyG">
      <h1>TESTING</h1>
      <ImageUpload></ImageUpload>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style>
@import "../assets/styles/panda-main.css";
</style>
