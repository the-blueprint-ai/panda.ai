const imageUploadStore = {
  state: {
    fileName: "",
    formData: null,
    success: "",
    error: "",
  },
  mutations: {
    setFileName(state, value) {
      state.fileName = value;
    },
    setFormData(state, value) {
      state.formData = value;
    },
    appendFormData(state, name, value) {
      state.formData.append(name, value);
    },
    setSuccess(state, value) {
      state.success = value;
    },
    setError(state, value) {
      state.error = value;
    },
  },
  getters: {},
  actions: {},
};

export default imageUploadStore;
