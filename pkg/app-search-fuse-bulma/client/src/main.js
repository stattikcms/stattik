import { createApp } from 'vue'
import App from './App.vue'

import Oruga from '@oruga-ui/oruga-next'
import { bulmaConfig } from '@oruga-ui/theme-bulma'

createApp(App)
  .use(Oruga, bulmaConfig)
  .mount('#app')
