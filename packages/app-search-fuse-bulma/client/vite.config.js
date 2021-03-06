import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import path from 'path'

const root = path.resolve(__dirname, '../../../stattik-theme-bulma')
const publicDir = path.resolve(root, './dist')
const outDir = path.resolve(__dirname, '../../stattik_app_search_fuse/bulma/static/search')

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  if (command === 'serve') {
    return {
      plugins: [vue()],
      publicDir,
    }
  } else {
    // command === 'build'
    return {
      plugins: [vue()],
      build: {
        outDir,
        lib: {
          entry: path.resolve(__dirname, 'src/main.js'),
          name: 'main',
          //fileName: (format) => `my-lib.${format}.js`
          fileName: (format) => `main.js`
        },
      },
    }
  }
})