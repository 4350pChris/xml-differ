<script setup lang="ts">
import { LawVersionListProjection } from "../client";

defineProps<{ versions: LawVersionListProjection[]; legend: string }>();

const model = defineModel<LawVersionListProjection["id"]>();
</script>

<template>
  <fieldset class="fieldset">
    <legend class="fieldset-legend">{{ legend }}</legend>
    <select v-model="model" :name="legend" class="select">
      <option disabled selected>Wähle eine Version</option>
      <option v-for="version in versions" :key="version.id" :value="version.id">{{ version.date }}</option>
    </select>
  </fieldset>
</template>
