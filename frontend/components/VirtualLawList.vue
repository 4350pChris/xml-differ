<script setup lang="ts">
import { useData } from "vike-vue/useData";
import { Data } from "../pages/+data";
import { computed, ref } from "vue";
import { useVirtualizer } from "@tanstack/vue-virtual";
import Link from "./Link.vue";

defineProps<{ fullPage?: boolean }>();
const data = useData<Data>();

const laws = data.laws.map((law) => ({
  ...law,
  url: `/law/${law.id}`,
}));

const parentRef = ref<HTMLElement | null>(null);

const rowVirtualizerOptions = computed(() => {
  return {
    count: laws.length,
    getScrollElement: () => parentRef.value,
    estimateSize: () => 40,
    overscan: 5,
  };
});

const rowVirtualizer = useVirtualizer(rowVirtualizerOptions);

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
  <div ref="parentRef" class="overflow-y-auto w-full" :style="{ flex: 1 }">
    <div
      class="relative w-full rounded-box px-2"
      :style="{ height: `${(totalSize * 100) / (parentRef?.offsetHeight || 1)}%` }"
    >
      <div
        class="absolute top-0 left-0 w-full"
        :style="{
          transform: `translateY(${virtualRows[0]?.start ?? 0}px)`,
        }"
      >
        <div
          v-for="virtualRow in virtualRows"
          :key="virtualRow.index"
          :ref="measureElement"
          :data-index="virtualRow.index"
        >
          <Link :href="laws[virtualRow.index].url">
            <slot :law="laws[virtualRow.index]">{{ laws[virtualRow.index].name }}</slot>
          </Link>
        </div>
      </div>
    </div>
  </div>
</template>
