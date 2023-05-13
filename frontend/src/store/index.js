import { createStore } from "vuex";
import chatStore from "./chatStore";
import imageUploadStore from "./imageUploadStore";
import typingStore from "./typingStore";
import userStore from "./userStore";
import roadmapStore from "./roadmapStore";
import faqsStore from "./faqsStore";
import userStatsStore from "./userStatsStore";
import integrationsStore from "./integrationsStore";

// Create a new store instance.
export default createStore({
  modules: {
    userStore: userStore,
    typingStore: typingStore,
    chatStore: chatStore,
    imageUploadStore: imageUploadStore,
    roadmapStore: roadmapStore,
    faqsStore: faqsStore,
    userStatsStore: userStatsStore,
    integrationsStore: integrationsStore,
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
