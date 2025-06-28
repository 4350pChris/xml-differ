<template>
  <div class="flex flex-col min-h-screen max-h-screen">
    <h1 class="font-bold text-3xl pb-4">Gesetze</h1>
    <VirtualLawList class="grow">
      <template #default="{ law }">
        <div>{{ law.name }}</div>
        <div class="text-xs text-gray-500">{{ law.long_title ?? law.short_title }}</div>
      </template>
    </VirtualLawList>
  </div>
</template>

<script setup lang="ts">
import VirtualLawList from "../../components/VirtualLawList.vue";
</script>
