<script setup lang="ts">
import { useParagraphs } from "../../composables/useParagraphs";
import ParagraphXMLViewer from "./ParagraphXMLViewer.vue";

const props = defineProps<{ versionId: string }>();
const { data: paragraphs } = useParagraphs(() => props.versionId);
</script>

<template>
  <template v-if="paragraphs">
    <ParagraphXMLViewer v-for="paragraph in paragraphs" :key="paragraph.id" :paragraph />
  </template>
  <p v-else>Loading...</p>
</template>
