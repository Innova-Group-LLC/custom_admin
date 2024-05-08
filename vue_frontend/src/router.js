import { createMemoryHistory, createRouter } from 'vue-router'
import { config_dataset } from '/src/utils/settings'

import Layout from '/src/layout/Layout.vue'
import Dashboard from '/src/views/Dashboard.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '',
    component: Layout,
    children: [
      {
        path: 'dashboard',
        props: true,
        component: Dashboard,
      },
    ]
  },

  { path: '/:pathMatch(.*)*', redirect: '/404', hidden: true }
]

const router = createRouter({
  base: config_dataset.base_admin_url,
  history: createMemoryHistory(),
  routes,
})

export default router
