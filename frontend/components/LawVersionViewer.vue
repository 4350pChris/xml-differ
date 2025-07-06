<script setup lang="ts">
import { LawDetailProjection } from "../client";
import { computed, onServerPrefetch, useTemplateRef } from "vue";
import { getDiffDiffLeftVersionIdRightVersionIdGetOptions } from "../client/@tanstack/vue-query.gen";
import { useQuery } from "@tanstack/vue-query";
import DiffOptions, { type DifferOptions } from "./DiffOptions.vue";
import MoveChangeButtons from "./paragraphs/MoveChangeButtons.vue";
import ParagraphXMLViewer from "./paragraphs/ParagraphXMLViewer.vue";
import TableOfContents from "./paragraphs/TableOfContents.vue";
import {
  makeBoolOptions,
  makeFloatOptions,
  makeStringOptions,
  useSyncedUrlParam,
} from "../composables/useSyncedUrlParam";

const props = defineProps<{ law: LawDetailProjection }>();
const versions = useSyncedUrlParam({
  oldVersion: makeStringOptions(props.law.versions[0]?.id),
  newVersion: makeStringOptions(props.law.versions[props.law.versions.length - 1]?.id),
});

const options = useSyncedUrlParam({
  fast_match: makeBoolOptions(false),
  ratio_mode: makeStringOptions<DifferOptions["ratio_mode"]>("fast"),
  F: makeFloatOptions(0.5),
  split: makeBoolOptions(false),
});

const diffEl = useTemplateRef<HTMLElement>("diffParent");

const handleSubmit = ([oldVersion, newVersion]: [string, string], newOptions: DifferOptions) => {
  versions.value = { oldVersion, newVersion };
  options.value = newOptions;
};

const queryOptions = computed(() => {
  return getDiffDiffLeftVersionIdRightVersionIdGetOptions({
    path: {
      left_version_id: versions.value.oldVersion,
      right_version_id: versions.value.newVersion,
    },
    query: options.value,
  });
});

const { data: diff, status, suspense } = useQuery(queryOptions);
onServerPrefetch(suspense);
</script>

<template>
  <div class="prose mx-auto flex flex-col items-center min-w-0 w-full">
    <h1>{{ law.name }}</h1>
    <p>{{ law.long_title ?? law.short_title }}</p>
    <DiffOptions
      class="fixed bottom-4 left-24 md:left-28 lg:left-32"
      :law
      :initial="{ ...versions, options }"
      @submit="handleSubmit"
    />
    <div v-if="status === 'pending'" class="skeleton w-full h-96"></div>
    <p v-else-if="status === 'error'" class="text-error-content">Fehler beim Laden</p>
    <template v-else-if="diff">
      <teleport to="#teleported">
        <TableOfContents class="fixed top-16 bottom-0 left-0 w-16 md:w-24 lg:w-28" :parent-element="diffEl" />
        <MoveChangeButtons class="fixed bottom-4 right-4" :parent-element="diffEl" />
      </teleport>
      <div ref="diffParent" class="max-w-full" :class="[options.split ? 'grid grid-cols-2 gap-4' : 'flex flex-col']">
        <template v-for="(paragraph, i) in diff" :key="`${i}-${paragraph.map((c) => c.length)}`">
          <ParagraphXMLViewer v-for="(content, j) in paragraph" :key="`p-${j}-${content.length}`" :content />
        </template>
      </div>
    </template>
  </div>
</template>
