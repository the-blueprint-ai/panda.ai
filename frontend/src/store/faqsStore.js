const faqsStore = {
  namespaced: true,
  state: {
    sortedFAQs: [],
    unsortedFAQs: [],
  },
  mutations: {
    setStoreSortedFAQs(state, value) {
      state.sortedFAQs = value;
    },
    setStoreUnsortedFAQs(state, value) {
      state.unsortedFAQs = value;
    },
  },
  getters: {
    getStoreSortedFAQs(state) {
      return state.sortedFAQs;
    },
    getStoreUnsortedFAQs(state) {
      return state.unsortedFAQs;
    },
  },
  actions: {},
};

export default faqsStore;
