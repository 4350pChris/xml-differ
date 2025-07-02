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

const { data: law, status, suspense } = useQuery(options);
onServerPrefetch(suspense);
</script>

<template>
  <div class="p-4 pl-20 md:pr-12 lg:pr-20">
    <template v-if="status === 'pending'">
      <div class="skeleton h-16 w-24"></div>
      <div class="skeleton h-8 w-48"></div>
    </template>
    <template v-else-if="status === 'error'">
      <p>Error loading law details!</p>
    </template>
    <template v-else-if="law">
      <h1 class="text-2xl font-bold">{{ law.name }}</h1>
      <p class="text-gray-700">{{ law.long_title ?? law.short_title }}</p>
      <LawVersionViewer :law />
    </template>
  </div>
</template>
