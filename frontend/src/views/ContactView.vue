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
  <main style="height: 71vh">
    <navBar></navBar>
    <div class="container-fluid h-100 bg-primary text-white">
      <div class="container text-center pt-5 pb-5">
        <h1>🐼</h1>
        <h1>CONTACT US</h1>
        <h2 class="mt-5">COMING SOON...</h2>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
