const userStore = {
  state: {
    session: false,
    userId: "",
    email: "",
    first_name: "",
    last_name: "",
    username: "",
    avatar: "../../src/assets/user.png",
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
  },
  getters: {},
  actions: {},
};

export default userStore;
