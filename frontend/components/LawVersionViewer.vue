<script setup lang="ts">
import { LawDetailProjection } from "../client";
import { computed, onServerPrefetch, ref, useTemplateRef, watch } from "vue";
import { getDiffDiffLeftVersionIdRightVersionIdGetOptions } from "../client/@tanstack/vue-query.gen";
import { useQuery } from "@tanstack/vue-query";
import DiffOptions, { type DifferOptions } from "./DiffOptions.vue";
import { useUrlSearchParams } from "@vueuse/core";
import { usePageContext } from "vike-vue/usePageContext";
import MoveChangeButtons from "./paragraphs/MoveChangeButtons.vue";
import ParagraphXMLViewer from "./paragraphs/ParagraphXMLViewer.vue";
import TableOfContents from "./paragraphs/TableOfContents.vue";

const props = defineProps<{ law: LawDetailProjection }>();
const urlParams = useUrlSearchParams();
const pageContext = usePageContext();
const { search } = pageContext.urlParsed;
const left = ref<string>(search.left ?? props.law.versions[0]?.id);
const right = ref<string>(search.right ?? props.law.versions[props.law.versions.length - 1]?.id);

const diffEl = useTemplateRef<HTMLElement>("diffParent");

watch(
  [left, right],
  ([newLeft, newRight]) => {
    urlParams.left = newLeft;
    urlParams.right = newRight;
  },
  { immediate: true },
);

const options = ref<DifferOptions>({
  fast_match: !!search.fast_match,
  ratio_mode: (search.ratio_mode as "fast") ?? "fast",
  F: search.F ? parseFloat(search.F) : 0.5,
});

watch(options, (newOptions) => {
  Object.entries(newOptions).forEach(([key, value]) => {
    urlParams[key] = value.toString();
  });
});

const handleSubmit = (versions: [string, string], newOptions: DifferOptions) => {
  left.value = versions[0];
  right.value = versions[1];
  options.value = newOptions;
};

const queryOptions = computed(() => {
  return getDiffDiffLeftVersionIdRightVersionIdGetOptions({
    path: {
      left_version_id: left.value,
      right_version_id: right.value,
    },
    query: options.value,
  });
});

const { data: diff, error, status, suspense } = useQuery(queryOptions);
onServerPrefetch(suspense);
</script>

<template>
  <div>
    <DiffOptions :law :initial="{ left, right, options }" @submit="handleSubmit" />
    <div v-if="status === 'pending'" class="skeleton w-full h-96"></div>
    <p v-else-if="status === 'error'">
      Error! <code>{{ error }}</code>
    </p>
    <template v-else-if="diff">
      <TableOfContents class="not-prose fixed top-16 bottom-0 left-0 w-20 md:w-24 lg:w-28" :parent-element="diffEl" />
      <MoveChangeButtons class="fixed bottom-4 right-4" :parent-element="diffEl" />
      <div ref="diffParent">
        <ParagraphXMLViewer v-for="(content, i) in diff" :key="`${i}-${content.length}`" :content />
      </div>
    </template>
  </div>
</template>
