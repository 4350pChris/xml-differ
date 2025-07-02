<script setup lang="ts">
import ParagraphXMLViewer from "./ParagraphXMLViewer.vue";
import { computed, onServerPrefetch, useTemplateRef } from "vue";
import { getDiffDiffLeftVersionIdRightVersionIdGetOptions } from "../../client/@tanstack/vue-query.gen";
import { useQuery } from "@tanstack/vue-query";
import MoveChangeButtons from "./MoveChangeButtons.vue";
import TableOfContents from "./TableOfContents.vue";

const props = defineProps<{ left: string; right: string }>();
const queryOptions = computed(() =>
  getDiffDiffLeftVersionIdRightVersionIdGetOptions({
    path: {
      left_version_id: props.left,
      right_version_id: props.right,
    },
  }),
);

const { data: diff, status, suspense } = useQuery(queryOptions);
onServerPrefetch(suspense);
const diffEl = useTemplateRef<HTMLElement>("diffParent");
</script>

<template>
  <div v-if="status === 'pending'" class="skeleton w-full h-96"></div>
  <p v-else-if="status === 'error'">Error!</p>
  <template v-else>
    <TableOfContents class="not-prose fixed top-16 bottom-0 left-0 w-16" :parent-element="diffEl" />
    <MoveChangeButtons class="fixed bottom-4 right-4" :parent-element="diffEl" />
    <div ref="diffParent" :key="`${props.left}-${props.right}`">
      <ParagraphXMLViewer v-for="(content, i) in diff" :key="i" :content />
    </div>
  </template>
</template>
