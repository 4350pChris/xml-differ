<template>
  <div id="page-content" class="h-full">
    <Navbar />
    <div class="container mx-auto px-4 py-6">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import Navbar from "./Navbar.vue";
</script>

<style>
/* Page Transition Animation */
body.page-is-transitioning #page-content {
  opacity: 0;
}
</style>

<style scoped>
/* Page Transition Animation */
#page-content {
  opacity: 1;
  transition: opacity 0.3s ease-in-out;
}
</style>
