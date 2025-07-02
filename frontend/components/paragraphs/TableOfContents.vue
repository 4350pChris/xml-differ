<script setup lang="ts">
import { computed } from "vue";
import { useWindowScroll } from "@vueuse/core";

const props = defineProps<{
  parentElement: HTMLElement | null;
}>();

// get all diff elements from the parent element
const tocElements = computed(() => {
  if (props.parentElement) {
    return Array.from(props.parentElement.querySelectorAll<HTMLElement>("h2"));
  }
  return [];
});
const { y } = useWindowScroll();
// const visibleElement = ref<HTMLElement>();
// find uppermost visible element in the viewport
const visibleElement = computed(() => {
  if (!props.parentElement) return null;
  const elements = tocElements.value;
  for (const el of elements) {
    const rect = el.getBoundingClientRect();
    if (rect.top >= 0 && rect.bottom <= y.value) {
      return el;
    }
  }
  return null;
});

const toc = computed(() => {
  return tocElements.value.map((el, index) => ({
    name: el.textContent?.trim()?.split(" ").slice(0, 2).join(" ") || `Item ${index + 1}`,
    id: el.id,
    visible: visibleElement.value === el,
  }));
});
</script>

<template>
  <ol class="overflow-y-auto bg-base-100 shadow-sm">
    <li v-for="item in toc" :key="item.id" class="truncate" :class="{ 'font-bold': item.visible }">
      <a :href="`#${item.id}`" class="block px-2 py-1 hover:bg-base-200" :title="`Zu ${item.name} springen`">
        {{ item.name }}
      </a>
    </li>
  </ol>
</template>

<style scoped></style>
