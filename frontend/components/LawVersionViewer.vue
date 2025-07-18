<script setup lang="ts">
import type { LawDetailProjection } from "../client";
import { computed, nextTick, onMounted, onServerPrefetch, shallowRef, useTemplateRef } from "vue";
import { getDiffDiffLeftVersionIdRightVersionIdGetOptions } from "../client/@tanstack/vue-query.gen";
import { useQuery } from "@tanstack/vue-query";
import DiffOptions, { type DifferOptions } from "./DiffOptions.vue";
import ParagraphXMLViewer from "./paragraphs/ParagraphXMLViewer.vue";
import TableOfContents from "./paragraphs/TableOfContents.vue";
import {
  makeBoolOptions,
  makeFloatOptions,
  makeStringOptions,
  useSyncedUrlParam,
} from "../composables/useSyncedUrlParam";
import { clientOnly } from "vike-vue/clientOnly";
import { useParsedDiff } from "../composables/useParsedDiff";
import { type Rect, useWindowVirtualizer } from "@tanstack/vue-virtual";

const props = defineProps<{ law: LawDetailProjection }>();

const MoveChangeButtons = clientOnly(() => import("./paragraphs/MoveChangeButtons.vue"));

const versions = useSyncedUrlParam({
  oldVersion: makeStringOptions(props.law.versions[0]?.id),
  newVersion: makeStringOptions(props.law.versions[props.law.versions.length - 1]?.id),
});

const options = useSyncedUrlParam({
  fast_match: makeBoolOptions(true),
  ratio_mode: makeStringOptions<DifferOptions["ratio_mode"]>("accurate"),
  F: makeFloatOptions(0.5),
  split: makeBoolOptions(false),
});

const diffEl = useTemplateRef<HTMLElement>("diffParent");

const handleSubmit = ([oldVersion, newVersion]: [string, string], newOptions: DifferOptions) => {
  versions.value = { oldVersion, newVersion };
  options.value = newOptions;
};

const queryOptions = computed(() => {
  return getDiffDiffLeftVersionIdRightVersionIdGetOptions({
    path: {
      left_version_id: versions.value.oldVersion,
      right_version_id: versions.value.newVersion,
    },
    query: options.value,
  });
});

const { data: diff, status, suspense } = useQuery(queryOptions);
onServerPrefetch(suspense);

const parsedDiff = useParsedDiff(diff);

const parentOffsetRef = shallowRef(0);

onMounted(() => {
  parentOffsetRef.value = diffEl.value?.offsetTop ?? 0;
});

const virtualizerOptions = computed(() => ({
  count: parsedDiff.value.length,
  estimateSize: () => 500,
  scrollMargin: parentOffsetRef.value - 64,
  overscan: 10,
  initialRect: { height: 800, width: 500 } satisfies Rect,
}));

const rowVirtualizer = useWindowVirtualizer(virtualizerOptions);

const virtualRows = computed(() => rowVirtualizer.value.getVirtualItems());

const totalSize = computed(() => rowVirtualizer.value.getTotalSize());

const measureElement = async (el: Element) => {
  await nextTick();
  if (!el) {
    return;
  }

  rowVirtualizer.value.measureElement(el);
};

// map every change index to a row index
const paragraphByChangeIndex = computed(() => {
  return parsedDiff.value.reduce(
    (acc, diffs, rowIndex) => {
      const innerIndexMap = diffs.flatMap((diff, paragraphIndex) => {
        const diffCount = diff.doc.querySelectorAll(".diff-del, .diff-insert").length;
        return Array.from({ length: diffCount }, (_, changeIndex) => ({
          rowIndex,
          paragraphIndex,
          changeIndex,
        }));
      });

      acc.push(...innerIndexMap);
      return acc;
    },
    [] as { rowIndex: number; paragraphIndex: number; changeIndex: number }[],
  );
});

const visibilityClassList = ["animate-pulse", "outline", "outline-blue-500"];

const scrollToIndex = (index: number) => rowVirtualizer.value.scrollToIndex(index, { align: "start" });

const scrollToChange = async (index: number) => {
  const { rowIndex, paragraphIndex, changeIndex } = paragraphByChangeIndex.value[index];
  if (!virtualRows.value.some((row) => row.index === rowIndex)) {
    scrollToIndex(rowIndex);
    await nextTick();
  }

  const oldCurrent = diffEl.value?.querySelector(".current");
  oldCurrent?.classList.remove("current");
  const paragraph = parsedDiff.value[rowIndex][paragraphIndex];
  const paragraphEl = diffEl.value?.querySelector(`#${paragraph.id}`) as HTMLElement;
  const newCurrent = paragraphEl?.querySelectorAll(".diff-del, .diff-insert")[changeIndex] as HTMLElement;
  newCurrent?.classList.add("current", ...visibilityClassList);
  newCurrent?.scrollIntoView({ behavior: "smooth" });
  setTimeout(() => {
    newCurrent?.classList.remove(...visibilityClassList);
  }, 2000);
};

const scrollToItem = (id: string) => {
  const row = parsedDiff.value.findIndex((row) => row.some((paragraph) => paragraph.id === id));
  if (row > -1) {
    scrollToIndex(row);
  }
};
</script>

<template>
  <div class="mx-auto min-w-0 w-full">
    <div class="prose self-start">
      <h1>{{ law.name }}</h1>
      <p>{{ law.long_title ?? law.short_title }}</p>
    </div>
    <DiffOptions
      class="fixed bottom-4 left-24 md:left-32 lg:left-36"
      :law
      :initial="{ ...versions, options }"
      @submit="handleSubmit"
    />
    <div v-if="status === 'pending'" class="skeleton w-full h-96"></div>
    <p v-else-if="status === 'error'" class="text-error-content">Fehler beim Laden</p>
    <template v-else-if="diff">
      <teleport to="#teleported">
        <TableOfContents
          class="fixed top-16 bottom-0 left-0 w-16 md:w-24 lg:w-28"
          :diffs="parsedDiff"
          :parent-element="diffEl"
          @scroll-to="scrollToItem"
        />
        <MoveChangeButtons
          class="fixed bottom-4 right-4"
          :count="paragraphByChangeIndex.length"
          @update:index="scrollToChange"
        />
      </teleport>
      <div ref="diffParent">
        <div
          class="w-full relative"
          :style="{
            height: `${totalSize}px`,
          }"
          data-allow-mismatch
        >
          <div
            class="absolute top-0 left-0 w-full"
            :style="{
              transform: `translateY(${virtualRows[0]?.start - rowVirtualizer.options.scrollMargin || 0}px)`,
            }"
          >
            <div
              v-for="virtualRow in virtualRows"
              :key="virtualRow.key as string"
              :ref="(el) => measureElement(el as Element)"
              :data-index="virtualRow.index"
              :class="[options.split ? 'grid grid-cols-2 gap-4' : 'flex flex-col']"
            >
              <ParagraphXMLViewer
                v-for="row in parsedDiff[virtualRow.index]"
                :key="`${virtualRow.key}-${row.id}`"
                :diff="row"
              />
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
