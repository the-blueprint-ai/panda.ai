import * as Session from "supertokens-web-js/recipe/session";

const userStore = {
  namespaced: true,
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
    about: "",
    onboarded: false,
    subscriber: false,
    admin: false,
    subscribed: "",
    integrations: 0,
    messagesPerMonth: 0,
    subscriberId: "",
    userChatHistory: [],
    entities: [],
  },
  mutations: {
    setStoreSession(state, value) {
      state.session = value;
    },
    setStoreUserId(state, value) {
      state.userId = value;
    },
    setStoreEmail(state, value) {
      state.email = value;
    },
    setStoreFirstName(state, value) {
      state.first_name = value;
    },
    setStoreLastName(state, value) {
      state.last_name = value;
    },
    setStoreUsername(state, value) {
      state.username = value;
    },
    setStoreAvatar(state, value) {
      state.avatar = value;
    },
    setStoreBanner(state, value) {
      state.banner = value;
    },
    setStoreJoined(state, value) {
      state.joined = value;
    },
    setStoreAbout(state, value) {
      state.about = value;
    },
    setStoreOnboarded(state, value) {
      state.onboarded = value;
    },
    setStoreSubscriber(state, value) {
      state.subscriber = value;
    },
    setStoreAdmin(state, value) {
      state.admin = value;
    },
    setStoreSubscribed(state, value) {
      state.subscribed = value;
    },
    setStoreIntegrations(state, value) {
      state.integrations = value;
    },
    setStoreMessagesPerMonth(state, value) {
      state.messagesPerMonth = value;
    },
    setStoreSubscriberID(state, value) {
      state.subscriberId = value;
    },
    setStoreUserChatHistory(state, value) {
      state.userChatHistory.push(value);
    },
    refreshStoreUserChatHistory(state, value) {
      state.userChatHistory = [];
      state.userChatHistory.push(value);
    },
    setStoreEntities(state, value) {
      state.entities.push(value);
    },
  },
  getters: {
    getStoreSession(state) {
      return state.session;
    },
    getStoreUserId(state) {
      return state.userId;
    },
    getStoreEmail(state) {
      return state.email;
    },
    getStoreFirstName(state) {
      return state.first_name;
    },
    getStoreLastName(state) {
      return state.last_name;
    },
    getStoreUsername(state) {
      return state.username;
    },
    getStoreAvatar(state) {
      return state.avatar;
    },
    getStoreBanner(state) {
      return state.banner;
    },
    getStoreJoined(state) {
      return state.joined;
    },
    getStoreAbout(state) {
      return state.about;
    },
    getStoreOnboarded(state) {
      return state.onboarded;
    },
    getStoreSubscriber(state) {
      return state.subscriber;
    },
    getStoreAdmin(state) {
      return state.admin;
    },
    getStoreSubscribed(state) {
      return state.subscribed;
    },
    getStoreIntegrations(state) {
      return state.integrations;
    },
    getStoreMessagesPerMonth(state) {
      return state.messagesPerMonth;
    },
    getStoreSubscriberID(state) {
      return state.subscriberId;
    },
    getStoreUserChatHistory(state) {
      return state.userChatHistory;
    },
    getStoreEntities(state) {
      return state.entities;
    },
  },
  actions: {
    async getSession({ commit }) {
      commit("setStoreSession", await Session.doesSessionExist());
    },
    async getUserInfo({ dispatch, commit }) {
      await dispatch("getSession");
      commit("setStoreUserId", await Session.getUserId());
    },
  },
};

export default userStore;
