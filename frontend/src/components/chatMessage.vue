<script lang="ts">
export default {
  props: {
    message: Object,
  },
};
</script>

<template>
  <div>
    <img :src="'/src/assets/' + message.user + '.png'" class="avatar"/>
    <p className="message">{{ message.message }}</p>
  </div>
</template>
