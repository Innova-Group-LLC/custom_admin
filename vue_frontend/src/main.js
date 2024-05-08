import { createApp } from 'vue'

import './style.css'
import App from './App.vue'
const app = createApp(App)

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
app.use(ElementPlus)

import router from './router'
app.use(router)

app.mount('#app')
