<script>
import { mapGetters, mapActions } from "vuex";
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  async mounted() {
    if (!this.userId) {
      await this.getUserInfo();
    }
  },
  computed: {
    ...mapGetters("userStore", {
      userId: "getStoreUserId",
    }),
  },
  methods: {
    ...mapActions("userStore", ["getUserInfo"]),
  },
  components: {
    navBar,
    navFooter,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div class="container-fluid vh-100 bg-primary text-white">
      <div class="container pt-5 pb-5 text-center">
        <img src="../../src/assets/panda.png" width="200" />
        <h1 class="mt-5">THANK YOU!</h1>
        <p class="mt-5">
          Thank you for signing up to our paid subscription plan.
        </p>
        <p class="mt-5">
          Don't forget to configure your integrations in your account settings.
        </p>
        <div v-if="userId">
          <router-link :to="'/auth/' + userId + '/account'">
            <button type="button" class="btn btn-secondary btn-lg mt-5">
              ACCOUNT SETTINGS
            </button>
          </router-link>
        </div>
        <div v-else>
          <router-link :to="'/signin'">
            <button type="button" class="btn btn-secondary btn-lg mt-5">
              ACCOUNT SETTINGS
            </button>
          </router-link>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
