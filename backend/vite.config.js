import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import { resolve } from "path";

export default defineConfig({
  server: {
    host: "localhost",
    port: 5173,
    hmr: {
      host: "localhost",
      port: 5173,
    },
    cors: true,
  },

  build: {
    manifest: true,
    rollupOptions: {
      // input: resolve(__dirname, "static/js/main.js"), // this is old
      // input: resolve(import.meta.dirname, "static/js/main.js"), // this is modern
      input: {
        main: resolve(import.meta.dirname, "static/js/main.js"),
        style: resolve(import.meta.dirname, "static/css/style.css"),
      },
      output: {
        entryFileNames: `js/[name]-bundle.js`,
        assetFileNames: `css/[name].css`,
      },
    },

    // outDir: resolve(__dirname, "static/dist"),
    outDir: resolve(import.meta.dirname, "static/dist"),
    emptyOutDir: true,
  },

  plugins: [
    tailwindcss()
  ],

});
