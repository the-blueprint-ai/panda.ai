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
    <div class="mainContainer container-fluid bg-primary text-white">
      <div class="container pt-5 pb-5">
        <h2 class="text-center">🐼 PANDA.AI PRIVACY POLICY</h2>
        <div class="aboutContainerLine"></div>
        <h3 class="text-secondary">EFFECTIVE DATE: 1ST APRIL 2023</h3>
        <p class="mb-3">
          At panda.ai, we are committed to protecting your privacy and ensuring
          that you have full control over your data. This Privacy Policy
          explains how we collect, use, disclose, and safeguard your information
          when you use our AI chatbot and associated services, in compliance
          with the EU General Data Protection Regulation (GDPR) and UK data
          privacy laws.
        </p>
        <p class="mb-3">
          Please read this policy carefully to understand our practices
          regarding your information. If you do not agree with the terms of this
          policy, please do not access or use our services.
        </p>
        <div class="aboutContainerLine"></div>
        <ol type="1">
          <li>
            <h3 class="text-secondary">INFORMATION WE COLLECT</h3>
            <p class="mb-3">
              We collect information that you provide to us directly and
              information that is generated as you use our services. This may
              include:
            </p>
            <ol type="a" class="mb-3">
              <li>
                Personal Information: When you interact with our AI chatbot, we
                collect and store the content of your messages and other
                information you provide.
              </li>
              <li>
                Usage Information: We gather data about your web browsing
                behaviour, social media activity, music preferences, and
                spending habits to personalise your AI chatbot experience.
              </li>
            </ol>
          </li>
          <li>
            <h3 class="text-secondary">HOW WE USE YOUR INFORMATION</h3>
            <p class="mb-3">We use your information to:</p>
            <ol type="a" class="mb-3">
              <li>
                Provide and improve our services: We use your information to
                deliver the personalised AI chatbot experience and make
                improvements to our services.
              </li>
              <li>
                Communicate with you: We may use your information to respond
                your inquiries and provide customer support.
              </li>
            </ol>
          </li>
          <li>
            <h3 class="text-secondary">
              LAWFUL BASIS FOR PROCESSING PERSONAL DATA
            </h3>
            <p class="mb-3">
              Under the GDPR, our lawful basis for processing your personal data
              is your explicit consent. By using our services, you give us
              permission to collect, use, and share your information as
              described in this Privacy Policy.
            </p>
          </li>
          <li>
            <h3 class="text-secondary">DATA RETENTION PERIOD</h3>
            <p class="mb-3">
              We will retain your personal data until you decide to delete your
              data and/or delete your account. Upon deletion, we will remove
              your information from our systems.
            </p>
          </li>
          <li>
            <h3 class="text-secondary">YOUR DATA RIGHTS</h3>
            <p class="mb-3">
              As a data subject, you have the following rights under the GDPR
              and UK data privacy laws:
            </p>
            <ol type="a" class="mb-3">
              <li>
                Access: You have the right to access your data at any time.
              </li>
              <li>
                You have the right to correct any inaccuracies in your data.
              </li>
              <li>
                Erasure: You have the right to request the deletion of your
                data.
              </li>
              <li>
                Restriction: You have the right to restrict the processing of
                your data in certain circumstances
              </li>
              <li>
                Object: You have the right to object to the processing of your
                data.
              </li>
              <li>
                Data Portability: You have the right to receive your personal
                data in a structured, commonly used, and machine-readable
                format.
              </li>
              <li>
                Lodge a complaint: You have the right to lodge a complaint with
                a supervisory authority if you believe that your data protection
                rights have been violated.
              </li>
            </ol>
          </li>
          <li>
            <h3 class="text-secondary">DATA STORAGE AND TRANSFERS</h3>
            <p class="mb-3">
              All data is currently held within the UK. If this changes in the
              future, we will inform our users and update our Privacy Policy
              accordingly.
            </p>
          </li>
          <li>
            <h3 class="text-secondary">CHANGES TO OUR PRIVACY POLICY</h3>
            <p class="mb-3">
              We may update this Privacy Policy from time to time. When we make
              changes, we will update the "Effective Date" at the top of this
              policy and notify you of any material changes. We encourage you to
              periodically review this policy to stay informed about how we are
              protecting your information.
            </p>
          </li>
          <li>
            <h3 class="text-secondary">CONTACT US</h3>
            <p>
              If you have any questions or concerns about this Privacy Policy,
              Policy, please contact us at:
              <a class="text-secondary" href="mailto:privacy@mypanda.ai"
                >privacy@mypanda.ai</a
              >
            </p>
          </li>
        </ol>
        <div class="aboutContainerLine"></div>
        <p>
          By using our services, you consent to the terms of this Privacy Policy
          and our collection, use, and sharing of your information as described
          herein.
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
