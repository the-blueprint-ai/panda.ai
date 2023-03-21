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
        <img src="../../src/assets/404.png" width="1200"/>
      </div>
    </div>
  </main>
</template>
<style scoped>
@import "../assets/styles/panda-main.css";
</style>
