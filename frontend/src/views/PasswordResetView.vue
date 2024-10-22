<script>
import { defineComponent } from "vue";
import { sendPasswordResetEmail } from "supertokens-web-js/recipe/thirdpartyemailpassword";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import SpinnerComponent from "../components/spinnerComponent.vue";
import { useToast } from "vue-toastification";

export default defineComponent({
  data() {
    return {
      email: "",
      sendButtonText: "SEND",
      loading: false,
      formSubmitted: false,
    };
  },
  mounted() {},
  computed: {
    isEmailValid() {
      return this.validateEmail(this.email);
    },
  },
  methods: {
    validateEmail: function (email) {
      var re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
    sendEmailClicked: async function (email) {
      const toast = useToast();
      this.formSubmitted = true;
      this.loading = true;
      try {
        let response = await sendPasswordResetEmail({
          formFields: [
            {
              id: "email",
              value: email,
            },
          ],
        });

        if (response.status === "FIELD_ERROR") {
          // one of the input formFields failed validaiton
          response.formFields.forEach((formField) => {
            if (formField.id === "email") {
              // Email validation failed (for example incorrect email syntax).
              toast.error(formField.error);
            }
          });
        } else {
          this.loading = false;
          // reset password email sent.
          toast.success("Reset password email sent!");
          toast.info("Please check your email for the password reset link");
        }
      } catch (err) {
        if (err.isSuperTokensGeneralError === true) {
          // this may be a custom error message sent from the API by you.
          toast.error(err.message);
        } else {
          toast.error("Oops! Something went wrong. Please try again later.");
        }
      }
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
    <div class="mainContainer container-fluid bg-primary text-white">
      <div class="container d-flex justify-content-center pt-5 pb-5">
        <div class="card text-bg-light text-center mb-3" style="width: 32rem">
          <div class="card-header pt-3 pb-3">
            <img
              src="../assets/panda.png"
              class="w-20 h-20"
              alt="panda"
              width="50"
            />
            <h2 class="pt-3">PASSWORD RESET</h2>
          </div>
          <div class="card-body pt-4 pb-4 px-5">
            <p>Please enter your email below to reset your password:</p>
            <div class="form-floating mb-3">
              <input
                type="email"
                ref="email"
                v-model="this.email"
                class="form-control"
                id="floatingInput"
                placeholder="kung-fu@panda.ai"
                autocomplete="email"
                @keyup.enter="sendEmailClicked(this.email)"
                :class="{
                  'is-valid': this.email.length > 0 && isEmailValid,
                  'is-invalid': formSubmitted && !isEmailValid,
                }"
                required
              />
              <label for="floatingInput">Email</label>
              <div class="valid-feedback">🐼 Looks good!</div>
              <div
                id="validationServerUsernameFeedback"
                class="invalid-feedback"
              >
                Please enter a valid email address.
              </div>
            </div>
            <div class="pt-4">
              <button
                type="button"
                class="btn btn-secondary btn-lg mb-3 d-inline-flex justify-content-center"
                style="width: 70%"
                @click="sendEmailClicked(this.email)"
              >
                <SpinnerComponent
                  :loading="this.loading"
                  :button-text="this.sendButtonText"
                ></SpinnerComponent>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
