<script>
export default {
  data() {
    return {};
  },
  watch: {},
  props: {
    dataMenu: Boolean,
  },
  created() {},
  components: {},
};
</script>

<template>
  <div className="userData" v-if="dataMenu">
    <h1>USER DATA</h1>
  </div>
</template>
