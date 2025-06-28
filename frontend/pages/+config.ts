import vikeVue from "vike-vue/config";
import vikeVueQuery from "vike-vue-query/config";
import type { Config } from "vike/types";
import Layout from "../layouts/LayoutDefault.vue";

// Default config (can be overridden by pages)
// https://vike.dev/config

export default {
  // https://vike.dev/Layout
  Layout,

  // https://vike.dev/head-tags
  title: "German Law Diff",
  description: "Show differences between versions of German laws",

  extends: [vikeVue as typeof vikeVue, vikeVueQuery as typeof vikeVueQuery],
} satisfies Config;
