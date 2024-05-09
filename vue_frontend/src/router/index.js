import { createRouter, createWebHistory } from 'vue-router'
import { config_dataset } from '/src/utils/settings'

import Layout from '/src/layout/Layout.vue'
import Dashboard from '/src/views/Dashboard.vue'
import List from '/src/views/List.vue'
import Edit from '/src/views/List.vue'

const routes = [
  {
    path: '',
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
      {
        path: ':group/:viewname/list',
        props: true,
        name: 'list',
        component: List,
      },
      {
        path: ':group/:viewname/:id/:mode',
        props: true,
        name: 'edit',
        component: Edit,
      },
      {
        path: ':group/:viewname/:mode',
        props: true,
        name: 'create',
        component: Edit,
      }
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/404', hidden: true }
]

export default createRouter({
  history: createWebHistory(config_dataset.base_admin_url),
  routes,
})
