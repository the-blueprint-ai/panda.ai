const integrationsStore = {
  namespaced: true,
  state: {
    integrationsList: [],
  },
  mutations: {
    setStoreIntegrationsList(state, value) {
      state.integrationsList = value;
    },
  },
  getters: {
    getStoreIntegrationsList(state) {
      return state.integrationsList;
    },
  },
  actions: {},
};

export default integrationsStore;
