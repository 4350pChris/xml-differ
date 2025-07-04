<script setup lang="ts">
import { computed } from "vue";
import { DOMParser } from "linkedom";
import ChangeIndicator, { type ChangeType } from "../ChangeIndicator.vue";

const props = defineProps<{ content: string }>();

const xmlDoc = computed(() => {
  const parser = new DOMParser();
  return parser.parseFromString(props.content, "text/xml");
});

const metadataElement = computed(() => {
  return xmlDoc.value.documentElement.firstElementChild;
});

const id = computed(() => {
  return xmlDoc.value.documentElement.getAttribute("doknr") || "";
});

const title = computed(() => {
  const titleElements = metadataElement.value?.querySelectorAll("enbez, titel");
  if (!titleElements) return "Missing Title";
  return Array.from(titleElements)
    .map((el) => el.textContent?.trim())
    .filter(Boolean)
    .join(" ");
});

const paragraphElement = computed(() => {
  return metadataElement.value?.nextElementSibling;
});

const change = computed<ChangeType>(() => {
  const deletions = paragraphElement.value?.querySelectorAll(".diff-del")?.length;
  const additions = paragraphElement.value?.querySelectorAll(".diff-insert")?.length;

  if (!deletions && !additions) return false;
  if (deletions && additions) return "mixed";
  return deletions ? "deletion" : "addition";
});
</script>

<template>
  <h2 :id="id" class="scroll-mt-16 indicator max-w-full" :data-change="change">
    <ChangeIndicator :change="change" />
    <span>{{ title }}</span>
  </h2>
  <div v-html="paragraphElement?.innerHTML"></div>
</template>

<style scoped>
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
  background-color: #d4f8d4;
  border: 1px solid #b2e0b2;
  padding: 0.3rem;
}

:deep(.diff-del) {
  text-decoration: none;
  background-color: #f8d4d4;
  border: 1px solid #e0b2b2;
  padding: 0.3rem;
}
</style>
