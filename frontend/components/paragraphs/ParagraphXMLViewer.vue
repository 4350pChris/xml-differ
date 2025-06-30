<script setup lang="ts">
import { ParagraphProjection } from "../../client";
import { useParseParagraphXML } from "../../composables/useParseParagraphXML";
import ParagraphNode from "./ParagraphNode.vue";

const props = defineProps<{ paragraph: ParagraphProjection }>();

const { parsed } = useParseParagraphXML(() => props.paragraph.content);
</script>

<template>
  <div>
    <h2 class="text-lg font-bold">{{ paragraph.title }}</h2>
    <ParagraphNode :node="parsed[0].norm[1].textdaten[0].text[0].Content" />
  </div>
</template>

<style>
dl {
  display: grid;
  grid-template-columns: minmax(0, auto) 1fr;
  grid-gap: 1rem;
}
dl > dt {
  font-weight: bold;
}
</style>
