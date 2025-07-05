<template>
  <div class="bg-base-100 min-h-svh max-w-svw">
    <Content><slot /></Content>
  </div>
</template>

<script lang="ts" setup>
import Content from "../components/Content.vue";
</script>

<style>
/* see https://stackoverflow.com/questions/55206901/how-to-import-css-files-in-vue-3-child-components */
@import "./tailwind.css";

body {
  margin: 0;
  font-family: sans-serif;
}
* {
  box-sizing: border-box;
}
</style>
