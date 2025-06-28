<script setup lang="ts">
import { useData } from "vike-vue/useData";
import { Data } from "./+data";
import LawVersionSelector from "../../../components/LawVersionSelector.vue";
import { ref } from "vue";

const { law } = useData<Data>();
const left = ref();
const right = ref();
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">{{ law.name }}</h1>
    <p class="text-gray-700">{{ law.long_title ?? law.short_title }}</p>
    <div class="flex items-center justify-center pb-2 gap-4">
      <LawVersionSelector v-model="left" legend="Linke Version" :versions="law.versions" />
      <LawVersionSelector v-model="right" legend="Rechte Version" :versions="law.versions" />
    </div>
  </div>
</template>
