import Vue from 'vue'
import checkView from 'vue-check-view'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import i18n from './lang'

import 'element-ui/lib/theme-chalk/index.css'
import '@/styles/index.scss'

import App from './App'
import router from './router'

import '@/icons'
import '@/permission'

Vue.use(ElementUI, {
  i18n: (key, value) => i18n.t(key, value)
})
Vue.use(checkView)

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  i18n,
  render: h => h(App)
})
