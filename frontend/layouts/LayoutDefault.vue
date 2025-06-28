<template>
  <div class="bg-base-100 mx-auto max-w-[100rem] drawer">
    <input id="drawer" type="checkbox" class="drawer-toggle" />
    <Content><slot /></Content>
    <Sidebar>
      <ul class="menu w-full rounded-box px-2">
        <li>
          <Link v-for="law in data.laws" :key="law.id" :href="`/law/${law.id}`">
            {{ law.name }}
          </Link>
        </li>
      </ul>
    </Sidebar>
  </div>
</template>

<script lang="ts" setup>
import Content from "../components/Content.vue";
import Link from "../components/Link.vue";
import Sidebar from "../components/Sidebar.vue";
import {useData} from "vike-vue/useData";
import {Data} from "../pages/+data";
import {ref} from "vue";

const data = useData<Data>();
</script>

<style>
/* see https://stackoverflow.com/questions/55206901/how-to-import-css-files-in-vue-3-child-components */
@import "./tailwind.css";

body {
  margin: 0;
  font-family: sans-serif;
}
* {
  box-sizing: border-box;
}
</style>
