import { createMemoryHistory, createRouter } from 'vue-router'

import Dashboard from './views/Dashboard.vue'

const routes = [
  { path: '/', component: Dashboard },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router
