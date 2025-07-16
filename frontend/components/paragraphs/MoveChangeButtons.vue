<script setup lang="ts">
import { computed, watch } from "vue";
import { useCycleList } from "@vueuse/core";

const props = defineProps<{
  count: number;
}>();

const emits = defineEmits<{
  "update:index": [number];
}>();

const { next, prev, index: _index, go } = useCycleList(Array.from({ length: props.count }, (_, i) => i));

const index = computed({
  get: () => _index.value + 1, // +1 for 1-based index
  set: (value: number) => {
    if (value < 1 || value > props.count) {
      return;
    }
    go(value - 1); // -1 for 0-based index
  },
});

watch(_index, (newIndex) => {
  emits("update:index", newIndex);
});
</script>

<template>
  <div class="join bg-base-100 z-10 shadow-lg rounded-box">
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
    <label class="grow input input-sm w-24 self-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="opacity-50" width="32" height="32" viewBox="0 0 24 24">
        <!-- Icon from Material Symbols by Google - https://github.com/google/material-design-icons/blob/master/LICENSE -->
        <path
          fill="currentColor"
          d="m12.05 19l2.85-2.825l-2.85-2.825L11 14.4l1.075 1.075q-.7.025-1.362-.225t-1.188-.775q-.5-.5-.763-1.15t-.262-1.3q0-.425.113-.85t.312-.825l-1.1-1.1q-.425.625-.625 1.325T7 12q0 .95.375 1.875t1.1 1.65t1.625 1.088t1.85.387l-.95.95zm4.125-4.25q.425-.625.625-1.325T17 12q0-.95-.363-1.888T15.55 8.45t-1.638-1.075t-1.862-.35L13 6.05L11.95 5L9.1 7.825l2.85 2.825L13 9.6l-1.1-1.1q.675 0 1.375.263t1.2.762t.763 1.15t.262 1.3q0 .425-.112.85t-.313.825zM12 22q-2.075 0-3.9-.788t-3.175-2.137T2.788 15.9T2 12t.788-3.9t2.137-3.175T8.1 2.788T12 2t3.9.788t3.175 2.137T21.213 8.1T22 12t-.788 3.9t-2.137 3.175t-3.175 2.138T12 22m0-2q3.35 0 5.675-2.325T20 12t-2.325-5.675T12 4T6.325 6.325T4 12t2.325 5.675T12 20m0-8"
        />
      </svg>
      <input v-model.number="index" name="change" min="1" :max="count" type="number" title="Gehe zu Änderung" />
    </label>
    <span class="join-item self-center-safe px-2"> / {{ count }} </span>
  </div>
</template>
