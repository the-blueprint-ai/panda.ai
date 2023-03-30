import * as Session from "supertokens-web-js/recipe/session";

const state = {
  session: false,
  userId: "",
  first_name: "",
  last_name: "",
  username: "",
  email: "",
  avatar: "../../src/assets/user.png",
  banner: "",
  joined: "",
  about: "",
  onboarded: false,
  subscriber: false,
  admin: false,
  userChatHistory: [],
};

const mutations = {
  setSession(state, value) {
    state.session = value;
  },
  setUserId(state, value) {
    state.userId = value;
  },
  setEmail(state, value) {
    state.email = value;
    console.log('Email set in store:', state.email);
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
  setAbout(state, value) {
    state.about = value;
  },
  setOnboarded(state, value) {
    state.onboarded = value;
  },
  setSubscriber(state, value) {
    state.subscriber = value;
  },
  setAdmin(state, value) {
    state.admin = value;
  },
  setUserChatHistory(state, value) {
    state.userChatHistory.push(value);
  },
};
const getters = {
  getSession(state) {
    return state.session;
  },
  getUserId(state) {
    return state.userId;
  },
  getEmail(state) {
    return state.email;
  },
  getFirstName(state) {
    return state.first_name;
  },
  getLastName(state) {
    return state.last_name;
  },
  getUsername(state) {
    return state.username;
  },
  getAvatar(state) {
    return state.avatar;
  },
  getBanner(state) {
    return state.banner;
  },
  getJoined(state) {
    return state.joined;
  },
  getAbout(state) {
    return state.about;
  },
  getOnboarded(state) {
    return state.onboarded;
  },
  getSubscriber(state) {
    return state.subscriber;
  },
  getAdmin(state) {
    return state.admin;
  },
  getChatUserHistory(state) {
    return state.userChatHistory;
  },
};
const actions = {
  async getSession({ commit }) {
    commit("setSession", await Session.doesSessionExist());
  },
  async getUserInfo({ dispatch, commit }) {
    await dispatch("userStore/getSession", null, { root: true });
    commit("setUserId", await Session.getUserId());
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions,
};
