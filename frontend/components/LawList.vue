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
  <ul class="flex flex-col divide-y divide-gray-200 bg-base-100">
    <li v-for="law in laws" :key="law.id">
      <a class="w-full inline-block py-2 px-4 hover:bg-gray-100" :href="`/law/${law.id}`">
        <slot :law="law">{{ law.name }}</slot>
      </a>
    </li>
  </ul>
</template>
