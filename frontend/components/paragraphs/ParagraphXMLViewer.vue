<script setup lang="ts">
import ChangeIndicator from "../ChangeIndicator.vue";
import { ParsedDiff } from "../../composables/useParsedDiff";

defineProps<{ diff: ParsedDiff }>();
</script>

<template>
  <div :id="diff.id" class="scroll-mt-16 indicator prose w-full" data-wrapper>
    <ChangeIndicator :change="diff.change" />
    <div class="w-full break-words" v-html="diff.doc.innerHTML"></div>
  </div>
</template>

<style scoped>
@reference "../../layouts/tailwind.css";

:deep(.S4) {
  margin-left: 0.5rem;
}

:deep(.S3) {
  margin-left: 1rem;
}

:deep(.S2) {
  margin-left: 1.5rem;
}

:deep(.S1) {
  margin-left: 2rem;
}

:deep(enbez) {
  margin-inline: 0.5rem;
}

:deep(.diff-insert) {
  text-decoration: none;
  @apply bg-success/30 border-success p-1 scroll-mt-20;
}

:deep(.diff-del) {
  text-decoration: none;
  @apply bg-error/30 border-error p-1 scroll-mt-20;
}
</style>
