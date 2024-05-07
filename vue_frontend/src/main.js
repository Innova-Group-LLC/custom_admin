import { createApp } from 'vue'

import App from './App.vue'
const app = createApp(App)

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
app.use(ElementPlus)

import router from './router'
app.use(router)

import i18n from './lang'
app.use(i18n)

app.mount('#app')
