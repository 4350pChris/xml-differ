<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ content: string }>();

const html = computed(() => {
  const parser = new DOMParser();
  const xmlDoc = parser.parseFromString(props.content, "application/xml");
  return xmlDoc.documentElement.innerHTML;
});
</script>

<template>
  <div class="[&_metadaten]:font-bold" v-html="html"></div>
</template>

<style scoped>
:deep(dl) {
  display: grid;
  grid-template-columns: minmax(0, auto) 1fr;
  grid-gap: 1rem;
}

:deep(dl > dt) {
  font-weight: bold;
}

:deep(enbez) {
  margin-inline: 0.5rem;
}

:deep([style="DiffInsert"], .diff-insert) {
  text-decoration: none;
  background-color: #d4f8d4;
  border: 1px solid #b2e0b2;
  padding: 0.3rem;
}

:deep([style="DiffDelete"], .diff-delete) {
  text-decoration: none;
  background-color: #f8d4d4;
  border: 1px solid #e0b2b2;
  padding: 0.3rem;
}
</style>
