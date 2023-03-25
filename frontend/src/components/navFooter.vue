<script>
export default {};
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
          <img src="../assets/icons/discord.svg" />
          <img src="../assets/icons/twitter.svg" />
          <img src="../assets/icons/linkedin.svg" />
          <img src="../assets/icons/envelope-at-fill.svg" />
        </div>
        <h3>© panda.ai 2023</h3>
      </div>
      <div class="footerMenus">
        <div class="singleMenu">
          <h2>Links</h2>
          <p>home</p>
          <p>roadmap</p>
          <p>privacy</p>
        </div>
        <div class="singleMenu">
          <h2>Company</h2>
          <p>about</p>
          <p>terms of service</p>
          <p>privacy policy</p>
        </div>
        <div class="singleMenu">
          <h2>Support</h2>
          <p>support</p>
          <p>contact us</p>
        </div>
        <div class="singleMenu">
          <h2>Social</h2>
          <p>Discord</p>
          <p>Twitter</p>
          <p>LinkedIn</p>
        </div>
      </div>
    </div>
  </div>
</template>
