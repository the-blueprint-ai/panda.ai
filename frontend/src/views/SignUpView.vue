<script>
import { defineComponent } from "vue";
import { mapMutations } from "vuex";
import {
  emailPasswordSignUp,
  doesEmailExist,
} from "supertokens-web-js/recipe/thirdpartyemailpassword";
import { emailVerification } from "../composables/emailVerification.js";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import SpinnerComponent from "../components/spinnerComponent.vue";
import { useToast } from "vue-toastification";

export default defineComponent({
  data() {
    return {
      email: "",
      password: "",
      isTyping: false,
      emailTimer: null,
      emailExistsError: "",
      emailChecking: true,
      emailOk: "",
      passwordOk: "",
      badPasswordError: "",
      loading: false,
      loadingGitHub: false,
      loadingGoogle: false,
      loadingApple: false,
      loadingFacebook: false,
      signUpButtonText: "SIGN UP",
      agreeToSPP: false,
      formSubmitted: false,
    };
  },
  watch: {
    email(newValue) {
      // Clear the previous timer (if there was one)
      clearTimeout(this.emailTimer);

      // Start a new timer for 1000ms
      this.emailTimer = setTimeout(() => {
        this.checkEmail(newValue);
      }, 400);
    },
    password() {
      if (this.isPasswordValid == true) {
        this.passwordOk = "ok";
        this.badPasswordError = "";
      } else {
        this.passwordOk = "no";
        this.badPasswordError =
          "Your password must be at least 8 characters long and include one lowercase, one uppercase and a number.";
      }
    },
    isCheckboxValid() {
      return this.agreeToSPP;
    },
  },
  computed: {
    isEmailValid() {
      return this.validateEmail(this.email);
    },
    isPasswordValid() {
      return this.validatePassword(this.password);
    },
  },
  methods: {
    ...mapMutations("userStore", {
      setStoreUserId: "setStoreUserId",
      setStoreEmail: "setStoreEmail",
    }),
    emailVerification,
    validateEmail: function (email) {
      var re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
    validatePassword: function (password) {
      const regex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])[a-zA-Z\d!@#$%^&*()]{8,}$/;
      return regex.test(password);
    },
    signUpClicked: async function (email, password) {
      const toast = useToast();
      this.formSubmitted = true;
      this.loading = true;

      // Check if the form is valid and if the user has agreed to the ToS and PP before making the API calls
      if (!this.isEmailValid || !this.isPasswordValid || !this.agreeToSPP) {
        this.loading = false;
        return;
      }

      try {
        let response = await emailPasswordSignUp({
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
          // one of the input formFields failed validaiton
          response.formFields.forEach((formField) => {
            if (formField.id === "email") {
              // Email validation failed (for example incorrect email syntax),
              // or the email is not unique.
              this.loading = false;
              toast.error(formField.error);
            } else if (formField.id === "password") {
              // Password validation failed.
              // Maybe it didn't match the password strength
              this.loading = false;
              toast.error(formField.error);
            }
          });
        } else if (response.status === "OK") {
          // sign up successful. The session tokens are automatically handled by
          // the frontend SDK.
          toast.success("Sign up successful!");
          let userId = response.user.id;
          let userEmail = response.user.email;
          this.setStoreUserId(userId);
          this.setStoreEmail(userEmail);
          emailVerification(userId, toast);
        }
      } catch (err) {
        if (err.isSuperTokensGeneralError === true) {
          // this may be a custom error message sent from the API by you.
          this.loading = false;
          toast.error(err.message);
        } else {
          this.loading = false;
          toast.error("Oops! Something went wrong. Please try again later.");
        }
      }
    },
    checkEmail: async function (email) {
      const toast = useToast();
      try {
        let response = await doesEmailExist({
          email,
        });

        if (response.doesExist) {
          this.emailChecking = false;
          toast.warning("Email already in use. Please sign in instead");
          this.emailExistsError =
            "Email already in use. Please sign in instead";
          this.emailOk = "no";
          setTimeout(() => {
            this.emailExistsError = "";
            this.emailOk = "";
            this.email = "";
            this.$refs.email.value = null;
            this.emailChecking = true;
          }, 3600);
        } else {
          this.emailChecking = false;
          setTimeout(() => {
            this.emailOk = "ok";
          }, 3000);
        }
      } catch (err) {
        toast.error(err);
        if (err.isSuperTokensGeneralError === true) {
          // this may be a custom error message sent from the API by you.
          toast.error(err.message);
        } else {
          toast.error("Oops! Something went wrong. Please try again later.");
        }
      }
    },
    toSignIn() {
      this.$router.push("/signin");
    },
    toToS() {
      window.open("/terms-of-service", "_blank");
    },
    toPP() {
      window.open("/privacy-policy", "_blank");
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
  <main>
    <navBar></navBar>
    <div class="container-fluid vh-100 bg-primary text-white">
      <div class="container d-flex justify-content-center pt-5 pb-5">
        <div class="card text-bg-light text-center mb-3" style="width: 32rem">
          <div class="card-header pt-3 pb-3">
            <img
              src="../assets/panda.png"
              class="w-20 h-20"
              alt="panda"
              width="50"
            />
            <h2 class="pt-3">SIGN UP</h2>
            <p>ALREADY HAVE AN ACCOUNT?</p>
            <button type="button" class="btn btn-secondary" @click="toSignIn()">
              SIGN IN
            </button>
          </div>
          <div class="card-body pt-5 pb-4 px-5">
            <form class="needs-validation" novalidate>
              <div class="form-floating mb-3">
                <input
                  type="email"
                  ref="email"
                  v-model="this.email"
                  class="form-control"
                  id="floatingInput"
                  placeholder="kung-fu@panda.ai"
                  autocomplete="email"
                  :class="{
                    'is-valid': this.email.length > 0 && !emailExistsError,
                    'is-invalid': emailExistsError,
                  }"
                  required
                />
                <label for="floatingInput">Email</label>
                <div class="valid-feedback">🐼 Looks good!</div>
                <div
                  v-if="emailExistsError"
                  class="invalid-feedback text-danger"
                >
                  {{ this.emailExistsError }}
                </div>
                <div
                  id="validationServerUsernameFeedback"
                  class="invalid-feedback"
                >
                  Please enter a valid email address.
                </div>
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
                  :class="{
                    'is-valid': this.password.length > 0 && isPasswordValid,
                    'is-invalid': this.password.length > 0 && !isPasswordValid,
                  }"
                  required
                />
                <label for="floatingPassword">Password</label>
                <div class="valid-feedback">🐼 Looks good!</div>
                <div
                  id="validationServerUsernameFeedback"
                  class="invalid-feedback"
                >
                  Please enter a valid password.
                </div>
                <div id="passwordHelpBlock" class="form-text">
                  Your password must be at least 8 characters long and include
                  one lowercase, one uppercase, a number and a special
                  character.
                </div>
              </div>
              <div class="form-check ms-4 pt-4 pb-4 px-4">
                <input
                  type="checkbox"
                  class="form-check-input mt-3"
                  id="ToS&PP"
                  v-model="agreeToSPP"
                  :class="{
                    'is-valid': formSubmitted && agreeToSPP,
                    'is-invalid': formSubmitted && !agreeToSPP,
                  }"
                  required
                />
                <label class="form-check-label" for="ToS&PP"
                  >Please agree to our
                  <a
                    class="text-secondary"
                    @click="toToS"
                    style="text-decoration: none"
                    >Terms of Service</a
                  >
                  and
                  <a
                    class="text-secondary"
                    @click="toPP"
                    style="text-decoration: none"
                    >Privacy Policy</a
                  >
                  to continue.</label
                >
                <div
                  v-if="formSubmitted && !agreeToSPP"
                  class="invalid-feedback d-block"
                >
                  You must agree before submitting.
                </div>
              </div>
              <div class="pt-1">
                <button
                  @click="signUpClicked(this.email, this.password)"
                  type="button"
                  class="btn btn-secondary btn-lg d-inline-flex justify-content-center mb-4"
                  style="width: 70%"
                  :disabled="
                    this.email.length == 0 ||
                    this.password.length == 0 ||
                    emailExistsError ||
                    !isPasswordValid ||
                    !agreeToSPP
                  "
                >
                  <SpinnerComponent
                    :loading="this.loading"
                    :button-text="this.signUpButtonText"
                  ></SpinnerComponent>
                </button>
              </div>
            </form>
          </div>
          <!-- <div class="card-footer pt-4 pb-4">
            <button
              type="button"
              class="btn btn-outline-primary d-inline-flex justify-content-center"
              style="width: 300px; margin: 7px"
              disabled
            >
              <SpinnerComponent :loading="this.loadingGitHub"></SpinnerComponent
              ><img
                class="thirdPartLogo"
                src="../assets/icons/github.svg"
              />Sign Up With GitHub
            </button>
            <button
              type="button"
              class="btn btn-outline-primary d-inline-flex justify-content-center"
              style="width: 300px; margin: 7px"
              disabled
            >
              <SpinnerComponent :loading="this.loadingGoogle"></SpinnerComponent
              ><img
                class="thirdPartLogo"
                src="../assets/icons/google.svg"
              />Sign Up With Google
            </button>
            <button
              type="button"
              class="btn btn-outline-primary d-inline-flex justify-content-center"
              style="width: 300px; margin: 7px"
              disabled
            >
              <SpinnerComponent :loading="this.loadingApple"></SpinnerComponent
              ><img class="thirdPartLogo" src="../assets/icons/apple.svg" />Sign
              Up With Apple
            </button>
            <button
              type="button"
              class="btn btn-outline-primary d-inline-flex justify-content-center"
              style="width: 300px; margin: 7px"
              disabled
            >
              <SpinnerComponent
                :loading="this.loadingFacebook"
              ></SpinnerComponent
              ><img
                class="thirdPartLogo"
                src="../assets/icons/facebook.svg"
              />Sign Up With Facebook
            </button>
          </div> -->
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style scoped>
.form-check a {
  color: #ffcb4c;
}
.form-check a:hover {
  color: #ffcb4c;
  cursor: pointer;
}
.thirdPartLogo {
  margin-top: 4px;
  margin-right: 12px;
}
</style>
