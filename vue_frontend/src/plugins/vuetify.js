import { useI18n } from 'vue-i18n'
import { createVueI18nAdapter } from 'vuetify/locale/adapters/vue-i18n'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import i18n from './i18n'
import { getSettings } from '/src/utils/settings'
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
// https://www.w3schools.com/colors/colors_picker.asp
export default createVuetify({
  theme: {
    defaultTheme: getSettings().theme || 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          light2: '#eff2f6',
          light3: '#dee5ed',
          secondary: '#bdcbdb', // light-4

          darken1: '#9db0c8',
          primary: '#5c7ca3', // darken-2
          darken3: '#304156',
          darken4: '#1f2d3d',

          accent: '#82B1FF',
          error: '#AA4A44',

          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
        }
      },
      dark: {
        dark: true,
        colors: {
          surface: 'rgb(28, 30, 31)',

          light2: '#1f2223',
          light3: '#dee5ed',
          secondary: '#283749', // light-4

          darken1: '#9db0c8',
          primary: '#5c7ca3', // darken-2
          darken3: '#304156',
          darken4: '#1f2d3d',

          accent: '#82B1FF',
          error: '#AA4A44',

          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
        }
      },
    },
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
