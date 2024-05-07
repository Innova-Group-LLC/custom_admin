import Vue from 'vue'
import Router from 'vue-router'
import i18n from '../lang'
import { config_dataset } from '@/utils/settings'

Vue.use(Router)

import Layout from '@/layout'

export const constantRoutes = [
  {
    path: '/',
    redirect: '/dashboard',
    meta: {title: i18n.t('main_page')},
    component: () => import('@/layout')
  },
  {
    path: '/login',
    component: () => import('@/views/login')
  },
  {
    path: '/404',
    component: () => import('@/views/404')
  },
  {
    path: '',
    component: Layout,
    children: [
      {
        path: 'dashboard',
        props: true,
        meta: {title: i18n.t('main_page')},
        component: () => import('@/views/dashboard')
      },
      {
        path: ':group/:viewname/list', props: true,
        name: 'list',
        component: () => import('@/views/list')
      },
      {
        path: ':group/:viewname/:id/:mode', props: true,
        name: 'edit',
        component: () => import('@/views/edit')
      },
      {
        path: ':group/:viewname/:mode', props: true,
        name: 'create',
        component: () => import('@/views/edit')
      }
    ]
  },

  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  base: config_dataset.base_admin_url,
  mode: 'history',
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher
}

export default router
