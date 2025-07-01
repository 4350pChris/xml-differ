<script setup lang="ts">
import LawVersionViewer from "../../../components/LawVersionViewer.vue";
import { useQuery } from "@tanstack/vue-query";
import { usePageContext } from "vike-vue/usePageContext";
import { computed, onServerPrefetch } from "vue";
import { getLawLawsLawIdGetOptions } from "../../../client/@tanstack/vue-query.gen";

const pageContext = usePageContext();
const options = computed(() => {
  return getLawLawsLawIdGetOptions({
    path: {
      law_id: pageContext.routeParams.id as string,
    },
  });
});

const { data: law, suspense } = useQuery(options);
onServerPrefetch(suspense);
</script>

<template>
  <div v-if="law" class="p-4">
    <h1 class="text-2xl font-bold">{{ law.name }}</h1>
    <p class="text-gray-700">{{ law.long_title ?? law.short_title }}</p>
    <LawVersionViewer :law />
  </div>
</template>
