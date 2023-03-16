const chatStore = {
  state: {
    msg: "",
    inputIsVisible: false,
    daypart: "",
    chatHistory: [],
    isDisabled: false,
    imageDrop: null,
    saveButton: null,
    fileError: null,
    preview: null,
  },
  mutations: {
    setMsg(state, value) {
      state.msg = value;
    },
    setInputIsVisible(state, value) {
      state.inputIsVisible = value;
    },
    setDaypart(state, value) {
      state.daypart = value;
    },
    setChatHistory(state, value) {
      state.chatHistory.unshift(value);
    },
    emptyChatHistory(state) {
      state.chatHistory = [];
    },
    removeChatHistory(state, value) {
      state.chatHistory = state.chatHistory.slice(0, value);
    },
    setIsDisabled(state, value) {
      state.isDisabled = value;
    },
    setImageDrop(state, value) {
      state.imageDrop = value;
    },
    setSaveButton(state, value) {
      state.saveButton = value;
    },
    setFileError(state, value) {
      state.fileError = value;
    },
    setPreview(state, value) {
      state.preview = value;
    },
  },
  getters: {},
  actions: {},
};

export default chatStore;
