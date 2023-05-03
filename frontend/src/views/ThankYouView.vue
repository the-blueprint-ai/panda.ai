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
      <div class="container pt-5 pb-5 text-center">
        <img src="../../src/assets/panda.png" width="200" />
        <h1 class="mt-5">THANK YOU!</h1>
        <p class="mt-5">Thank you for signing up to our paid subscription plan.</p>
        <div v-if="session">
          <router-link :to="'/auth/' + userId + '/chat'">
            <button type="button" class="btn btn-secondary btn-lg mt-5">LET'S CHAT</button>
          </router-link>
        </div>
        <div v-else>
          <router-link :to="'/signin'">
            <button type="button" class="btn btn-secondary btn-lg mt-5">LET'S CHAT</button>
          </router-link>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
