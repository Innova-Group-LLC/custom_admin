import { useI18n } from 'vue-i18n'
import { createVueI18nAdapter } from 'vuetify/locale/adapters/vue-i18n'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import i18n from './i18n'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'light',
  },
  locale: {
    adapter: createVueI18nAdapter({ i18n, useI18n }),
  },
})
