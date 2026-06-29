import { defineConfig } from 'vite';
import { resolve } from 'path';
import { viteStaticCopy } from 'vite-plugin-static-copy';

export default defineConfig({
  base: './',
  root: '.',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        methods: resolve(__dirname, 'methods.html'),
        notfound: resolve(__dirname, '404.html')
      }
    }
  },
  plugins: [
    viteStaticCopy({
      targets: [
        {
          src: 'data/*',
          dest: 'data'
        },
        {
          src: 'assets/*',
          dest: 'assets'
        },
        {
          src: '_headers',
          dest: '.'
        },
        {
          src: '_redirects',
          dest: '.'
        },
        {
          src: 'robots.txt',
          dest: '.'
        },
        {
          src: 'sitemap.xml',
          dest: '.'
        },
        {
          src: 'site.webmanifest',
          dest: '.'
        }
      ]
    })
  ]
});
