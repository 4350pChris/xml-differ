<script setup lang="ts">
import { computed, onMounted, shallowRef } from "vue";
import { useEventListener, useMutationObserver, whenever, useThrottleFn } from "@vueuse/core";
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

const throttledScrollHandler = useThrottleFn(() => {
  const targetY = window.innerHeight / 2;
  const entry = [...headerElements.value].reverse().find((wrapper) => {
    const { top } = wrapper.getBoundingClientRect();
    const distance = top - targetY;
    return distance < 0 && toc.value.has(wrapper.id);
  });
  visibleElement.value = entry?.id;
}, 100);

onMounted(() => {
  useEventListener("scroll", throttledScrollHandler);
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

const scrollTo = (item: TocItem) => {
  const id = item.href.slice(1);
  visibleElement.value = id;
  emits("scrollTo", id);
};
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
        @click.prevent="scrollTo(item)"
      >
        <div class="indicator grow">
          <ChangeIndicator :change="item.change" />
          <span class="truncate">{{ item.name }}</span>
        </div>
      </a>
    </li>
  </ol>
</template>
