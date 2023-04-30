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
      <div class="container pt-5 pb-5">
        <h2>About 🐼 panda.ai</h2>
        <p>
          Welcome to 🐼 panda.ai, where we believe in the power of personalised
          AI experiences and giving users complete control over their own data.
          Founded in 2023, we're on a mission to change the AI chatbot landscape
          by ensuring that our users have full ownership and control of their
          digital lives.
        </p>
        <h2 class="mt-4">The platform 🐼</h2>
        <p class="mb-5">
          🐼 panda.ai is an artificial intelligence personal assistant designed
          to learn from you and adapt to your unique needs. As you interact with
          🐼 panda.ai, it will evolve and grow, learning from your
          conversations, web browsing behaviour, social media activity, music
          preferences, and even your spending habits. Our goal is to create a
          highly personalised digital assistant that knows and understands each
          user individually.
        </p>
        <div class="aboutContainerLine"></div>
        <div class="row">
          <div class="col d-flex justify-content-center">
            <div
              class="card text-bg-light text-center mb-5"
              style="width: 36rem"
            >
              <h5 class="card-header text-center">What Sets Us Apart 🔐</h5>
              <p class="card-text pt-3 pb-3 px-3">
                At 🐼 panda.ai, we're not like other large digital platforms. We
                believe in putting the user first, which means giving you
                complete ownership and control of your data. It's a whole new
                approach to AI that emphasises data privacy and ethical
                practices.
              </p>
            </div>
          </div>
          <div class="col d-flex justify-content-center">
            <div
              class="card text-bg-light text-center mb-5"
              style="width: 36rem"
            >
              <h5 class="card-header text-center">
                Powered by OpenAI's ChatGPT LLM 🔋
              </h5>
              <p class="card-text pt-3 pb-3 px-3">
                While we don't have any significant partnerships or
                collaborations to mention, it's worth noting that our AI is
                built on top of OpenAI's ChatGPT LLM, the technology foundation
                that powers 🐼 panda.ai's awesomeness.
              </p>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col d-flex justify-content-center">
            <div
              class="card text-bg-light text-center mb-5"
              style="width: 36rem"
            >
              <h5 class="card-header text-center">Our Core Values 🦄</h5>
              <p class="card-text pt-3 pb-3 px-3">
                At 🐼 panda.ai, we live by three core values:
              </p>
              <div class="d-inline-flex justify-content-center">
                <ol class="mt-n4 text-start" type="1">
                  <li>Challenging the status quo 💪</li>
                  <li>Curiosity 🧐</li>
                  <li>Collaboration 🤝</li>
                </ol>
              </div>
              <p class="card-text mt-n4 pt-3 pb-3 px-3">
                These values guide our mission to revolutionize the AI chatbot
                industry and provide users with a truly personalized and ethical
                AI experience.
              </p>
            </div>
          </div>
          <div class="col d-flex justify-content-center">
            <div
              class="card text-bg-light text-center mb-5"
              style="width: 36rem"
            >
              <h5 class="card-header text-center">
                Our Vision for the Future 🔮
              </h5>
              <p class="card-text pt-3 pb-3 px-3">
                🐼 panda.ai aspires to provide a fully personalized AI assistant
                that caters to all of your digital needs. In the future, we aim
                to create a platform that not only understands each user
                individually but can also preempt and predict your needs, making
                your digital life more seamless and enjoyable.
              </p>
            </div>
          </div>
        </div>
        <div class="aboutContainerLine"></div>
        <h3 class="text-center">
          Join us on our mission to make AI chatbots more personal, ethical, and
          fun! 🤓
        </h3>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
.aboutContainerLine {
  height: 1px;
  width: 100%;
  margin: 0px;
  margin-top: 15px;
  margin-bottom: 40px;
  display: flex;
  background-color: #ffffff;
}
</style>
