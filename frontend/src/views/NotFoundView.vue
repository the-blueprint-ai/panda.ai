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
    <div class="mainContainer container-fluid bg-primary text-white">
      <div class="container text-center pt-5 pb-5">
        <img class="img-fluid page404" src="../../src/assets/404.png" />
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
