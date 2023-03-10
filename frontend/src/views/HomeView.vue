<script lang="ts">
import * as Session from "supertokens-web-js/recipe/session";
import { defineComponent } from "vue";

export default defineComponent({
  data() {
    return {
      session: false,
      userId: "",
    };
  },
  mounted() {
    this.getUserInfo();
  },
  methods: {
    redirectToLogin() {
      window.location.href = "/auth";
    },
    async getUserInfo() {
      this.session = await Session.doesSessionExist();
      if (this.session) {
        this.userId = await Session.getUserId();
      }
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
      <img src="../../src/assets/panda.png" width="200"/>
      <h1>Welcome to panda.ai</h1>

      <div v-if="session">
        <h2>Your UserId Is:</h2>
        <h3>{{ userId }}</h3>

        <button @click="onLogout">Sign Out</button>
      </div>
      <div v-else>
        <button @click="redirectToLogin">Sign In</button>
      </div>
    </div>
  </main>
</template>
<style scoped>
.body {
  background-color: #000000;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-family: "Monaco"; /*"Helvetica Neue", "Arial", sans-serif;*/
}
.user {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: baseline;
  padding: 0.1rem;
}
span {
  margin-right: 0.3rem;
  font-size: large;
}
h3 {
  color: #FFFFFF;
}
h2 {
  color: #FFFFFF;
}
h1 {
  color: #FFFFFF;
  text-transform: uppercase;
  font-size: 4em;
  font-weight: 100;
}
button {
  cursor: pointer;
  background-color: #FFFFFF;
  border: none;
  padding: 1rem;
  margin: 2rem;
  transition: all 0.5s ease-in-out;
  border: 5px solid #FFFFFF;
  border-radius: 2rem;
  font-size: large;
  font-family: "Monaco";
  width: 200px;
}
button:hover {
  /*transform: scale(1.1);*/
  background-color: #000000;
  color: #FFFFFF;
  border: 5px solid #FFFFFF;
}
</style>
