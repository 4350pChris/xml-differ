<template>
  <div class="bg-base-100 mx-auto max-w-[100rem] drawer min-h-svw">
    <input id="drawer" type="checkbox" class="drawer-toggle" />
    <Content><slot /></Content>
    <Sidebar />
  </div>
</template>

<script lang="ts" setup>
import Content from "../components/Content.vue";
import Sidebar from "../components/Sidebar.vue";
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
