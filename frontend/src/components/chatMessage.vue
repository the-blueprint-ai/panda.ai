<script>
import SpinnerComponent from "../components/spinnerComponent.vue";
import { useToast } from "vue-toastification";
import { submitRating } from "../composables/submitRating.js";
import { submitFeedback } from "../composables/submitFeedback.js";

export default {
  data() {
    return {
      isDisabled: true,
      pandaImage: "",
      userImage: "",
      thinkingImage: "",
      loading: false,
      buttonText: "SUBMIT FEEDBACK",
      upFeedback: "",
      downFeedback: "",
    };
  },
  props: {
    message: Object,
    searchTerm: String,
    feedbackDisabled: Boolean,
    userId: String,
  },
  async created() {
    const pandaImageModule = await import("../assets/panda.png");
    this.pandaImage = pandaImageModule.default;
    const userImageModule = await import("../assets/user.png");
    this.userImage = userImageModule.default;
    const thinkingImageModule = await import("../assets/thinking.png");
    this.thinkingImage = thinkingImageModule.default;
  },
  computed: {
    avatar() {
      return this.$store.state.userStore.avatar;
    },
    containsSearchTerm() {
      if (this.searchTerm) {
        if (this.searchTerm.trim() === "") return false;
        return this.message.message
          .toLowerCase()
          .includes(this.searchTerm.trim().toLowerCase());
      }
      return null;
    },
    messageClass() {
      return this.containsSearchTerm ? "highlighted" : "";
    },
  },
  methods: {
    formatMessage(message) {
      const urlPattern = /(https?:\/\/[^\s/$.?#].[^\s]*)/gi;

      // Create a temporary DOM element to parse and manipulate the message HTML
      const tempDiv = document.createElement("div");
      tempDiv.innerHTML = message;

      // Iterate through all text nodes within the temporary DOM element
      function traverseTextNodes(node) {
        if (node.nodeType === Node.TEXT_NODE) {
          // Replace URLs with clickable links in the text node's content
          node.textContent = node.textContent.replace(urlPattern, (match) => {
            return `<a href="${match}" target="_blank">${match}</a>`;
          });
        } else {
          // Continue traversing child nodes
          for (const child of node.childNodes) {
            traverseTextNodes(child);
          }
        }
      }

      traverseTextNodes(tempDiv);

      // Return the modified HTML
      return tempDiv.innerHTML;
    },
    messageImage() {
      if (this.message.message == "Thinking...") {
        return this.thinkingImage;
      } else if (this.message.user == "panda") {
        return this.pandaImage;
      } else if (!this.avatar) {
        return this.userImage;
      } else if (this.avatar) {
        return this.avatar;
      }
    },
    async submitRating(user_id, message, rating) {
      this.loading = true;
      try {
        await submitRating(user_id, message, rating);
        console.log("Rating submitted successfully");
      } catch (error) {
        console.error("Error submitting rating");
      } finally {
        this.loading = false;
      }
    },
    async submitFeedback(user_id, message, rating, feedback) {
      // Check if message length is 0
      if (message.length === 0) {
        return; // Stop the function
      }

      this.loading = true;
      try {
        await submitFeedback(user_id, message, rating, feedback);
        useToast().success("Feedback submitted successfully");
      } catch (error) {
        useToast().error("Error submitting feedback");
      } finally {
        this.loading = false;
      }
    },
  },
  components: {
    SpinnerComponent,
  },
};
</script>

<template>
  <div :class="['chatMessage', message.user, messageClass]">
    <img v-bind:src="messageImage()" class="chatAvatar" />
    <div class="w-100 d-flex flex-row justify-content-between">
      <p class="message" v-html="formatMessage(message.message)"></p>
      <span
        class="thumbs d-flex"
        v-if="message.user == 'panda' && !feedbackDisabled"
      >
        <div
          class="d-flex"
          data-bs-toggle="modal"
          data-bs-target="#thumbsUpModal"
          @click="submitRating(userId, message.message, 'up')"
        >
          <img class="thumbUp" src="../assets/icons/hand-thumbs-up.svg" />
        </div>
        <div
          class="d-flex"
          data-bs-toggle="modal"
          data-bs-target="#thumbsDownModal"
          @click="submitRating(userId, message.message, 'down')"
        >
          <img
            class="thumbDown ms-2"
            src="../assets/icons/hand-thumbs-down.svg"
          />
        </div>
      </span>
    </div>
    <div
      class="modal fade"
      id="thumbsUpModal"
      tabindex="-1"
      aria-labelledby="thumbsUpModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <div class="d-flex mt-2 mb-n2">
              <img
                class="thumbUpAdditional me-3"
                src="../assets/icons/hand-thumbs-up.svg"
              />
              <p class="mt-1">Please provide additional feedback</p>
            </div>
            <button
              type="button"
              class="btn-close me-1"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body text-center">
            <div class="form-floating mt-n3 mb-2">
              <textarea
                type="text"
                class="form-control mt-4"
                id="floatingTextarea"
                v-model="upFeedback"
              ></textarea>
              <label for="floatingTextarea"
                >What would you like to add to the feedback?</label
              >
            </div>
          </div>
          <div class="modal-footer">
            <button
              @click="
                submitFeedback(userId, message.message, 'up', this.upFeedback)
              "
              type="button"
              class="btn btn-secondary d-flex justify-content-center"
              data-bs-dismiss="modal"
              aria-label="Close"
              style="width: 150px"
            >
              <SpinnerComponent
                :loading="this.loading"
                :button-text="this.buttonText"
              ></SpinnerComponent>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div
      class="modal fade"
      id="thumbsDownModal"
      tabindex="-1"
      aria-labelledby="thumbsDownModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <div class="d-flex mt-2 mb-n2">
              <img
                class="thumbDownAdditional me-3"
                src="../assets/icons/hand-thumbs-down.svg"
              />
              <p class="mt-1">Please provide additional feedback</p>
            </div>
            <button
              type="button"
              class="btn-close me-1"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body text-center">
            <div class="form-floating mt-n3 mb-2">
              <textarea
                type="text"
                class="form-control mt-4"
                id="floatingTextarea"
                v-model="downFeedback"
              ></textarea>
              <label for="floatingTextarea"
                >What would you like to add to the feedback?</label
              >
            </div>
          </div>
          <div class="modal-footer">
            <button
              @click="
                submitFeedback(
                  userId,
                  message.message,
                  'down',
                  this.downFeedback
                )
              "
              type="button"
              class="btn btn-secondary d-flex justify-content-center"
              data-bs-dismiss="modal"
              aria-label="Close"
              style="width: 150px"
            >
              <SpinnerComponent
                :loading="this.loading"
                :button-text="this.buttonText"
              ></SpinnerComponent>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.userChat {
  background-color: #ffffff;
  text-align: left;
  display: flex;
  max-width: 785px;
  padding-left: 60px;
  flex-direction: row-reverse;
  justify-content: right;
  align-items: right;
}
.userChat p {
  width: 100%;
  text-align: end;
}
.userChat.highlighted {
  position: relative;
  width: 99%;
  margin-top: 5px;
  margin-bottom: 5px;
  background-color: #ffcb4c;
  border-radius: 15px;
  flex-direction: row-reverse;
  justify-content: right;
  align-items: right;
  border: none;
}
.pandaChat {
  background-color: #ffffff;
  text-align: left;
  display: flex;
  max-width: 785px;
  padding-right: 60px;
  flex-direction: row;
  justify-content: left;
  align-items: left;
}
.pandaChat.highlighted {
  position: relative;
  width: 99%;
  margin-top: 5px;
  margin-bottom: 5px;
  background-color: #ffcb4c;
  border-radius: 15px;
  border: none;
}
.chatMessage {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #efefef;
}
.message {
  display: flex;
  flex-direction: column;
  align-items: left;
  margin: 10px;
  padding-top: 10px;
  padding-left: 15px;
  padding-right: 15px;
  padding-bottom: 15px;
  width: fit-content;
  word-wrap: break-word;
  border-radius: 15px;
  color: #000000;
}
.message ol li {
  margin-bottom: 10px;
}
.message a {
  color: #000000;
  text-decoration: none;
  text-align: center;
}
.message a:hover {
  color: #ffcb4c;
  text-decoration: none;
}
.chatAvatar {
  width: 50px;
  height: 50px;
  margin: 5px;
  margin-bottom: 12px;
  border-radius: 10px;
}
.thumbs {
  margin-right: -63px;
  opacity: 0.2;
}
.thumbUp,
.thumbDown {
  margin: auto;
  padding: 5px;
  height: 30px;
  border-radius: 5px;
}
.thumbUp:hover,
.thumbDown:hover {
  cursor: pointer;
  background-color: #efefef;
}
.thumbUpAdditional,
.thumbDownAdditional {
  height: 30px;
  padding: 5px;
  border-radius: 5px;
}
.thumbUpAdditional {
  background-color: lightgreen;
}
.thumbDownAdditional {
  background-color: red;
}
@media (max-width: 576px) {
  .chatAvatar {
    display: none;
  }
  .message {
    width: 300px;
    padding: 3px;
    margin: 3px;
  }
  .pandaChat {
    width: 300px;
  }
  .userChat {
    width: 300px;
  }
}
</style>
