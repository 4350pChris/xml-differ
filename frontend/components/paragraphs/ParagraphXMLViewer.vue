<script setup lang="ts">
import { computed } from "vue";
import { DOMParser } from "linkedom";
import ChangeIndicator, { type ChangeType } from "../ChangeIndicator.vue";

const props = defineProps<{ content: string }>();

const xmlDoc = computed(() => {
  const parser = new DOMParser();
  return parser.parseFromString(props.content, "text/xml");
});

const id = computed(() => {
  return xmlDoc.value.documentElement.getAttribute("doknr");
});

const change = computed<ChangeType>(() => {
  const deletions = xmlDoc.value.documentElement.querySelectorAll(".diff-del")?.length;
  const additions = xmlDoc.value.documentElement.querySelectorAll(".diff-insert")?.length;

  if (!deletions && !additions) return false;
  if (deletions && additions) return "mixed";
  return deletions ? "deletion" : "addition";
});
</script>

<template>
  <div :id="id" class="scroll-mt-16 indicator prose w-full" data-wrapper="true" :data-change="change">
    <ChangeIndicator :change="change" />
    <div class="w-full break-words" v-html="xmlDoc.documentElement.innerHTML"></div>
  </div>
</template>

<style scoped>
@reference "../../layouts/tailwind.css";

:deep(.S4) {
  margin-left: 0.5rem;
}

:deep(.S3) {
  margin-left: 1rem;
}

:deep(.S2) {
  margin-left: 1.5rem;
}

:deep(.S1) {
  margin-left: 2rem;
}

:deep(enbez) {
  margin-inline: 0.5rem;
}

:deep(.diff-insert) {
  text-decoration: none;
  @apply bg-success/30 border-success p-1 inline-block;
}

:deep(.diff-del) {
  text-decoration: none;
  @apply bg-error/30 border-error p-1 inline-block;
}
</style>
