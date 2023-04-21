<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  components: {
    navBar,
    navFooter,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div class="body">
      <div>
        <img class="page404" src="../../src/assets/404.png" width="1200"/>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
