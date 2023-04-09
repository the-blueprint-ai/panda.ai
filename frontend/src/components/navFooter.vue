<script>
export default {
  methods: {
    goToPage(route) {
      this.$router.push(route);
    },
    navigate(event) {
      const navigateTo = event.target.getAttribute("navigate-to");
      if (navigateTo == "home") {
        this.$router.push("/");
      } else if (navigateTo == "discord") {
        window.open("https://www.discord.com", "_blank");
      } else if (navigateTo == "twitter") {
        window.open("https://twitter.com/mypanda_ai", "_blank");
      } else if (navigateTo == "linkedin") {
        window.open("https://www.linkedin.com", "_blank");
      } else {
        this.$router.push(navigateTo);
      }
    },
  },
};
</script>

<template>
  <div class="navFooter">
    <div class="footerbar"></div>
    <div class="footerContainer">
      <div class="brandSocialsHolder">
        <div class="footerBranding">
          <div class="brandHolder">
            <router-link to="/">
              <img class="logo" src="../../src/assets/panda.png" width="50" />
            </router-link>
            <div class="brandText">
              <h2>panda.ai</h2>
              <p>MADE WITH ❤️</p>
            </div>
          </div>
        </div>
        <div class="socialsHolder">
          <img
            navigate-to="discord"
            @click="navigate($event)"
            src="../assets/icons/discord.svg"
          />
          <img
            navigate-to="twitter"
            @click="navigate($event)"
            src="../assets/icons/twitter.svg"
          />
          <img
            navigate-to="linkedin"
            @click="navigate($event)"
            src="../assets/icons/linkedin.svg"
          />
          <a :href="'mailto:contact@mypanda.ai?subject=Hello!'">
            <img
              navigate-to="contact"
              src="../assets/icons/envelope-at-fill.svg"
            />
          </a>
        </div>
        <h3>©panda.ai 2023</h3>
      </div>
      <div class="footerMenus">
        <div class="singleMenu">
          <h2>Links</h2>
          <p navigate-to="home" @click="goToPage('/')">home</p>
          <p navigate-to="roadmap" @click="goToPage('/roadmap')">roadmap</p>
          <p navigate-to="privacy" @click="goToPage('/privacy')">privacy</p>
        </div>
        <div class="singleMenu">
          <h2>Company</h2>
          <p navigate-to="about" @click="goToPage('/about')">about</p>
          <p navigate-to="terms-of-service" @click="goToPage('/terms-of-service')">
            terms of service
          </p>
          <p navigate-to="privacy-policy" @click="goToPage('/privacy-policy')">
            privacy policy
          </p>
        </div>
        <div class="singleMenu">
          <h2>Support</h2>
          <p navigate-to="support" @click="goToPage('/support')">support</p>
          <p navigate-to="contact" @click="goToPage('/support')">contact us</p>
        </div>
        <div class="singleMenu">
          <h2>Social</h2>
          <p navigate-to="discord" @click="navigate($event)">Discord</p>
          <p navigate-to="twitter" @click="navigate($event)">Twitter</p>
          <p navigate-to="linkedin" @click="navigate($event)">LinkedIn</p>
        </div>
      </div>
    </div>
  </div>
</template>
