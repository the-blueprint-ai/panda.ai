const chatStore = {
  namespaced: true,
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
    setChatStoreChatHistory(state, value) {
      state.chatHistory.unshift(value);
    },
    setMultiChatHistory(state, values) {
      state.chatHistory.unshift(...values);
    },
    emptyChatHistory(state) {
      state.chatHistory = [];
    },
    removeChatHistory(state, value) {
      state.chatHistory = state.chatHistory.slice(value);
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
  getters: {
    getMsg(state) {
      return state.msg;
    },
    getInputIsVisible(state) {
      return state.inputIsVisible;
    },
    getDaypart(state) {
      return state.daypart;
    },
    getChatStoreChatHistory(state) {
      return state.chatHistory;
    },
    getIsDisabled(state) {
      return state.isDisabled;
    },
    getImageDrop(state) {
      return state.imageDrop;
    },
    getSaveButton(state) {
      return state.saveButton;
    },
    getFileError(state) {
      return state.fileError;
    },
    getPreview(state) {
      return state.preview;
    },
  },
  actions: {},
};

export default chatStore;
