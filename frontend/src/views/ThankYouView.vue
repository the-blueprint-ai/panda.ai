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
        <h1>THANK YOU!</h1>
        <p>Thank you for signing up to our paid subscription plan</p>
      </div>
      <div v-if="session">
        <router-link :to="'/auth/' + userId + '/chat'">
          <button class="letsChat">Let's Chat</button>
        </router-link>
      </div>
      <div v-else>
        <router-link :to="'/signin'">
          <button class="letsChat">Let's Chat</button>
        </router-link>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
