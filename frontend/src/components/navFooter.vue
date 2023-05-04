<script>
export default {
  methods: {
    redirectToHome() {
      this.$router.push("/");
    },
    goToPage(route) {
      this.$router.push(route);
    },
    navigate(event) {
      const navigateTo = event.target.getAttribute("navigate-to");
      if (navigateTo == "home") {
        this.$router.push("/");
      } else if (navigateTo == "discord") {
        window.open("https://discord.gg/8GnUbDKUFV", "_blank");
      } else if (navigateTo == "twitter") {
        window.open("https://twitter.com/mypanda_ai", "_blank");
      } else if (navigateTo == "linkedin") {
        window.open("https://www.linkedin.com/company/my-panda-ai", "_blank");
      } else {
        this.$router.push(navigateTo);
      }
    },
  },
};
</script>

<template>
  <div class="row h-200 pt-5 pb-3 bg-white">
    <div class="col-sm-2 px-5">
      <div class="row pb-5" @click="redirectToHome" style="min-width: 300px">
        <img class="w-25 h-25" src="../../src/assets/panda.png"  style="min-width: 100px" />
        <div class="col mt-n2" style="min-width: 150px">
          <h4 class="pt-3 lh-1">panda.ai</h4>
          <p class="lh-1">MADE WITH ❤️</p>
        </div>
      </div>
      <div class="row ps-2 list-unstyled" style="min-width: 250px">
        <div class="col-3" style="min-width: 50px">
          <li class="nav-item">
            <img
              navigate-to="discord"
              @click="navigate($event)"
              src="../assets/icons/discord.svg"
              width="30"
              height="30"
            />
          </li>
        </div>
        <div class="col-3" style="min-width: 50px">
          <li class="nav-item">
            <img
              navigate-to="twitter"
              @click="navigate($event)"
              src="../assets/icons/twitter.svg"
              width="30"
              height="30"
            />
          </li>
        </div>
        <div class="col-3" style="min-width: 50px">
          <li class="nav-item">
            <img
              navigate-to="linkedin"
              @click="navigate($event)"
              src="../assets/icons/linkedin.svg"
              width="30"
              height="30"
            />
          </li>
        </div>
        <div class="col-3" style="min-width: 50px">
          <li class="nav-item">
            <a :href="'mailto:contact@mypanda.ai?subject=Hello!'">
              <img
                navigate-to="contact"
                src="../assets/icons/envelope-at-fill.svg"
                width="30"
                height="30"
              />
            </a>
          </li>
        </div>
      </div>
    </div>
    <div class="bottomLinks nav col-sm-10 justify-content-end px-5">
      <div class="col-1" style="min-width: 150px">
        <h3 class="pb-3"><strong>LINKS</strong></h3>
        <p class="ps-1 lh-1" navigate-to="home" @click="goToPage('/')">home</p>
        <p class="ps-1 lh-1" navigate-to="roadmap" @click="goToPage('/roadmap')">
          roadmap
        </p>
        <p class="ps-1 lh-1" navigate-to="privacy" @click="goToPage('/privacy')">
          privacy
        </p>
      </div>
      <div class="col-1" style="min-width: 150px">
        <h3 class="pb-3"><strong>COMPANY</strong></h3>
        <p class="ps-1 lh-1" navigate-to="about" @click="goToPage('/about')">
          about
        </p>
        <p class="ps-1 lh-1" navigate-to="about" @click="goToPage('/pricing')">
          pricing
        </p>
        <p
          class="ps-1 lh-1"
          navigate-to="terms-of-service"
          @click="goToPage('/terms-of-service')"
        >
          terms of service
        </p>
        <p
          class="ps-1 lh-1"
          navigate-to="privacy-policy"
          @click="goToPage('/privacy-policy')"
        >
          privacy policy
        </p>
      </div>
      <div class="col-1" style="min-width: 150px">
        <h3 class="pb-3"><strong>SUPPORT</strong></h3>
        <p class="ps-1 lh-1" navigate-to="support" @click="goToPage('/support')">
          support
        </p>
        <p class="ps-1 lh-1" navigate-to="contact" @click="goToPage('/support')">
          contact us
        </p>
      </div>
      <div class="col-1" style="min-width: 150px">
        <h3 class="pb-3"><strong>SOCIAL</strong></h3>
        <p class="ps-1 lh-1" navigate-to="discord" @click="navigate($event)">
          Discord
        </p>
        <p class="ps-1 lh-1" navigate-to="twitter" @click="navigate($event)">
          Twitter
        </p>
        <p class="ps-1 lh-1" navigate-to="linkedin" @click="navigate($event)">
          LinkedIn
        </p>
      </div>
    </div>
    <div class="copywright row px-5 pt-3 text-center"><h5>©panda.ai 2023</h5></div>
  </div>
</template>

<style scoped>
p:hover {
  cursor: pointer;
  text-decoration: underline;
}
h4:hover {
  cursor: pointer;
}
img:hover {
  cursor: pointer;
}
@media (max-width: 992px) {
  .bottomLinks {
    display: none;
  }
  .copywright {
    margin-top: 20px;
  }
}
</style>
