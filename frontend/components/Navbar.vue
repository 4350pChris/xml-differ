<script setup lang="ts">
import { usePageContext } from "vike-vue/usePageContext";
import { computed } from "vue";
import LawSearch from "./LawSearch.vue";

const pageContext = usePageContext();
const isRootPath = computed(() => pageContext.urlPathname === "/");
</script>

<template>
  <div
    class="bg-base-100/90 text-base-content sticky top-0 z-30 flex h-16 w-full [transform:translate3d(0,0,0)] justify-center backdrop-blur transition-shadow duration-100 print:hidden shadow-xs"
  >
    <div class="navbar w-full py-0 gap-4">
      <a v-if="!isRootPath" class="btn btn-ghost btn-circle text-xl" href="/" title="Zu den Gesetzen">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
          <!-- Icon from Google Material Icons by Material Design Authors - https://github.com/material-icons/material-icons/blob/master/LICENSE -->
          <path fill="currentColor" d="M17.77 3.77L16 2L6 12l10 10l1.77-1.77L9.54 12z" />
        </svg>
      </a>
      <LawSearch class="pl-16 flex-1 justify-self-center self-center" />
    </div>
  </div>
</template>
