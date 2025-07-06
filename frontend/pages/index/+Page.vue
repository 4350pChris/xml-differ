<template>
  <h1 class="text-2xl mb-4">Gesetze</h1>
  <label class="label">
    <input v-model="params.all" type="checkbox" class="checkbox" name="all" />
    <span>Alle Gesetze anzeigen</span>
  </label>
  <LawList :laws="laws ?? []">
    <template #default="{ law }">
      <div>{{ law.name }}</div>
      <div class="text-xs text-gray-500">{{ law.long_title ?? law.short_title }}</div>
    </template>
  </LawList>
</template>

<script setup lang="ts">
import LawList from "../../components/LawList.vue";
import { useAllLaws } from "../../composables/useAllLaws";
import { onServerPrefetch } from "vue";
import { makeBoolOptions, useSyncedUrlParam } from "../../composables/useSyncedUrlParam";

const params = useSyncedUrlParam({ all: makeBoolOptions(false) });
const { data: laws, suspense } = useAllLaws(() => params.value.all);

onServerPrefetch(suspense);
</script>
