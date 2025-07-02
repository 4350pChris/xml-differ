<template>
  <h1 class="text-2xl mb-4">Gesetze</h1>
  <LawList :laws="laws ?? []">
    <template #default="{ law }">
      <div>{{ law.name }}</div>
      <div class="text-xs text-gray-500">{{ law.long_title ?? law.short_title }}</div>
    </template>
  </LawList>
</template>

<script setup lang="ts">
import LawList from "../../components/LawList.vue";
import { useAllLaws } from "../../composables/useAllLaws";
import { onServerPrefetch } from "vue";

const { data: laws, suspense } = useAllLaws();

onServerPrefetch(suspense);
</script>
