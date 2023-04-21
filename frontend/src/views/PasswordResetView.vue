<script>
import { defineComponent } from "vue";
import { sendPasswordResetEmail } from "supertokens-web-js/recipe/thirdpartyemailpassword";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";

export default defineComponent({
  data() {
    return {
      email: "",
    };
  },
  mounted() {},
  methods: {
    sendEmailClicked: async function (email) {
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
              window.alert(formField.error);
            }
          });
        } else {
          // reset password email sent.
          window.alert("Please check your email for the password reset link");
        }
      } catch (err) {
        if (err.isSuperTokensGeneralError === true) {
          // this may be a custom error message sent from the API by you.
          window.alert(err.message);
        } else {
          window.alert("Oops! Something went wrong.");
        }
      }
    },
  },
  components: {
    navBar,
    navFooter,
  },
});
</script>

<template>
  <main>
    <navBar></navBar>
    <div class="bodyG">
      <div class="emailSentContainer">
        <img id="emailSentPanda" src="../assets/panda.png" />
        <h2>PASSWORD RESET</h2>
        <img
          id="emailSentEnvelope"
          src="../assets/icons/envelope-paper-heart-fill.svg"
        />
        <div class="signInBar"></div>
        <p>Please enter your email below to reset your password:</p>
        <div class="emailPassword">
          <input
            ref="email"
            v-model="this.email"
            type="email"
            placeholder="kung-fu@panda.ai"
            @keyup.enter="sendEmailClicked(this.email)"
          />
          <button @click="sendEmailClicked(this.email)">SEND</button>
        </div>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
