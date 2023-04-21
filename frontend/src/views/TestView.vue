<script>
import { defineComponent } from "vue";
import navBar from "../components/navBar.vue";
import navFooter from "../components/navFooter.vue";
import SpinnerComponent from "../components/spinnerComponent.vue";
import { sendEmail } from "@/composables/sendEmail";

export default defineComponent({
  data() {
    return {
      sentences: [
        "This is the first sentence.",
        "Here is the second one.",
        "And this is the last sentence.",
        "Or is it?",
        "How many sentences can I do?!",
        "One more?!",
      ],
      currentIndex: 0,
      currentLetter: 0,
      typingSpeed: 50,
      pauseDuration: 1000,
      initiallength: 6,
      lastTypedIndex: -1,
      loading: true,
      buttonText: "SEND",
      isMobile: false,
      from_email: "contact@mypanda.ai",
      to_emails: "seanbetts@icloud.com",
      subject: "TEST",
    };
  },
  mounted() {
    this.typeSentence();
    this.isMobile = window.innerWidth <= 768;
    window.addEventListener('resize', () => {
      this.isMobile = window.innerWidth <= 768;
    });
  },
  methods: {
    sendEmail,
    generateWelcomeHTMLContent() {
      const user_name = "Sean";
      const htmlTemplate = `
      <html>
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Welcome Email</title>
        </head>
        <body style="display: flex; flex-direction: column; align-items: center; justify-content: flex-start; background-color: #EFEFEF; font-family: Monaco; font-size: 12px; line-height: 1.5; color: #FFFFFF; max-width: 600px; margin: 0 auto;">   
            <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="margin-top: 20px; background-color: #000000; border-radius: 10px; text-align: center;">
                <tr>
                  <td style="padding: 40px; font-size: 12px;">
                    <a href="https://www.mypanda.ai?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=logo"><img src="https://www.mypanda.ai/assets/panda.396faefe.png" class="biglogo" width="100" /></a>
                    <a href="https://www.mypanda.ai?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=title" style="text-decoration: none;"><h1 style="font-size: 24px; font-weight: bold; text-align: center; color: #FFFFFF; margin-bottom: 20px;">WELCOME TO PANDA.AI!</h1></a>
                    <p style="text-align: left;">Hi ${user_name},</p>
                    <p style="text-align: left;">We're thrilled to have you on board! Thank you for for taking 🐼 panda.ai out for a spin. We believe in the power of personalised AI experiences and giving users complete control over their own data.</p>
                    <p style="text-align: left;">Here are some helpful links to get you started:</p>
                    <ul style="list-style-type: none; padding-left: 10px;">
                      <li style="padding-bottom: 5px; text-align: left;"><a href="https://www.mypanda.ai/about?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=about" style="color: #FFCB4C; text-decoration: none;">ABOUT</a></li>
                      <li style="padding-bottom: 5px; text-align: left;"><a href="https://www.mypanda.ai/roadmap?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=roadmap" style="color: #FFCB4C; text-decoration: none;">ROADMAP</a></li>
                      <li style="padding-bottom: 5px; text-align: left;"><a href="https://www.mypanda.ai/privacy?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=privacy" style="color: #FFCB4C; text-decoration: none;">PRIVACY</a></li>
                      <li style="padding-bottom: 5px; text-align: left;"><a href="https://www.mypanda.ai/support?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=support" style="color: #FFCB4C; text-decoration: none;">SUPPORT</a></li>
                    </ul>
                    <p style="text-align: left;">If you have any questions, don't hesitate to reach out to our support team. We're here to help!</p>
                    <p style="text-align: left;">Love & hugs,</p>
                    <p style="text-align: left;"><strong>🐼</strong></p>
                  </td>
                </tr>
            </table>
          <div data-role="module-unsubscribe" class="module" role="module" data-type="unsubscribe" style="color:#444444; font-size:12px; line-height:20px; padding:16px 16px 16px 16px; text-align:Center;" data-muid="4e838cf3-9892-4a6d-94d6-170e474d21e5">
            
            <p style="font-size:12px; line-height:20px; color: #000000;">
              <a href="<%asm_group_unsubscribe_raw_url%>" target="_blank" class="Unsubscribe--unsubscribeLink" style="font-family: Monaco; color: #000000; text-decoration:none;">
                UNSUBSCRIBE
              </a>
              |
              <a href="<%asm_preferences_raw_url%>" target="_blank" class="Unsubscribe--unsubscribePreferences" style="font-family: Monaco; color: #000000; text-decoration:none;">
                UNSUBSCRIBE PREFERENCES
              </a>
            </p>
          </div>
        </body>
      </html>
      `;
      return htmlTemplate;
    },
    getCurrentText(index) {
      if (index < this.currentIndex) {
        return this.sentences[index];
      } else if (index === this.currentIndex) {
        return (
          this.sentences[index].substring(0, this.currentLetter) +
          '<span class="cursor"></span>'
        );
      } else if (
        index === this.sentences.length - 1 &&
        this.currentIndex === this.sentences.length
      ) {
        return this.sentences[index] + '<span class="cursor"></span>';
      }
      return "";
    },
    typeSentence() {
      if (this.currentIndex >= this.sentences.length) {
        this.lastTypedIndex = this.sentences.length - 1;
        return;
      }

      if (this.currentLetter < this.sentences[this.currentIndex].length) {
        this.currentLetter++;
        setTimeout(this.typeSentence, this.typingSpeed);
      } else {
        setTimeout(() => {
          this.currentIndex++;
          this.currentLetter = 0;
          this.typeSentence();
        }, this.pauseDuration);
      }
    },
    addSentences() {
      this.sentences.push("New sentence 1");
      this.sentences.push("New sentence 2");
      this.sentences.push("New sentence 3");
    },
  },
  watch: {
    sentences: {
      deep: true,
      handler(newValue, oldValue) {
        if (this.lastTypedIndex !== this.sentences.length - 1) {
          this.typeSentence();
        }
      },
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
    <div class="body">
      <h1>TESTING</h1>
      <div class="spacer"></div>
      <button @click="addSentences">Add sentences</button>
      <div id="app">
        <p v-for="(sentence, index) in sentences" :key="index">
          <span v-html="getCurrentText(index)"></span>
        </p>
      </div>
      <div class="spacer"></div>
      <div class="spacer"></div>
      <div>
        <h2 v-if="isMobile">IS DESKTOP</h2>
        <h2 v-else>IS MOBILE</h2>
      </div>
      <div class="spacer"></div>
      <div class="signUpForm">
        <iframe src="https://cdn.forms-content.sg-form.com/64ff0892-de22-11ed-946b-321cf8977179"/>
      </div>
      <div class="spacer"></div>
      <button class="letsChat" @click="sendEmail(this.from_email, this.to_emails, this.subject, generateWelcomeHTMLContent())">SEND EMAIL</button>
      <div class="spacer"></div>
      <div style="width: 500px;">
        <iframe style="border-radius: 12px" width="100%" height="352" title="Spotify Embed: This Is Radiohead" frameborder="0" allowfullscreen allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy" src="https://open.spotify.com/embed/playlist/37i9dQZF1DZ06evO2VxlyE?utm_source=oembed"></iframe>
      </div>
    </div>
    <navFooter></navFooter>
  </main>
</template>

<style>
/* @import "../assets/styles/panda-main.css"; */

.smallcursor {
  display: inline-block;
  width: 12px;
  height: 16px;
  margin-left: 5px;
  background-color: white;
}
</style>
