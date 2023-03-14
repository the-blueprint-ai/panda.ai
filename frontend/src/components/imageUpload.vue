<script>
import axios from "axios";

export default {
  data() {
    return {
      fileName: "",
      imageDrop: null,
      saveButton: null,
      fileError: null,
      preview: null,
      preset: "", //process.env.VUE_APP_UPLOAD_PRESET,
      formData: null,
      cloudName: "", //process.env.VUE_APP_CLOUD_NAME,
      success: "",
      msg: "",
    };
  },
  mounted() {},
  methods: {
    getMessage: async function () {
      axios
        .get("/test")
        .then((res) => {
          this.msg = res.data;
          console.log(this.msg);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    handleFileChange: function (event) {
      this.file = event.files[0];
      this.fileName = this.file.name;
      this.fileType = this.fileName.split(".").pop();
      if (
        this.fileType != "jpg" &&
        this.fileType != "jpeg" &&
        this.fileType != "png" &&
        this.fileType != "gif"
      ) {
        this.fileError =
          "you tried to updload a " +
          this.fileType +
          " file, please only upload a .png, .jpg, .jpeg or .gif";
        document.getElementById("badFile").innerHTML = this.fileError;
        setTimeout(() => this.clear(), 3);
        setTimeout(
          () => (
            (this.fileError = null),
            (document.getElementById("badFile").innerHTML = "")
          ),
          3600
        );
      }
      this.formData = new FormData();
      this.formData.append("upload_preset", this.preset);
      let reader = new FileReader();
      reader.readAsDataURL(this.file);
      reader.onload = (e) => {
        this.preview = e.target.result;
        this.formData.append("file", this.preview);
        this.saveButton = "active";
      };
    },
    upload: async function () {
      const res = await fetch(
        `https://api.cloudinary.com/v1_1/${this.cloudName}/image/upload`,
        {
          method: "POST",
          body: this.formData,
        }
      );
      const data = await res.json();
      this.fileName = "";
      this.preview = null;
      this.formData = null;
      this.success = data.public_id;
    },
    clear: function () {
      this.fileName = "";
      this.preview = null;
      this.formData = null;
      this.saveButton = null;
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
      accept="image/*"
      @change="handleFileChange($event.target)"
      required
    />
    <p
      v-if="(this.preview == null) & (this.fileError == null)"
      for="imageInput"
    >
      drop it like a thotty
    </p>
    <div v-if="this.preview">
      <img
        src="../assets/x-circle.svg"
        className="cancelButton"
        v-on:click="clear"
      />
    </div>
    <img className="dropImage" v-bind:src="preview" />
    <p id="badFile" for="imageInput" style="color: #ffcb4c; margin: 5px;"></p>
    <button
      v-if="saveButton"
      className="chatButton"
      type="submit"
      v-on:click="upload"
    >
      Save
    </button>
  </div>
  <h3 v-if="success">File Uploaded Successfully. publicId: {{ success }}</h3>
</template>

<style>
.dropzone {
  height: fit-content;
  height: 150px;
  width: 98%;
  background: #000000;
  border-radius: 8px;
  border: 2px dashed #FFFFFF;
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
</style>
