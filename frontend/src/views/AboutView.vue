<script lang="ts">
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
    <div className="body">
      <div>
        <h1>ABOUT</h1>
      </div>
    </div>
  </main>
</template>

<style scoped>
@import "../assets/styles/panda-main.css";
</style>
