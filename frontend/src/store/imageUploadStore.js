const imageUploadStore = {
  state: {
    fileName: "",
    preset: "", //process.env.VUE_APP_UPLOAD_PRESET,
    formData: null,
    cloudName: "", //process.env.VUE_APP_CLOUD_NAME,
    success: "",
  },
  mutations: {
    setFileName(state, value) {
      state.fileName = value;
    },
    setPreset(state, value) {
      state.preset = value;
    },
    setFormData(state, value) {
      state.formData = value;
    },
    setCloudName(state, value) {
      state.cloudName = value;
    },
    setSuccess(state, value) {
      state.success = value;
    },
  },
  getters: {},
  actions: {},
};

export default imageUploadStore;
