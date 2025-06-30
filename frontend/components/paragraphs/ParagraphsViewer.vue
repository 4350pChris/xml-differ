<script setup lang="ts">
import ParagraphXMLViewer from "./ParagraphXMLViewer.vue";
import { computed } from "vue";
import { getDiffDiffLeftVersionIdRightVersionIdGetOptions } from "../../client/@tanstack/vue-query.gen";
import { useQuery } from "@tanstack/vue-query";

const props = defineProps<{ left: string; right: string }>();
const queryOptions = computed(() =>
  getDiffDiffLeftVersionIdRightVersionIdGetOptions({
    path: {
      left_version_id: props.left,
      right_version_id: props.right,
    },
  }),
);

const { data: diff, status } = useQuery(queryOptions);
</script>

<template>
  <p v-if="status === 'pending'">Loading...</p>
  <p v-else-if="status === 'error'">Error!</p>
  <div v-else class="space-y-4">
    <ParagraphXMLViewer v-for="(paragraph, i) in diff" :key="i" :content="paragraph as string" />
  </div>
</template>
