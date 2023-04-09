const userStatsStore = {
  namespaced: true,
  state: {
    toplineUsersStats: [],
    dailyUsersStats: [],
    toplineOnboardingStats: [],
    dailyOnboardingStats: [],
    toplineChatsStats: [],
    dailyChatsStats: [],
    toplineEntitiesStats: [],
    dailyEntitiesStats: [],
  },
  mutations: {
    setStoreToplineUsersStats(state, value) {
      state.toplineUsersStats.push(value);
    },
    setStoreDailyUsersStats(state, value) {
      state.dailyUsersStats.push(value);
    },
    setStoreToplineOnboardingStats(state, value) {
      state.toplineOnboardingStats.push(value);
    },
    setStoreDailyOnboardingStats(state, value) {
      state.dailyOnboardingStats.push(value);
    },
    setStoreToplineChatsStats(state, value) {
      state.toplineChatsStats.push(value);
    },
    setStoreDailyChatsStats(state, value) {
      state.dailyChatsStats.push(value);
    },
    setStoreToplineEntitiesStats(state, value) {
      state.toplineEntitiesStats.push(value);
    },
    setStoreDailyEntitiesStats(state, value) {
      state.dailyEntitiesStats.push(value);
    },
  },
  getters: {
    getStoreToplineUsersStats(state) {
      return state.toplineUsersStats;
    },
    getStoreDailyUsersStats(state) {
      return state.dailyUsersStats;
    },
    getStoreToplineOnboardingStats(state) {
      return state.toplineOnboardingStats;
    },
    getStoreDailyOnboardingStats(state) {
      return state.dailyOnboardingStats;
    },
    getStoreToplineChatsStats(state) {
      return state.toplineChatsStats;
    },
    getStoreDailyChatsStats(state) {
      return state.dailyChatsStats;
    },
    getStoreToplineEntitiesStats(state) {
      return state.toplineEntitiesStats;
    },
    getStoreDailyEntitiesStats(state) {
      return state.dailyEntitiesStats;
    },
  },
  actions: {},
};

export default userStatsStore;
