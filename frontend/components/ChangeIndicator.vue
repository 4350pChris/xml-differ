<script setup lang="ts">
import type { ChangeType } from "../composables/useParsedDiff";

defineProps<{
  change: ChangeType;
}>();
</script>

<template>
  <span
    v-if="change"
    title="Änderungen vorhanden"
    class="indicator-item status"
    :class="{
      'status-success': change === 'addition',
      'status-error': change === 'deletion',
      'status-info': change === 'mixed',
    }"
  ></span>
</template>
