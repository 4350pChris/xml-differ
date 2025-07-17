<script setup lang="ts">
import { computed, shallowRef } from "vue";
import { useIntersectionObserver, useMutationObserver, whenever } from "@vueuse/core";
import ChangeIndicator from "../ChangeIndicator.vue";
import type { ChangeType, ParsedDiff } from "../../composables/useParsedDiff";

const props = defineProps<{
  diffs: ParsedDiff[][];
  parentElement: HTMLElement | null;
}>();

const emits = defineEmits<{
  scrollTo: [id: string];
}>();

// get all diff elements from the parent element
const headerElements = shallowRef<HTMLElement[]>([]);

useMutationObserver(
  () => props.parentElement,
  () => {
    if (props.parentElement) {
      headerElements.value = Array.from(props.parentElement.querySelectorAll<HTMLElement>("[data-wrapper]"));
    }
  },
  {
    childList: true,
    subtree: true,
  },
);

const visibleElement = shallowRef<string>();

useIntersectionObserver(
  headerElements,
  ([entry]) => {
    // if the first element is visible, set it as the visible element
    if (entry.isIntersecting) {
      visibleElement.value = entry.target.id;
    }
  },
  {
    root: props.parentElement,
    threshold: 0.1,
  },
);

type TocItem = {
  id: `toc-${string}`;
  href: `#${string}`;
  name: string;
  change: ChangeType;
};

const toc = computed(() => {
  const map = new Map<string, TocItem>();
  props.diffs.forEach((paragraphs) => {
    const { id, doc, change } = paragraphs[paragraphs.length - 1];
    map.set(id, {
      id: `toc-${id}`,
      href: `#${id}`,
      name: doc.querySelector(".enbez")?.textContent?.trim()?.split(" ").slice(0, 2).join(" ") || "Unbenannt",
      change,
    });
  });
  return map;
});

// if the corresponding toc element is not visible when the visible heading changes, scroll to it
whenever(visibleElement, (newVisible) => {
  const tocItem = toc.value.get(newVisible);
  if (tocItem) {
    // We use DOM manipulation here to save the overhead of keeping all refs in a list
    const target = document.getElementById(tocItem.id);
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
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
        @click.prevent="emits('scrollTo', item.href.slice(1))"
      >
        <div class="indicator grow">
          <ChangeIndicator :change="item.change" />
          <span class="truncate">{{ item.name }}</span>
        </div>
      </a>
    </li>
  </ol>
</template>
