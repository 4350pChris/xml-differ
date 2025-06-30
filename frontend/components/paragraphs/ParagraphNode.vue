<script setup lang="ts">
type Json = string | number | boolean | Json[] | { [key: string]: Json };

defineProps<{ node: Json }>();
</script>

<template>
  <template v-if="Array.isArray(node)">
    <ParagraphNode v-for="(item, index) in node" :key="index" :node="item" />
  </template>
  <template v-else-if="typeof node === 'object'">
    <template v-for="[key, value] in Object.entries(node)" :key="key">
      <template v-if="key === '#text'">{{ value }}</template>
      <component :is="key" v-else>
        <ParagraphNode :node="value" />
      </component>
    </template>
  </template>
  <template v-else>{{ node }}</template>
</template>
