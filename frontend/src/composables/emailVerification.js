import { sendVerificationEmail } from "supertokens-web-js/recipe/emailverification";
import router from "../router";

export async function emailVerification(userId, toast) {
  try {
    let response = await sendVerificationEmail();
    if (response.status === "EMAIL_ALREADY_VERIFIED_ERROR") {
      // Redirect the user to onboarding
      router.push(userId + "/onboarding");
    } else {
      // email was sent successfully
      toast.success("Verification email sent.");
      router.push("/auth/email");
    }
  } catch (err) {
    console.error(err);
    if (err.isSuperTokensGeneralError === true) {
      toast.error(err.message);
    } else {
      toast.error(
        "Sorry, we couldn't complete your request. Please try again later."
      );
    }
  }
}
