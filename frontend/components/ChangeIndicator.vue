<script lang="ts">
export type ChangeType = boolean | "addition" | "deletion" | "mixed";
</script>

<script setup lang="ts">
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
