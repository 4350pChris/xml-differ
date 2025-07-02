<script setup lang="ts">
import { computed, watch } from "vue";
import { useCycleList, useTimeoutFn } from "@vueuse/core";

const props = defineProps<{
  parentElement: HTMLElement | null;
}>();

// get all diff elements from the parent element
const diffs = computed(() => {
  if (props.parentElement) {
    return Array.from(props.parentElement.querySelectorAll<HTMLElement>(".diff-insert, .diff-del"));
  }
  return [];
});

const { next, prev, state, index: _index, go } = useCycleList(diffs);

const index = computed({
  get: () => _index.value + 1, // +1 for 1-based index
  set: (value: number) => {
    if (value < 1 || value > diffs.value.length) {
      return;
    }
    go(value - 1); // -1 for 0-based index
  },
});

const visibilityClassList = ["animate-pulse", "outline", "outline-blue-500"];

watch(state, (newCurrent, oldCurrent) => {
  if (!oldCurrent || !newCurrent) {
    return;
  }
  oldCurrent.classList.remove("current");
  newCurrent.classList.add("current", ...visibilityClassList);
  newCurrent.scrollIntoView({ behavior: "smooth" });
  pulseTimeout.start(newCurrent);
});

const pulseTimeout = useTimeoutFn((node: HTMLElement | undefined) => {
  node?.classList.remove(...visibilityClassList);
}, 2000);
</script>

<template>
  <div class="join bg-base-100 shadow-lg rounded-box">
    <button class="btn btn-square btn-ghost join-item" title="Vorherige Änderung" @click="prev()">
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
        <!-- Icon from Google Material Icons by Material Design Authors - https://github.com/material-icons/material-icons/blob/master/LICENSE -->
        <path fill="currentColor" d="m4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8z" />
      </svg>
    </button>
    <button class="btn btn-square btn-ghost join-item" title="Nächste Änderung" @click="next()">
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
        <!-- Icon from Google Material Icons by Material Design Authors - https://github.com/material-icons/material-icons/blob/master/LICENSE -->
        <path fill="currentColor" d="m20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8z" />
      </svg>
    </button>
    <input
      v-model.number="index"
      min="1"
      :max="diffs.length"
      type="number"
      title="Gehe zu Änderung"
      class="input input-bordered join-item w-20"
    />
    <span class="join-item self-center-safe px-2"> / {{ diffs.length }} </span>
  </div>
</template>

<style>
.diff-insert,
.diff-del {
  scroll-margin-top: 4.5rem;
}
</style>
