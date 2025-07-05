<script setup lang="ts">
const split = defineModel<boolean>({ required: true });
</script>

<template>
  <fieldset class="fieldset">
    <legend class="fieldset-legend text-lg">Diff Ansicht</legend>
    <label class="swap swap-active *:w-full">
      <input v-model="split" type="checkbox" aria-label="Zwischen Seite bei Seite und vereinigtem Diff wechseln" />

      <svg
        aria-label="Seite bei Seite Diff"
        :class="split ? 'swap-on' : 'swap-off'"
        xmlns="http://www.w3.org/2000/svg"
        width="32"
        height="32"
        viewBox="0 0 24 24"
      >
        <!-- Icon from Material Design Icons by Pictogrammers - https://github.com/Templarian/MaterialDesign/blob/master/LICENSE -->
        <path
          fill="currentColor"
          d="M10 18H6v-2h4zm0-4H6v-2h4zm0-13v1H6c-1.11 0-2 .89-2 2v16a2 2 0 0 0 2 2h4v1h2V1zm10 7v12c0 1.11-.89 2-2 2h-4v-2h4v-9h-4V9h4.5L14 4.5V2zm-4 6h-2v-2h2zm0 4h-2v-2h2z"
        />
      </svg>

      <span
        :class="split ? 'swap-off' : 'swap-on'"
        class="flex items-center justify-center"
        aria-label="Vereinigtes Diff"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
          <!-- Icon from Material Design Icons by Pictogrammers - https://github.com/Templarian/MaterialDesign/blob/master/LICENSE -->
          <path
            fill="currentColor"
            d="M22.54 21.12L20.41 19l2.13-2.12l-1.42-1.42L19 17.59l-2.12-2.13l-1.42 1.42L17.59 19l-2.13 2.12l1.42 1.42L19 20.41l2.12 2.13M6 2a2 2 0 0 0-2 2v16c0 1.11.89 2 2 2h7.81c-.36-.62-.61-1.3-.73-2H6V4h7v5h5v4.08c.33-.05.67-.08 1-.08c.34 0 .67.03 1 .08V8l-6-6M8 12v2h8v-2m-8 4v2h5v-2Z"
          />
        </svg>

        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
          <!-- Icon from Material Design Icons by Pictogrammers - https://github.com/Templarian/MaterialDesign/blob/master/LICENSE -->
          <path
            fill="currentColor"
            d="M23 18h-3v-3h-2v3h-3v2h3v3h2v-3h3M6 2a2 2 0 0 0-2 2v16c0 1.11.89 2 2 2h7.81c-.36-.62-.61-1.3-.73-2H6V4h7v5h5v4.08c.33-.05.67-.08 1-.08c.34 0 .67.03 1 .08V8l-6-6M8 12v2h8v-2m-8 4v2h5v-2Z"
          />
        </svg>
      </span>
    </label>
  </fieldset>
</template>
