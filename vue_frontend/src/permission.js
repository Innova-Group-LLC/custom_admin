import router from './router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { getToken } from '@/utils/auth'
import getPageTitle from '@/utils/get-page-title'

NProgress.configure({ showSpinner: false })

const whiteList = ['/login']

router.beforeEach(async(to, from, next) => {
  NProgress.start()

  document.title = getPageTitle(to.meta.title)

  if (getToken()) {
    if (to.path === '/login') {
      return next({ path: '/' })
    }
    return next()
  } else {
    if (whiteList.indexOf(to.path) !== -1) {
      return next()
    }
    return next(`/login?redirect=${to.path}`)
  }
})

router.afterEach(() => {
  NProgress.done()
})
