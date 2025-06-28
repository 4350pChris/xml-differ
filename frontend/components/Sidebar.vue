<template>
  <div class="drawer-side z-40">
    <label for="drawer" class="drawer-overlay" aria-label="Close menu"></label>
    <aside class="bg-base-100 w-80">
      <div class="max-h-screen min-h-screen flex flex-col">
        <VirtualLawList />
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import VirtualLawList from "../components/VirtualLawList.vue";
</script>
