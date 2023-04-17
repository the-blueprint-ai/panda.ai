const typingStore = {
  namespaced: true,
  state: {
    typeValue: "",
    typeStatus: false,
    displayTextArray: ["Welcome to panda.ai"],
    typingSpeed: 150,
    newTextDelay: 1500,
    displayTextArrayIndex: 0,
    charIndex: 0,
  },
  mutations: {
    setTypeValue(state, value) {
      state.typeValue = value;
    },
    setTypeStatus(state, value) {
      state.typeStatus = value;
    },
    setDisplayTextArray(state, value) {
      state.displayTextArray = [];
      state.displayTextArray.push(value);
    },
    setTypingSpeed(state, value) {
      state.typingSpeed = value;
    },
    setNewTextDelay(state, value) {
      state.newTextDelay = value;
    },
    setDisplayTextArrayIndex(state, value) {
      state.displayTextArrayIndex = value;
    },
    setCharIndex(state, value) {
      state.charIndex = value;
    },
  },
  getters: {
    getTypeValue(state) {
      return state.typeValue;
    },
    getTypeStatus(state) {
      return state.typeStatus;
    },
    getDisplayTextArray(state) {
      return state.displayTextArray;
    },
    getTypingSpeed(state) {
      return state.typingSpeed;
    },
    getNewTextDelay(state) {
      return state.newTextDelay;
    },
    getDisplayTextArrayIndex(state) {
      return state.displayTextArrayIndex;
    },
    getCharIndex(state) {
      return state.charIndex;
    },
  },
  actions: {},
};

export default typingStore;
