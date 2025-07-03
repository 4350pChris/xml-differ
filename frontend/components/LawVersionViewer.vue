<script setup lang="ts">
import { LawDetailProjection } from "../client";
import LawVersionSelector from "./LawVersionSelector.vue";
import { computed, onServerPrefetch, ref, watch } from "vue";
import ParagraphsViewer from "./paragraphs/ParagraphsViewer.vue";
import { useUrlSearchParams } from "@vueuse/core";
import { usePageContext } from "vike-vue/usePageContext";
import { getDiffDiffLeftVersionIdRightVersionIdGetOptions } from "../client/@tanstack/vue-query.gen";
import { useQuery } from "@tanstack/vue-query";

const props = defineProps<{ law: LawDetailProjection }>();

const urlParams = useUrlSearchParams();
const pageContext = usePageContext();
const { search } = pageContext.urlParsed;
const left = ref<string>(search.left ?? props.law.versions[0]?.id);
const right = ref<string>(search.right ?? props.law.versions[props.law.versions.length - 1]?.id);

watch(
  [left, right],
  ([newLeft, newRight]) => {
    urlParams.left = newLeft;
    urlParams.right = newRight;
  },
  { immediate: true },
);

const queryOptions = computed(() => {
  console.log("Querying diff for versions:", left.value, right.value, "with fast match:", urlParams.fast);
  return getDiffDiffLeftVersionIdRightVersionIdGetOptions({
    path: {
      left_version_id: left.value,
      right_version_id: right.value,
    },
    query: {
      fast_match: !!urlParams.fast,
    },
  });
});

const { data: diff, status, suspense } = useQuery(queryOptions);
onServerPrefetch(suspense);
</script>

<template>
  <div>
    <div class="flex items-center justify-center pb-2 gap-4">
      <LawVersionSelector v-model="left" legend="Alte Version" :versions="law.versions" />
      <LawVersionSelector v-model="right" legend="Neue Version" :versions="law.versions" />
      <fieldset class="fieldset bg-base-100 border-base-300 rounded-box w-64 border p-4">
        <legend class="fieldset-legend">XMLdiff Optionen</legend>
        <label class="label">
          <input v-model="urlParams.fast" type="checkbox" class="checkbox" name="fast_match" />
          Fast Match
        </label>
      </fieldset>
    </div>
    <div v-if="status === 'pending'" class="skeleton w-full h-96"></div>
    <p v-else-if="status === 'error'">Error!</p>
    <ParagraphsViewer v-else-if="diff" :diff />
  </div>
</template>
