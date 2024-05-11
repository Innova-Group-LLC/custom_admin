import { registerPlugins } from '@/plugins'
import App from './App.vue'
import { createApp } from 'vue'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

import '/src/styles/index.scss'

import List from '/src/views/List.vue'
import ModelForm from '/src/components/ModelForm.vue'

const app = createApp(App)
registerPlugins(app)
app.component('List', List)
app.component('ModelForm', ModelForm)
app.mount('#app')
