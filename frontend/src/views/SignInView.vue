<script>
import { defineComponent } from "vue";
import { emailPasswordSignIn } from "supertokens-web-js/recipe/thirdpartyemailpassword";
import * as Session from "supertokens-web-js/recipe/session";
import { mapActions } from "vuex";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import SpinnerComponent from "../components/spinnerComponent.vue";

export default defineComponent({
  data() {
    return {
      email: "",
      password: "",
      loading: false,
      signInButtonText: "SIGN IN",
    };
  },
  methods: {
    ...mapActions("userStore", ["getSession", "getUserInfo"]),
    signInClicked: async function (email, password) {
      this.loading = true;
      try {
        let response = await emailPasswordSignIn({
          formFields: [
            {
              id: "email",
              value: email,
            },
            {
              id: "password",
              value: password,
            },
          ],
        });

        if (response.status === "FIELD_ERROR") {
          response.formFields.forEach((formField) => {
            if (formField.id === "email") {
              this.loading = false;
              // Email validation failed (for example incorrect email syntax).
              window.alert(formField.error);
            }
          });
        } else if (response.status === "WRONG_CREDENTIALS_ERROR") {
          this.loading = false;
          window.alert("Email password combination is incorrect.");
        } else {
          await this.getSession;
          let userId = await Session.getUserId();
          if (userId) {
            this.loading = false;
            this.$router.push("/auth/" + userId + "/chat");
          }
        }
      } catch (err) {
        if (err.isSuperTokensGeneralError === true) {
          this.loading = false;
          // this may be a custom error message sent from the API by you.
          window.alert(err.message);
        } else {
          this.loading = false;
          window.alert("Oops! Something went wrong.");
        }
      }
    },
    toSignUp() {
      this.$router.push("/signup");
    },
    toForgotPassword() {
      this.$router.push("/password-reset");
    },
  },
  components: {
    navBar,
    navFooter,
    SpinnerComponent,
  },
});
</script>

<template>
  <main style="min-height: 71vh">
    <navBar></navBar>
    <div class="container-fluid h-100 bg-primary text-white">
      <div class="container d-flex justify-content-center pt-5 pb-5">
        <div class="card text-bg-light text-center mb-3" style="width: 32rem">
          <div class="card-header pt-3 pb-3">
            <img
              src="../assets/panda.png"
              class="w-20 h-20"
              alt="panda"
              width="50"
            />
            <h2 class="pt-3">SIGN IN</h2>
            <p>NOT REGISTERED YET?</p>
            <button type="button" class="btn btn-secondary" @click="toSignUp()">
              SIGN UP
            </button>
          </div>
          <div class="card-body pt-5 pb-4 px-5">
            <div class="form-floating mb-3">
              <input
                type="email"
                ref="email"
                v-model="this.email"
                class="form-control"
                id="floatingInput"
                placeholder="kung-fu@panda.ai"
                autocomplete="email"
              />
              <label for="floatingInput">Email</label>
            </div>
            <div class="form-floating">
              <input
                type="password"
                ref="password"
                v-model="this.password"
                class="form-control"
                id="floatingPassword"
                placeholder="sKad00sh"
                autocomplete="password"
                @keyup.enter="signInClicked(this.email, this.password)"
              />
              <label for="floatingPassword">Password</label>
            </div>
            <div class="pt-5">
              <button
                type="button"
                class="btn btn-secondary btn-lg d-inline-flex justify-content-center"
                style="width: 300px"
                @click="signInClicked(this.email, this.password)"
              >
                <SpinnerComponent
                  :loading="this.loading"
                  :button-text="this.signInButtonText"
                ></SpinnerComponent>
              </button>
            </div>
            <h4
              class="pt-4"
              @click="toForgotPassword()"
              style="cursor: pointer"
            >
              FORGOT PASSWORD?
            </h4>
          </div>
          <div class="card-footer pt-4 pb-4">
            <button
              type="button"
              class="btn btn-outline-primary d-inline-flex justify-content-center"
              style="width: 300px; margin: 7px"
            >
              <SpinnerComponent :loading="this.loadingGitHub"></SpinnerComponent
              ><img class="thirdPartLogo" src="../assets/icons/github.svg" />Sign In With GitHub
            </button>
            <button
              type="button"
              class="btn btn-outline-primary d-inline-flex justify-content-center"
              style="width: 300px; margin: 7px"
            >
              <SpinnerComponent :loading="this.loadingGoogle"></SpinnerComponent
              ><img class="thirdPartLogo" src="../assets/icons/google.svg" />Sign In With Google
            </button>
            <button
              type="button"
              class="btn btn-outline-primary d-inline-flex justify-content-center"
              style="width: 300px; margin: 7px"
            >
              <SpinnerComponent :loading="this.loadingApple"></SpinnerComponent
              ><img class="thirdPartLogo" src="../assets/icons/apple.svg" />Sign In With Apple
            </button>
            <button
              type="button"
              class="btn btn-outline-primary d-inline-flex justify-content-center"
              style="width: 300px; margin: 7px"
            >
              <SpinnerComponent :loading="this.loadingFacebook"></SpinnerComponent
              ><img class="thirdPartLogo" src="../assets/icons/facebook.svg" />Sign In With Facebook
            </button>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
.thirdPartLogo {
  margin-top: 4px;
  margin-right: 12px;
}
</style>
