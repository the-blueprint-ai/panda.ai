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
        <h2>About 🐼 panda.ai</h2>
        <p>
          Welcome to 🐼 panda.ai, where we believe in the power of personalised
          AI experiences and giving users complete control over their own data.
          Founded in 2023, we're on a mission to change the AI chatbot landscape
          by ensuring that our users have full ownership and control of their
          digital lives.
        </p>
        <h2>The Platform 🐼</h2>
        <p>
          🐼 panda.ai is an artificial intelligence personal assistant designed
          to learn from you and adapt to your unique needs. As you interact with
          🐼 panda.ai, it will evolve and grow, learning from your
          conversations, web browsing behaviour, social media activity, music
          preferences, and even your spending habits. Our goal is to create a
          highly personalised digital assistant that knows and understands each
          user individually.
        </p>
        <div class="aboutContainerLine"></div>
        <div class="aboutBox">
          <h2>What Sets Us Apart 🔐</h2>
          <p>
            At 🐼 panda.ai, we're not like other large digital platforms. We
            believe in putting the user first, which means giving you complete
            ownership and control of your data. It's a whole new approach to AI
            that emphasises data privacy and ethical practices.
          </p>
        </div>
        <div class="aboutBox">
          <h2>Powered by OpenAI's ChatGPT LLM 🔋</h2>
          <p>
            While we don't have any significant partnerships or collaborations
            to mention, it's worth noting that our AI is built on top of
            OpenAI's ChatGPT LLM, the technology foundation that powers 🐼
            panda.ai's awesomeness.
          </p>
        </div>
        <div class="aboutBox">
          <h2>Our Core Values 🦄</h2>
          <p>At 🐼 panda.ai, we live by three core values:</p>
          <ol type="1">
            <li>Challenging the status quo 💪</li>
            <li>Curiosity 🧐</li>
            <li>Collaboration 🤝</li>
          </ol>
          <p>
            These values guide our mission to revolutionize the AI chatbot
            industry and provide users with a truly personalized and ethical AI
            experience.
          </p>
        </div>
        <div class="aboutBox">
          <h2>Our Vision for the Future 🔮</h2>
          <p>
            🐼 panda.ai aspires to provide a fully personalized AI assistant
            that caters to all of your digital needs. In the future, we aim to
            create a platform that not only understands each user individually
            but can also preempt and predict your needs, making your digital
            life more seamless and enjoyable.
          </p>
        </div>
        <div class="aboutContainerLine"></div>
        <h3>
          Join us on our mission to make AI chatbots more personal, ethical, and
          fun! 🤓
        </h3>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
@import "../assets/styles/panda-main.css";
</style>
