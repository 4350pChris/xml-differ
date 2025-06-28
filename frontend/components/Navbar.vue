<script setup lang="ts">
import { usePageContext } from "vike-vue/usePageContext";
import { getTitle } from "../pages/utils";

const pageContext = usePageContext();
const title = getTitle(pageContext);
</script>

<template>
  <div
    class="bg-base-100/90 text-base-content sticky top-0 z-30 flex h-16 w-full [transform:translate3d(0,0,0)] justify-center backdrop-blur transition-shadow duration-100 print:hidden shadow-xs"
  >
    <div class="navbar w-full py-0">
      <h1 class="text-2xl">{{ title }}</h1>
    </div>
  </div>
</template>
