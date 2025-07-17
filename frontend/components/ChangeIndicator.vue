<script setup lang="ts">
import type { ChangeType } from "../composables/useParsedDiff";

defineProps<{
  change: ChangeType;
}>();

const titles = {
  addition: "Hinzugefügt",
  deletion: "Gelöscht",
  mixed: "Geändert",
};

const statuses = {
  addition: "status-success",
  deletion: "status-error",
  mixed: "status-info",
};
</script>

<template>
  <span v-if="change" :title="titles[change]" class="indicator-item status" :class="statuses[change]"></span>
</template>
