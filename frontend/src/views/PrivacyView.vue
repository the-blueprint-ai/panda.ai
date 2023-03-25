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
      <div class="aboutContainer">
        <h2>At 🐼 panda.ai, Privacy Matters 🛡️</h2>
        <p>
          We believe that privacy is a fundamental human right, and we take it
          very seriously. That's why we've built our entire platform with your
          privacy and data ownership in mind. We don't believe in hiding behind
          jargon or complex terms; instead, we strive for full transparency and
          open communication with all our users.
        </p>
        <div class="aboutContainerLine"></div>
        <h2>Here's our commitment to you: 🤝</h2>
        <ol type="1">
          <li>
            No Jargon 🚫
            <p>
              We promise to keep things simple and straightforward, so you
              always know exactly what's happening with your data.
            </p>
          </li>
          <li>
            Full Transparency 🌟
            <p>
              We're an open book, and we want you to be confident in how we
              handle your data. If you ever have any questions or concerns, just
              reach out to us, and we'll be happy to clarify.
            </p>
          </li>
          <li>
            Complete Data Ownership 💾
            <p>
              You have the ability to see all your data at any time. It's your
              data, and you should have full control over it.
            </p>
          </li>
          <li>
            Data Deletion 🔨
            <p>
              If you ever decide that you no longer want to use 🐼 panda.ai, you
              can delete your data at any time. We'll never hold your data
              hostage.
            </p>
          </li>
          <li>
            AI Model Training 🤖
            <p>
              We don't train any AI models on your data. The only information we
              use is the chat history between you and your 🐼 panda.ai personal
              assistant, ensuring your privacy remains intact.
            </p>
          </li>
        </ol>
        <div class="aboutContainerLine"></div>
        <p>
          At 🐼 panda.ai, our goal is to provide a personalized and trustworthy
          experience that puts you, the user, in control. We're dedicated to
          protecting your privacy and ensuring you have the peace of mind to
          enjoy all the benefits our AI personal assistant has to offer.
        </p>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
@import "../assets/styles/panda-main.css";
</style>
