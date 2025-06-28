<template>
  <VirtualLawList>
    <template #default="{ law }">
      <div>{{ law.name }}</div>
      <div class="text-xs text-gray-500">{{ law.long_title ?? law.short_title }}</div>
    </template>
  </VirtualLawList>
</template>

<script setup lang="ts">
import VirtualLawList from "../../components/VirtualLawList.vue";
</script>
