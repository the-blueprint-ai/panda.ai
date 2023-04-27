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
    <img src="../../src/assets/panda.png" class="biglogo" width="200" />
      <div>
        <h1>SUCCESSFULLY UNSUBSCRIBED</h1>
        <p>We are sorry to see you go 😭</p>
        <p>
          You can always keep up to date with what we are doing by keeping an
          eye on the Roadmap page.
        </p>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
