import { defineConfig } from 'vite';

/** Serves static multi-page HTML/CSS from the repo root (see index.html). */
export default defineConfig({
  root: '.',
  appType: 'mpa',
  server: {
    port: 5173,
    strictPort: false,
  },
});
