<script lang="ts">
export default {
  props: {
    message: Object,
  },
};
</script>

<template>
  <div>
    <img :src="'/src/assets/' + message.user + '.png'" class="chatImage"/>
    <p className="message">{{ message.message }}</p>
  </div>
</template>
