<script setup lang="ts">
import { computed } from "vue";
import { useWindowVirtualizer } from "@tanstack/vue-virtual";
import Link from "./Link.vue";
import { useAllLaws } from "../composables/useAllLaws";

const { data } = useAllLaws();

const laws = computed(() =>
  (data.value ?? []).map((law) => ({
    ...law,
    url: `/law/${law.id}`,
  })),
);

const rowVirtualizerOptions = computed(() => {
  return {
    count: laws.value.length,
    estimateSize: () => 40,
    overscan: 5,
  };
});

const rowVirtualizer = useWindowVirtualizer(rowVirtualizerOptions);

const virtualRows = computed(() => rowVirtualizer.value.getVirtualItems());

const totalSize = computed(() => rowVirtualizer.value.getTotalSize());

const measureElement = (el: HTMLElement | undefined) => {
  if (!el) {
    return;
  }

  rowVirtualizer.value.measureElement(el);

  return undefined;
};
</script>

<template>
  <div class="relative w-full" :style="{ height: `${totalSize}px` }">
    <div
      v-for="virtualRow in virtualRows"
      :key="virtualRow.index"
      :ref="measureElement"
      class="absolute top-0 left-0 w-full"
      :data-index="virtualRow.index"
      :style="{
        transform: `translateY(${virtualRow.start}px)`,
      }"
    >
      <Link :href="laws[virtualRow.index].url">
        <slot :law="laws[virtualRow.index]">{{ laws[virtualRow.index].name }}</slot>
      </Link>
    </div>
  </div>
</template>
