import vuetify from './vuetify'
import i18n from './i18n'

import router from '@/router'

export function registerPlugins (app) {
  app
    .use(vuetify)
    .use(router)
    .use(i18n)
}
