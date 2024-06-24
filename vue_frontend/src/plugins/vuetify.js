import { useI18n } from 'vue-i18n'
import { createVueI18nAdapter } from 'vuetify/locale/adapters/vue-i18n'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import i18n from './i18n'
import { getSettings } from '/src/utils/settings'
import { createVuetify } from 'vuetify'

export const themes = [
  'blueLight', 'blueDark', 'greenLight', 'greenDark', 'deepPurpleLight', 'deepPurpleDark'
]

function getTheme() {
    const theme = getSettings().theme
    if (themes.indexOf(theme) !== -1) return theme
    return themes[0]
}

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
// https://www.w3schools.com/colors/colors_picker.asp

const greenLight = {
  dark: false,
  colors: {
    light2: '#b5e3d1',
    light3: '#91eeca',
    secondary: '#187f58', // light-4

    darken1: '#4fe3aa',
    primary: '#0c4b33', // darken-2
    darken3: 'rgb(10, 66, 45)',
    darken4: 'rgb(4, 59, 39)',

    accent: '#B9F6CA',
    error: '#AA4A44',

    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107',
  }
}
const greenDark = {
  dark: true,
  colors: {
    surface: '#1a1d1e',

    light2: '#22594a',
    light3: '#91eeca',
    secondary: '#187f58', // light-4

    darken1: '#4fe3aa',
    primary: '#0c4b33', // darken-2
    darken3: 'rgb(10, 66, 45)',
    darken4: 'rgb(4, 59, 39)',

    accent: '#B9F6CA',
    error: '#AA4A44',

    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107',
  }
}
const blueLight = {
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
}
const blueDark = {
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
}
const deepPurpleLight = {
  dark: false,
  colors: {
    light2: '#D1C4E9',
    light3: '#B39DDB',
    secondary: '#9575CD', // light-4

    darken1: '#5E35B1',
    primary: '#7E57C2', // darken-2
    darken3: '#512DA8',
    darken4: '#4527A0',

    accent: '#B388FF',
    error: '#AA4A44',

    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107',
  }
}
const deepPurpleDark = {
  dark: true,
  colors: {
    surface: '#1a1d1e',

    light2: '#34383a',
    light3: '#B39DDB',
    secondary: '#4e3084', // light-4

    darken1: '#5E35B1',
    primary: '#5a3798', // darken-2
    darken3: '#512DA8',
    darken4: '#4527A0',

    accent: '#B388FF',
    error: '#AA4A44',

    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107',
  }
}

export default createVuetify({
  theme: {
    defaultTheme: getTheme(),
    themes: {
      blueLight,
      blueDark,
      greenLight,
      greenDark,
      deepPurpleLight,
      deepPurpleDark,
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
