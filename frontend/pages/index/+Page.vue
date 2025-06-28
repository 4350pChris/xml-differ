<template>
  <h1 class="font-bold text-3xl pb-4">Gesetze</h1>
  <ul class="list">
    <li v-for="law in laws" :key="law.id" class="list-row">
      <Link :href="law.url">
        <div>{{ law.name }}</div>
        <div class="text-xs text-gray-500">{{ law.long_title ?? law.short_title }}</div>
      </Link>
    </li>
  </ul>
</template>

<script setup lang="ts">
import Link from "../../components/Link.vue";
import { useLawList } from "../../composables/useLawList";

const { laws } = useLawList();
</script>
