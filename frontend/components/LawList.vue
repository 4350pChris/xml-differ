<script setup lang="ts">
import { computed } from "vue";
import { LawListProjection } from "../client";

const props = defineProps<{
  laws: LawListProjection[];
}>();

const laws = computed(() =>
  props.laws.map((law) => ({
    ...law,
    url: `/law/${law.id}`,
  })),
);
</script>

<template>
  <ul class="flex flex-col divide-y divide-base-content/10 bg-base-100">
    <li v-for="law in laws" :key="law.id">
      <a class="w-full inline-block py-2 px-4 hover:bg-base-content/10" :href="`/law/${law.id}`">
        <slot :law="law">
          <span class="inline-block w-full">{{ law.name }}</span>
          <span class="text-xs text-gray-500">{{ law.long_title ?? law.short_title }}</span>
        </slot>
      </a>
    </li>
  </ul>
</template>
