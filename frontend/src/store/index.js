import { createStore } from "vuex";
import chatStore from "./chatStore";
import imageUploadStore from "./imageUploadStore";
import typingStore from "./typingStore";
import userStore from "./userStore";

// Create a new store instance.
export default createStore({
  modules: {
    userStore: userStore,
    typingStore: typingStore,
    chatStore: chatStore,
    imageUploadStore: imageUploadStore,
  },
  state() {
    return {
      isOpen: false,
    };
  },
  mutations: {
    setIsOpen(state, value) {
      state.isOpen = value;
    },
  },
});
