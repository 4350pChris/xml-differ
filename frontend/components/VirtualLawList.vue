<script setup lang="ts">
import { useData } from "vike-vue/useData";
import { Data } from "../pages/index/+data";
import { computed } from "vue";
import { useWindowVirtualizer } from "@tanstack/vue-virtual";
import Link from "./Link.vue";

const data = useData<Data>();

const laws = data.laws.map((law) => ({
  ...law,
  url: `/law/${law.id}`,
}));

const rowVirtualizerOptions = computed(() => {
  return {
    count: laws.length,
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
