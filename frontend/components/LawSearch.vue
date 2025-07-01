<script setup lang="ts">
import { useAllLaws } from "../composables/useAllLaws";
import { computed, ref, useTemplateRef } from "vue";
import LawList from "./LawList.vue";
import { unrefElement, useMagicKeys, whenever } from "@vueuse/core";

const { data: laws } = useAllLaws();
const searchQuery = ref("");

const filteredLaws = computed(() => {
  if (!laws.value || !searchQuery.value) return null;
  const query = searchQuery.value.toLowerCase();
  return laws.value.filter(
    (law) =>
      law.name.toLowerCase().includes(query) ||
      (law.short_title && law.short_title.toLowerCase().includes(query)) ||
      (law.long_title && law.long_title.toLowerCase().includes(query)),
  );
});

const inputRef = useTemplateRef<HTMLInputElement>("search");
const keys = useMagicKeys();
whenever(keys.cmd_K, () => {
  const el = unrefElement(inputRef);
  el?.focus();
  el?.select();
});
</script>

<template>
  <div class="dropdown max-w-lg">
    <label class="input w-full">
      <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" fill="none" stroke="currentColor">
          <circle cx="11" cy="11" r="8"></circle>
          <path d="m21 21-4.3-4.3"></path>
        </g>
      </svg>
      <input
        ref="search"
        v-model="searchQuery"
        type="search"
        spellcheck="false"
        autocomplete="off"
        class="grow"
        placeholder="Search"
      />
      <kbd class="kbd kbd-sm">⌘</kbd>
      <kbd class="kbd kbd-sm">K</kbd>
    </label>
    <LawList
      v-if="filteredLaws"
      tabindex="0"
      class="dropdown-content rounded-box z-1 w-full max-h-96 overflow-y-auto p-2 shadow-sm"
      :laws="filteredLaws"
    />
  </div>
</template>
