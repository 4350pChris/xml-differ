<script setup lang="ts">
import { computed, watch } from "vue";
import { throttledRef, useWindowScroll } from "@vueuse/core";
import ChangeIndicator, { ChangeType } from "../ChangeIndicator.vue";

const props = defineProps<{
  parentElement: HTMLElement | null;
}>();

// get all diff elements from the parent element
const headerElements = computed(() => {
  if (props.parentElement) {
    return Array.from(props.parentElement.querySelectorAll<HTMLElement>("[data-wrapper='true']"));
  }
  return [];
});
const reverseHeaders = computed(() => [...headerElements.value.values()].reverse());
const { y: _y } = useWindowScroll();
const y = throttledRef(_y, 100);
// find uppermost visible element in the viewport
const visibleElement = computed(() => {
  // trick to have this trigger when scrolling
  if (!props.parentElement || y.value < 0) return null;
  for (const el of reverseHeaders.value) {
    const rect = el.getBoundingClientRect();
    if (rect.top <= 80) {
      return el.id;
    }
  }
  return null;
});

const getChangeType = (val: string | undefined) => {
  if (!val || val === "false") return false;
  return val as ChangeType;
};

type TocItem = {
  id: `toc-${string}`;
  href: `#${string}`;
  name: string;
  change: ChangeType;
};

const toc = computed(() => {
  const map = new Map<string, TocItem>();
  headerElements.value.forEach((el, index) => {
    map.set(el.id, {
      id: `toc-${el.id}`,
      href: `#${el.id}`,
      name: el.querySelector(".enbez")?.textContent?.trim()?.split(" ").slice(0, 2).join(" ") || `Item ${index + 1}`,
      change: getChangeType(el.dataset.change),
    });
  });
  return map;
});

// if the corresponding toc element is not visible when the visible heading changes, scroll to it
watch(visibleElement, (newVisible) => {
  if (newVisible) {
    const tocItem = toc.value.get(newVisible);
    if (tocItem) {
      // We use DOM manipulation here to save the overhead of keeping all refs in a list
      const target = document.getElementById(tocItem.id);
      if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }
  }
});
</script>

<template>
  <ol class="z-10 overflow-y-auto bg-base-100 shadow-sm">
    <li
      v-for="[headingId, item] in toc.entries()"
      :key="item.id"
      :class="{ 'font-bold': visibleElement === headingId }"
    >
      <a
        :id="item.id"
        :href="item.href"
        class="inline-flex w-full px-2 py-1 hover:bg-base-200"
        :title="`Zu ${item.name} springen`"
      >
        <div class="indicator grow">
          <ChangeIndicator :change="item.change" />
          <span class="truncate">{{ item.name }}</span>
        </div>
      </a>
    </li>
  </ol>
</template>

<style scoped></style>
