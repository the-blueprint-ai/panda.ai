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
    <div class="body">
      <div>
        <h1>PRIVACY</h1>
      </div>
    </div>
  </main>
</template>

<style scoped>
@import "../assets/styles/panda-main.css";
</style>
