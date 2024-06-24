import { registerPlugins } from '@/plugins'
import App from './App.vue'
import { createApp } from 'vue'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import { JsonForms } from "@jsonforms/vue"

import '/src/styles/index.scss'
import '@vuepic/vue-datepicker/dist/main.css';

import '@jsonforms/vue-vanilla/vanilla.css';

const app = createApp(App)
app.component('JsonForms', JsonForms)

import List from '/src/views/List.vue'
import Edit from '/src/views/Edit.vue'
app.component('List', List)
app.component('Edit', Edit)

registerPlugins(app)

import mitt from 'mitt';
const emitter = mitt();
app.config.globalProperties.emitter = emitter;

app.mount('#app')
