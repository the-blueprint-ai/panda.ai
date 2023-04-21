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
  <main>
    <navBar></navBar>
    <div class="body">
      <div class="privacyPolicyContainer">
        <h2>🐼 panda.ai Terms of Service</h2>
        <div class="aboutContainerLine"></div>
        <h3>Effective Date: 1st April 2023</h3>
        <p>
          Please read these Terms of Service ("Terms") carefully before using
          the panda.ai chatbot and associated services (the "Services") provided
          by panda.ai ("us", "we", or "our"). By accessing or using our
          Services, you agree to be bound by these Terms. If you do not agree
          with any part of these Terms, you must not use our Services.
        </p>
        <div class="aboutContainerLine"></div>
        <ol type="1">
          <li>
            <h3>Eligibility</h3>
            By using our Services, you represent and warrant that you are at
            least 18 years old and have the legal capacity to enter into these
            Terms. If you are under 18, you must have consent from a parent or
            legal guardian to use our Services.
          </li>
          <li>
            <h3>Account Registration</h3>
            To use our Services, you may need to register for an account. You
            agree to provide accurate, complete, and up-to-date information when
            registering for an account. You are responsible for maintaining the
            confidentiality of your account credentials and for all activities
            that occur under your account.
          </li>
          <li>
            <h3>Acceptable Use</h3>
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
          </li>
          <li>
            <h3>Intellectual Property Rights</h3>
            All content, features, and functionality of our Services, including
            but not limited to text, graphics, logos, and software, are the
            property of panda.ai or its licensors and are protected by
            copyright, trademark, and other intellectual property laws.
            Unauthorised use of our content or any part of our Services may
            result in legal action.
          </li>
          <li>
            <h3>Termination</h3>
            We reserve the right to terminate or suspend your access to our
            Services, with or without notice, if we believe you have breached
            any provision of these Terms or if your use of our Services is
            harmful to our interests or the interests of other users.
          </li>
          <li>
            <h3>Disclaimer of Warranties</h3>
            Our Services are provided on an "as is" and "as available" basis. We
            make no warranties, expressed or implied, and hereby disclaim and
            negate all other warranties, including without limitation, implied
            warranties or conditions of merchantability, fitness for a
            particular purpose, or non-infringement of intellectual property or
            other violation of rights.
          </li>
          <li>
            <h3>Limitation of Liability</h3>
            In no event shall panda.ai or its suppliers be liable for any
            damages (including, without limitation, damages for loss of data or
            profit, or due to business interruption) arising out of the use or
            inability to use our Services, even if we have been notified orally
            or in writing of the possibility of such damage.
          </li>
          <li>
            <h3>Changes to Terms</h3>
            We reserve the right to modify or replace these Terms at any time.
            We will provide notice of any material changes to the Terms, and
            your continued use of our Services after any such changes
            constitutes your acceptance of the new Terms.
          </li>
          <li>
            <h3>Governing Law</h3>
            These Terms shall be governed by and construed in accordance with
            the laws of the United Kingdom, without regard to its conflict of
            law provisions.
          </li>
          <li>
            <h3>Contact Us</h3>
            <p>
              If you have any questions or concerns about these Terms, please
              contact us at:
            </p>
            <a href="mailto:terms@mypanda.ai">terms@mypanda.ai</a>
          </li>
        </ol>
        <div class="aboutContainerLine"></div>
        <p>
          By using our Services, you agree to be bound by these Terms of
          Service.
        </p>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>
