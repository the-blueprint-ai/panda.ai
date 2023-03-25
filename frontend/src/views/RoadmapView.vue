<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";

export default defineComponent({
  components: {
    navBar,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div class="body">
      <div>
        <h1>🐼</h1>
        <h1>ROADMAP</h1>
        <h2>COMING SOON...</h2>
      </div>
    </div>
  </main>
</template>

<style scoped>
@import "../assets/styles/panda-main.css";
</style>