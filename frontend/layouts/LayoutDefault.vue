<template>
  <div class="bg-base-100 mx-auto max-w-[100rem] drawer">
    <input id="drawer" type="checkbox" class="drawer-toggle" />
    <Content><slot /></Content>
    <Sidebar>
      <ul class="menu w-full rounded-box px-2">
        <li v-for="law in laws" :key="law.id">
          <Link :href="law.url">
            {{ law.name }}
          </Link>
        </li>
      </ul>
    </Sidebar>
  </div>
</template>

<script lang="ts" setup>
import Content from "../components/Content.vue";
import Sidebar from "../components/Sidebar.vue";
import Link from "../components/Link.vue";
import { useLawList } from "../composables/useLawList";

const { laws } = useLawList();
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
