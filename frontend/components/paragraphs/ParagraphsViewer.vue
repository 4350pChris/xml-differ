<script setup lang="ts">
import ParagraphXMLViewer from "./ParagraphXMLViewer.vue";
import { useTemplateRef } from "vue";
import MoveChangeButtons from "./MoveChangeButtons.vue";
import TableOfContents from "./TableOfContents.vue";

defineProps<{ diff: string[] }>();

const diffEl = useTemplateRef<HTMLElement>("diffParent");
</script>

<template>
  <TableOfContents class="not-prose fixed top-16 bottom-0 left-0 w-20 md:w-24 lg:w-28" :parent-element="diffEl" />
  <MoveChangeButtons class="fixed bottom-4 right-4" :parent-element="diffEl" />
  <div ref="diffParent">
    <ParagraphXMLViewer v-for="(content, i) in diff" :key="`${i}-${content.length}`" :content />
  </div>
</template>
