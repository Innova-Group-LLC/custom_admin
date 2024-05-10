import { createI18n } from 'vue-i18n'
import { en, ru, cs, tr } from 'vuetify/locale'

import { getLang } from '/src/utils/auth'

const messages = {
  en: {
    mainPage: 'Main page',
    languageSelection: 'Language selection',
    $vuetify: {
      ...en,
      dataIterator: {
        loadingText: 'Loading...',
      },
    },
  },
  ru: {
    mainPage: 'Главная',
    languageSelection: 'Выбор языка',
    $vuetify: {
      ...ru,
      dataIterator: {
        loadingText: 'Загрузка...',
      },
    },
  },
  cs: {
    mainPage: 'Hlavní stránka',
    languageSelection: 'Výběr jazyka',
    $vuetify: {
      ...cs,
      dataIterator: {
        loadingText: 'Načítání...',
      },
    },
  },
  tr: {
    mainPage: 'Hlavní stránka',
    languageSelection: 'Dil seçimi',
    $vuetify: {
      ...cs,
      dataIterator: {
        loadingText: 'Ana sayfa...',
      },
    },
  },
}

export default createI18n({
  legacy: false,
  locale: getLang(),
  fallbackLocale: 'en',
  messages,
})
