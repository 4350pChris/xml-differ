import vikeVue from "vike-vue/config";
import vikeVueQuery from "vike-vue-query/config";
import vikeServer from "vike-server/config";
import Layout from "../layouts/LayoutDefault.vue";
import { Config } from "vike/types";

// Default config (can be overridden by pages)
// https://vike.dev/config

export default {
  // https://vike.dev/Layout
  Layout,

  // https://vike.dev/head-tags
  title: "German Law Diff",
  description: "Show differences between versions of German laws",

  lang: "de",

  passToClient: ["apiUrl"],

  extends: [vikeVue, vikeVueQuery, vikeServer],

  server: "./server/h3-entry.ts",

  meta: {
    apiUrl: {
      env: {
        server: true,
        client: false,
      },
    },
  },
} satisfies Config;

declare global {
  namespace Vike {
    interface PageContext {
      apiUrl: string;
    }

    interface Config {
      apiUrl?: string;
    }
  }
}
