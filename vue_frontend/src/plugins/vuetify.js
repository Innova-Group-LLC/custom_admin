import { useI18n } from 'vue-i18n'
import { createVueI18nAdapter } from 'vuetify/locale/adapters/vue-i18n'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import i18n from './i18n'
import { getSettings } from '/src/utils/settings'
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: getSettings().theme || 'light',
  },
  locale: {
    adapter: createVueI18nAdapter({ i18n, useI18n }),
  },
  defaults: {
    global: {
      ripple: false,
      density: 'compact',
      hideDetails: 'auto',
    },
    VList: {
      density: 'default',
    },
    VTabs: {
      density: 'default',
    },
    VDataTable: {
      density: 'default',
    },
    VBtn: {
      density: 'default',
    },
  },
})
