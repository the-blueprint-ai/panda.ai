import * as Session from "supertokens-web-js/recipe/session";

const userStore = {
  state: {
    session: false,
    userId: "",
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    avatar: "../../src/assets/user.png",
    banner: "",
    joined: "",
    userChatHistory: [],
  },
  mutations: {
    setSession(state, value) {
      state.session = value;
    },
    setUserId(state, value) {
      state.userId = value;
    },
    setEmail(state, value) {
      state.email = value;
    },
    setFirstName(state, value) {
      state.first_name = value;
    },
    setLastName(state, value) {
      state.last_name = value;
    },
    setUsername(state, value) {
      state.username = value;
    },
    setAvatar(state, value) {
      state.avatar = value;
    },
    setBanner(state, value) {
      state.banner = value;
    },
    setJoined(state, value) {
      state.joined = value;
    },
    setUserChatHistory(state, value) {
      state.userChatHistory.push(value);
    },
  },
  getters: {},
  actions: {
    async getSession({ commit }) {
      commit('setSession', await Session.doesSessionExist());
    },
    async getUserInfo({ dispatch, commit }) {
      await dispatch('getSession');
      commit('setUserId', await Session.getUserId());
    },
  },
};

export default userStore;
