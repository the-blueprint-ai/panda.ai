<script>
import axios from "axios";

export default {
  data() {
    return {
      formData: null,
    };
  },
  props: ["userId"],
  computed: {
    avatar() {
      return this.$store.state.userStore.avatar;
    },
    fileName() {
      return this.$store.state.imageUploadStore.fileName;
    },
    imageDrop() {
      return this.$store.state.chatStore.imageDrop;
    },
    saveButton() {
      return this.$store.state.chatStore.saveButton;
    },
    fileError() {
      return this.$store.state.chatStore.fileError;
    },
    preview() {
      return this.$store.state.chatStore.preview;
    },
    success() {
      return this.$store.state.imageUploadStore.success;
    },
    error() {
      return this.$store.state.imageUploadStore.error;
    },
    msg() {
      return this.$store.state.chatStore.msg;
    },
  },
  mounted() {},
  methods: {
    setAvatar(value) {
      this.$store.commit("setAvatar", value);
    },
    setFileName(value) {
      this.$store.commit("setFileName", value);
    },
    setImageDrop(value) {
      this.$store.commit("setImageDrop", value);
    },
    setSaveButton(value) {
      this.$store.commit("setSaveButton", value);
    },
    setFileError(value) {
      this.$store.commit("setFileError", value);
    },
    setPreview(value) {
      this.$store.commit("setPreview", value);
    },
    setSuccess(value) {
      this.$store.commit("setSuccess", value);
    },
    setError(value) {
      this.$store.commit("setError", value);
    },
    setMsg(value) {
      this.$store.commit("setMsg", value);
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
        const url = "http://localhost:3001/uploadimage/?userid=" + this.userId;
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
      id="imageInput"
      type="file"
      accept="image/png, image/jpg, image/jpeg, image/gif"
      @change="handleFileChange($event.target)"
      required
    />
    <p v-if="(preview == null) & (fileError == null)" for="imageInput">
      drop it, then give me 10!
    </p>
    <div v-if="this.preview">
      <img
        src="../assets/x-circle.svg"
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
.dropzone {
  height: fit-content;
  height: 150px;
  width: 98%;
  background: #000000;
  border-radius: 8px;
  border: 2px dashed #ffffff;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
}
input[type="file"] {
  position: absolute;
  opacity: 0;
  width: inherit;
  min-height: 200px;
  max-height: 400px;
  cursor: pointer;
}
.dropImage {
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}
.cancelButton {
  margin-top: -60px;
  margin-left: 90px;
  height: 25px;
  position: absolute;
  z-index: 100;
  cursor: pointer;
}
.saveButton {
  cursor: pointer;
  color: #000000;
  background-color: #ffcb4c;
  border: none;
  padding: 0.5rem;
  margin: 0.5rem;
  margin-right: 0px;
  transition: all 0.5s ease-in-out;
  border: 5px solid #ffcb4c;
  border-radius: 1rem;
  font-size: large;
  font-family: "Monaco";
  width: 100px;
  z-index: 100;
}
</style>
