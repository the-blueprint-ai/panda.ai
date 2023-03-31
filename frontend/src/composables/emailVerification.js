import * as Session from "supertokens-web-js/recipe/session";
import { sendVerificationEmail } from "supertokens-web-js/recipe/emailverification";

export async function emailVerification() {
  try {
    let response = await sendVerificationEmail();
    if (response.status === "EMAIL_ALREADY_VERIFIED_ERROR") {
      // This can happen if the info about email verification in the session was outdated.
      // Redirect the user to the home page
      await this.getSession();
      let userId = await Session.getUserId();
      this.$router.push(userId + "/onboarding");
      // window.location.assign = userId + "/onboarding";
    } else {
      // email was sent successfully
      this.$router.push("/auth/email");
      // window.location.href = "/auth/email";
    }
  } catch (err) {
    console.error(err);
    if (err.isSuperTokensGeneralError === true) {
      // this may be a custom error message sent from the API by you.
      window.alert(err.message);
    } else {
      window.alert("Sorry, we couldn't complete your request. Please try again later.");
    }
  }
}


// await this.getSession();
// let userId = await Session.getUserId();
// console.log("From emailVerification.js - userId: " + userId + "email: " + email);
// saveEmail(userId, email);