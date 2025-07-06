import md from "unplugin-vue-markdown/vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";
import vike from "vike/plugin";
import path from "node:path";
import Unfonts from "unplugin-fonts/vite";

export default defineConfig({
  plugins: [
    vike({}),
    tailwindcss(),
    vue({
      include: [/\.vue$/, /\.md$/],
    }),
    md({}),
    vueDevTools({
      launchEditor: "webstorm",
    }),
    Unfonts({
      fontsource: {
        families: ["Inter Variable"],
      },
    }),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    target: "es2022",
  },
});
