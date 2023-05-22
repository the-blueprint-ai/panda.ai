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
      <div class="container pt-5 pb-5 text-center">
        <img src="../../src/assets/panda.png" width="200" />
        <h1 class="mt-5">SUCCESSFULLY UNSUBSCRIBED</h1>
        <h2 class="mt-5">We are sorry to see you go 😭</h2>
        <p class="mt-3">
          You can always keep up to date with what we are doing by keeping an
          eye on the Roadmap page.
        </p>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
