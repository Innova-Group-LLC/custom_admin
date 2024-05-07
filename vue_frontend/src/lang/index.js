import Vue from 'vue'
import VueI18n from 'vue-i18n'

import enLocale from './en'
import ruLocale from './ru'
import { getLang } from './utils/auth'

Vue.use(VueI18n)

const messages = {
  en: {
    ...enLocale,
  },
  ru: {
    ...ruLocale,
  },
}

const i18n = new VueI18n({
  locale: getLang(),
  messages
})

export default i18n
