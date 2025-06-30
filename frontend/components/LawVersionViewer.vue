<script setup lang="ts">
import { LawDetailProjection } from "../client";
import LawVersionSelector from "./LawVersionSelector.vue";
import { ref } from "vue";
import ParagraphsViewer from "./paragraphs/ParagraphsViewer.vue";

defineProps<{ law: LawDetailProjection }>();

const left = ref<string>();
const right = ref<string>();
</script>

<template>
  <div>
    <div class="flex items-center justify-center pb-2 gap-4">
      <LawVersionSelector v-model="left" legend="Linke Version" :versions="law.versions" />
      <LawVersionSelector v-model="right" legend="Rechte Version" :versions="law.versions" />
    </div>
    <ParagraphsViewer v-if="right && left" :left :right />
  </div>
</template>
