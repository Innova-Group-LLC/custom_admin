import { createMemoryHistory, createRouter } from 'vue-router'

import Layout from './layout/index.vue'
import i18n from './lang'
import { config_dataset } from './utils/settings'

export const routes = [
  {
    path: '/',
    redirect: '/dashboard',
    meta: {title: i18n.t('main_page')},
    component: () => import('./layout/index.vue')
  },
  {
    path: '/login',
    component: () => import('./views/login.vue')
  },
  {
    path: '/404',
    component: () => import('./views/404.vue')
  },
  {
    path: '',
    component: Layout,
    children: [
      {
        path: 'dashboard',
        props: true,
        meta: {title: i18n.t('main_page')},
        component: () => import('./views/dashboard.vue')
      },
      {
        path: ':group/:viewname/list', props: true,
        name: 'list',
        component: () => import('./views/list.vue')
      },
      {
        path: ':group/:viewname/:id/:mode', props: true,
        name: 'edit',
        component: () => import('./views/edit.vue')
      },
      {
        path: ':group/:viewname/:mode', props: true,
        name: 'create',
        component: () => import('./views/edit.vue')
      }
    ]
  },

  { path: '*', redirect: '/404', hidden: true }
]

const router = createRouter({
  base: config_dataset.base_admin_url,
  history: createMemoryHistory(),
  routes,
})

export default router
