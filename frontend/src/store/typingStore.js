const typingStore = {
  state: {
    typeValue: "",
    typeStatus: false,
    displayTextArray: ["Welcome to panda.ai"],
    typingSpeed: 100,
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
  getters: {},
  actions: {},
};

export default typingStore;
