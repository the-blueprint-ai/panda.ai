<script>
import { mapGetters, mapMutations } from "vuex";
import axios from "axios";

export default {
  data() {
    return {
      formData: null,
      imageDropPhrase: "",
    };
  },
  props: ["userId", "chatName"],
  computed: {
    ...mapGetters("userStore", {
      avatar: "getStoreAvatar",
    }),
    ...mapGetters("chatStore", {
      imageDrop: "getImageDrop",
      saveButton: "getSaveButton",
      fileError: "getFileError",
      preview: "getPreview",
      msg: "getMsg",
    }),
    ...mapGetters("imageUploadStore", {
      fileName: "getFileName",
      success: "getSuccess",
      error: "getError",
    }),
  },
  mounted() {
    this.setImageDropPhrase(this.chatName);
  },
  methods: {
    ...mapMutations("userStore", {
      setAvatar: "setStoreAvatar",
    }),
    ...mapMutations("imageUploadStore", {
      setFileName: "setFileName",
    }),
    ...mapMutations("chatStore", {
      setImageDrop: "setImageDrop",
      setSaveButton: "setSaveButton",
      setFileError: "setFileError",
      setPreview: "setPreview",
      setMsg: "setMsg",
    }),
    ...mapMutations("imageUploadStore", {
      setSuccess: "setSuccess",
      setError: "setError",
    }),
    setImageDropPhrase(chatName) {
      if (chatName == "privatePanda") {
        this.imageDropPhrase = "drop it, then give me 10...";
      } else if (chatName == "piratePanda") {
        this.imageDropPhrase = "drop it, ye scallywag...";
      } else if (chatName == "streetPanda") {
        this.imageDropPhrase = "drop it like a thotty, drop it like a thotty...";
      } else if (chatName == "pandaWeather") {
        this.imageDropPhrase = "drop it, human...";
      }
    },
    getMessage: async function () {
      axios
        .get("/test")
        .then((res) => {
          this.setMsg(res.data);
          console.log(this.msg);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    handleFileChange: function (event) {
      this.file = event.files[0];
      this.setFileName(this.file.name);
      this.fileType = this.fileName.split(".").pop();
      if (
        this.fileType != "jpg" &&
        this.fileType != "jpeg" &&
        this.fileType != "png" &&
        this.fileType != "gif"
      ) {
        this.setFileError(
          "you tried to updload a " +
            this.fileType +
            " file, please only upload a .png, .jpg, .jpeg or .gif"
        );
        document.getElementById("badFile").innerHTML = this.fileError;
        setTimeout(() => this.clear(), 3);
        setTimeout(
          () => (
            this.setFileError(null),
            (document.getElementById("badFile").innerHTML = "")
          ),
          3600
        );
      }
      this.formData = new FormData();
      let reader = new FileReader();
      reader.readAsDataURL(this.file);
      reader.onload = (e) => {
        this.setPreview(e.target.result);
        this.formData.append("file", this.file);
        this.setAvatar(this.preview);
        this.setSaveButton("active");
      };
    },
    save: async function () {
      try {
        const url = import.meta.env.VITE_APP_API_URL + "/uploadimage?userid=" + this.userId;
        const res = await fetch(url, {
          method: "POST",
          body: this.formData,
        });

        // Check if the response status indicates an error
        if (!res.ok) {
          throw new Error(`Server responded with status ${res.status}`);
        }

        const response = await res.json();

        this.setAvatar(response.url);
        this.setFileName("");
        this.setPreview(null);
        this.formData = null;
        this.setSaveButton(null);
        this.setImageDrop(null);
        this.setSuccess(true);
        this.$emit("imageUploaded");
      } catch (error) {
        // Handle the error
        this.setError("An error occurred while saving the file:", error);
        setTimeout(() => this.setImageDropValue("active"), 9200);
        this.setSuccess("");
      }
    },
    clear: function () {
      this.setFileName("");
      this.setPreview(null);
      this.setAvatar("../../src/assets/user.png");
      this.formData = null;
      this.setSaveButton(null);
    },
  },
};
</script>

<template>
  <div
    class="dropzone"
    @dragover.prevent
    @dragenter.prevent
    @dragstart.prevent
    @drop.prevent="handleFileChange($event.dataTransfer)"
  >
    <input
      class="imageInput"
      id="imageInput"
      type="file"
      accept="image/png, image/jpg, image/jpeg, image/gif"
      @change="handleFileChange($event.target)"
      required
    />
    <p v-if="(preview == null) & (fileError == null)" for="imageInput" v-text="imageDropPhrase"></p>
    <div v-if="this.preview">
      <img
        src="../assets/icons/x-circle.svg"
        class="cancelButton"
        v-on:click="clear"
      />
    </div>
    <img class="dropImage" v-bind:src="preview" />
    <p id="badFile" for="imageInput" style="color: #ffcb4c; margin: 5px"></p>
    <button
      v-if="saveButton"
      class="saveButton"
      type="submit"
      v-on:click="save"
    >
      Save
    </button>
  </div>
</template>

<style>
@import "../assets/styles/panda-main.css";
</style>
