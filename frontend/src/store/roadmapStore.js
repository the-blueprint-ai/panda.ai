const roadmapStore = {
  namespaced: true,
  state: {
    roadmapData: null,
    roadmapId: 0,
    roadmapName: "",
    roadmapDescription: "",
    roadmapTags: [],
    roadmapVotes: 0,
  },
  mutations: {
    setRoadmapData(state, value) {
      state.roadmapData = value;
    },
    setRoadmapId(state, value) {
      state.roadmapId = value;
    },
    setRoadmapName(state, value) {
      state.roadmapName = value;
    },
    setRoadmapDescription(state, value) {
      state.roadmapDescription = value;
    },
    setRoadmapTags(state, value) {
      state.roadmapTags.push(...value);
    },
    setRoadmapVotes(state, value) {
      state.roadmapVotes = value;
    },
  },
  getters: {
    getRoadmapData(state) {
      return state.roadmapData;
    },
    getRoadmapId(state) {
      return state.roadmapId;
    },
    getRoadmapName(state) {
      return state.roadmapName;
    },
    getRoadmapDescription(state) {
      return state.roadmapDescription;
    },
    getRoadmapTags(state) {
      return state.roadmapTags;
    },
    getRoadmapVotes(state) {
      return state.roadmapVotes;
    },
  },
  actions: {},
};

export default roadmapStore;
