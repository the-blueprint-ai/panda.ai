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
  <main style="min-height: 71vh">
    <navBar></navBar>
    <div class="container-fluid h-100 bg-primary text-white">
      <div class="container pt-5 pb-5">
        <h2 class="text-center">🐼 PANDA.AI TERMS OF SERVICE</h2>
        <div class="aboutContainerLine"></div>
        <h3 class="text-secondary">EFFECTIVE DATE: 1ST APRIL 2023</h3>
        <p class="mb-3">
          Please read these Terms of Service ("Terms") carefully before using
          the panda.ai chatbot and associated services (the "Services") provided
          by panda.ai ("us", "we", or "our"). By accessing or using our
          Services, you agree to be bound by these Terms. If you do not agree
          with any part of these Terms, you must not use our Services.
        </p>
        <div class="aboutContainerLine"></div>
        <ol type="1">
          <li>
            <h3 class="text-secondary">ELIGIBILITY</h3>
            <p class="mb-3">
            By using our Services, you represent and warrant that you are at
            least 18 years old and have the legal capacity to enter into these
            Terms. If you are under 18, you must have consent from a parent or
            legal guardian to use our Services.
          </p>
          </li>
          <li>
            <h3 class="text-secondary">ACCOUNT REGISTRATION</h3>
            <p class="mb-3">
            To use our Services, you may need to register for an account. You
            agree to provide accurate, complete, and up-to-date information when
            registering for an account. You are responsible for maintaining the
            confidentiality of your account credentials and for all activities
            that occur under your account.
          </p>
          </li>
          <li>
            <h3 class="text-secondary">ACCEPTABLE USE</h3>
            <p class="mb-3">
            You agree not to use our Services for any unlawful, harmful, or
            disruptive purpose or in any manner that violates these Terms. You
            agree not to:
            <ol type="a">
              <li>
                Engage in any harassing, threatening, or abusive behaviour.
              </li>
              <li>
                Attempt to interfere with the proper functioning of our Services
                or disrupt the experience of other users.
              </li>
              <li>
                Use our Services to send unsolicited or unauthorised advertising
                or promotional material.
              </li>
            </ol>
          </p>
          </li>
          <li>
            <h3 class="text-secondary">INTELLECTUAL PROPERTY RIGHTS</h3>
            <p class="mb-3">
            All content, features, and functionality of our Services, including
            but not limited to text, graphics, logos, and software, are the
            property of panda.ai or its licensors and are protected by
            copyright, trademark, and other intellectual property laws.
            Unauthorised use of our content or any part of our Services may
            result in legal action.
          </p>
          </li>
          <li>
            <h3 class="text-secondary">TERMINATION</h3>
            <p class="mb-3">
            We reserve the right to terminate or suspend your access to our
            Services, with or without notice, if we believe you have breached
            any provision of these Terms or if your use of our Services is
            harmful to our interests or the interests of other users.
          </p>
          </li>
          <li>
            <h3 class="text-secondary">DISCLAIMER OF WARRANTIES</h3>
            <p class="mb-3">
            Our Services are provided on an "as is" and "as available" basis. We
            make no warranties, expressed or implied, and hereby disclaim and
            negate all other warranties, including without limitation, implied
            warranties or conditions of merchantability, fitness for a
            particular purpose, or non-infringement of intellectual property or
            other violation of rights.
          </p>
          </li>
          <li>
            <h3 class="text-secondary">LIMITATION OF LIABILITY</h3>
            <p class="mb-3">
            In no event shall panda.ai or its suppliers be liable for any
            damages (including, without limitation, damages for loss of data or
            profit, or due to business interruption) arising out of the use or
            inability to use our Services, even if we have been notified orally
            or in writing of the possibility of such damage.
          </p>
          </li>
          <li>
            <h3 class="text-secondary">CHANGES TO TERMS</h3>
            <p class="mb-3">
            We reserve the right to modify or replace these Terms at any time.
            We will provide notice of any material changes to the Terms, and
            your continued use of our Services after any such changes
            constitutes your acceptance of the new Terms.
          </p>
          </li>
          <li>
            <h3 class="text-secondary">GOVERNING LAW</h3>
            <p class="mb-3">
            These Terms shall be governed by and construed in accordance with
            the laws of the United Kingdom, without regard to its conflict of
            law provisions.
          </p>
          </li>
          <li>
            <h3 class="text-secondary">CONTACT US</h3>
            <p>
              If you have any questions or concerns about these Terms, please
              contact us at:
            <a class="text-secondary" href="mailto:terms@mypanda.ai">terms@mypanda.ai</a>
          </p>
          </li>
        </ol>
        <div class="aboutContainerLine"></div>
        <p class="text-center">
          By using our Services, you agree to be bound by these Terms of
          Service.
        </p>
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
  margin-top: 25px;
  margin-bottom: 25px;
  display: flex;
  background-color: #ffffff;
}
</style>
