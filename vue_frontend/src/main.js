import { registerPlugins } from '@/plugins'
import App from './App.vue'
import { createApp } from 'vue'

import '/src/styles/index.scss'

const app = createApp(App)
registerPlugins(app)
app.mount('#app')
