<template>
  <div class="bg-base-100 min-h-svh max-w-svw">
    <Content><slot /></Content>
  </div>
</template>

<script lang="ts" setup>
import "unfonts.css";
import Content from "../components/Content.vue";
import { client } from "../client/client.gen";
import { usePageContext } from "vike-vue/usePageContext";

const pageContext = usePageContext();
const { apiUrl } = pageContext;
client.setConfig({
  baseUrl: import.meta.env.SSR ? apiUrl.ssr : apiUrl.client,
});
</script>

<style>
/* see https://stackoverflow.com/questions/55206901/how-to-import-css-files-in-vue-3-child-components */
@import "./tailwind.css";

@theme {
  --font-sans: "Inter Variable", sans-serif;
}
</style>
