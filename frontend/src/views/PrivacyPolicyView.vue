<script lang="ts">
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";

export default defineComponent({
  methods: {
    redirectToLogin() {
      window.location.href = "/auth";
    },
    async onLogout() {
      await Session.signOut();
      window.location.reload();
    },
  },
});
</script>

<template>
  <main>
    <div className="body">
      <div>
        <img src="../../src/assets/panda.png" width="200"/>
        <h1>PRIVACY POLICY</h1>
      </div>
    </div>
  </main>
</template>
<style scoped>
@import "../assets/styles/panda-main.css";
</style>
