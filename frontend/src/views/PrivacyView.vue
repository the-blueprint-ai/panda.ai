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
        <div class="aboutContainerLine"></div>
        <h2>Powered by chatGPT 🔋</h2>
        <p>
          🐼 panda.ai is built on top of open.ai's ChatGPT Large Language
          Model(LLM) Artificial Intelligence. As an AI language model, it's
          limitations primarily stem from it's training data and inherent
          design. While it can provide vast amounts of information, it's
          knowledge is limited to what it's been trained on and the additional
          data 🐼 panda.ai provides it. Consequently, it can lack real-time
          awareness and might be unfamiliar with recent events or developments.
        </p>
        <p>
          Additionally, chatGPT's understanding of context and nuance may be
          limited, which can sometimes lead to inaccuracies or
          misinterpretations. Though it strives to be neutral and unbiased,
          chatGPT's training data may contain biases present in the text it was
          trained on, inadvertently affecting it's responses.
        </p>
        <p>
          🐼 panda.ai is built on open.ai's 4th generation chatGPT model, and
          you can find out more information about it's limitations and nuances,
          by reading the paper that open.ai published
          <a
            href="https://cdn.openai.com/papers/gpt-4-system-card.pdf"
            target="_blank"
            >here</a
          >. It details chatGPT 4's limitations and also how it has improved
          upon previous generations of chatGPT.
        </p>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
@import "../assets/styles/panda-main.css";
</style>
