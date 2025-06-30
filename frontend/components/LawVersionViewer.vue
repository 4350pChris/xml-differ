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
  <div class="flex items-center justify-center pb-2 gap-4">
    <div>
      <LawVersionSelector v-model="left" legend="Linke Version" :versions="law.versions" />
      <LawVersionSelector v-model="right" legend="Rechte Version" :versions="law.versions" />
      <ParagraphsViewer v-if="right" :version-id="right" />
    </div>
  </div>
</template>
