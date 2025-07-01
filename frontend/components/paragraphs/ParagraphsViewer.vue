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
  <div v-if="status === 'pending'" class="skeleton w-full h-96"></div>
  <p v-else-if="status === 'error'">Error!</p>
  <div v-else class="space-y-4">
    <ParagraphXMLViewer v-for="(content, i) in diff" :key="i" :content />
  </div>
</template>
