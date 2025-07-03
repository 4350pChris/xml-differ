<script setup lang="ts">
import { LawDetailProjection } from "../client";
import LawVersionSelector from "./LawVersionSelector.vue";
import { ref, watch } from "vue";
import ParagraphsViewer from "./paragraphs/ParagraphsViewer.vue";
import { useUrlSearchParams } from "@vueuse/core";
import { usePageContext } from "vike-vue/usePageContext";

const props = defineProps<{ law: LawDetailProjection }>();

const urlParams = useUrlSearchParams();
const pageContext = usePageContext();
const { search } = pageContext.urlParsed;
const left = ref<string>(search.left ?? props.law.versions[0]?.id);
const right = ref<string>(search.right ?? props.law.versions[props.law.versions.length - 1]?.id);

watch(
  [left, right],
  ([newLeft, newRight]) => {
    urlParams.left = newLeft;
    urlParams.right = newRight;
  },
  { immediate: true },
);
</script>

<template>
  <div>
    <div class="flex items-center justify-center pb-2 gap-4">
      <LawVersionSelector v-model="left" legend="Alte Version" :versions="law.versions" />
      <LawVersionSelector v-model="right" legend="Neue Version" :versions="law.versions" />
    </div>
    <ParagraphsViewer v-if="right && left" :left :right />
  </div>
</template>
