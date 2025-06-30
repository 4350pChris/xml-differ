<script setup lang="ts">
import { useData } from "vike-vue/useData";
import { Data } from "./+data";
import LawVersionViewer from "../../../components/LawVersionViewer.vue";

const { law } = useData<Data>();
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">{{ law.name }}</h1>
    <p class="text-gray-700">{{ law.long_title ?? law.short_title }}</p>
    <LawVersionViewer :law />
  </div>
</template>
