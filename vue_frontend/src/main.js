import { registerPlugins } from '@/plugins'
import App from './App.vue'
import { createApp } from 'vue'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import { JsonForms } from "@jsonforms/vue"

import '/src/styles/index.scss'

const app = createApp(App)
app.component('JsonForms', JsonForms)
registerPlugins(app)
app.mount('#app')
