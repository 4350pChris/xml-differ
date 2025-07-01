<script setup lang="ts">
import { computed, onServerPrefetch } from "vue";
import Link from "./Link.vue";
import { useAllLaws } from "../composables/useAllLaws";

const { data, suspense } = useAllLaws();

onServerPrefetch(suspense);

const laws = computed(() =>
  (data.value ?? []).map((law) => ({
    ...law,
    url: `/law/${law.id}`,
  })),
);
</script>

<template>
  <ul class="flex flex-col divide-y divide-gray-200">
    <li v-for="law in laws" :key="law.id" class="py-2 px-4 hover:bg-gray-100">
      <Link class="" :href="`/law/${law.id}`">
        <slot :law="law">{{ law.name }}</slot>
      </Link>
    </li>
  </ul>
</template>
