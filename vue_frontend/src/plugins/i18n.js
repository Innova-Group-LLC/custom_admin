import { createI18n } from 'vue-i18n'
import { en, ru, cs, tr } from 'vuetify/locale'

import { getLang } from '/src/utils/auth'

const messages = {
  en: {
    notFoundPageHeadline: 'Page not found',
    notFoundPageTitle: 'The page you were looking for does not exist',
    notFoundPageGoBack: 'Go back to Dashboard',
    yes: 'Yes',
    no: 'No',
    mainPage: 'Main page',
    login: 'Login',
    languageSelection: 'Language selection',
    itemsPerPage: 'Items per page:',
    applyToAllRecords: 'Apply to all finded records. In total:',
    actionNotAllowEmptySelection: 'At least one record must be selected to perform this action!',
    fixErrors: 'Fix the errors',
    modelUpdated: 'Record {id} updated',
    modelCreated: 'Record {id} created',
    confirmation: 'Confirmation',
    confirm: 'Confirm',
    send: 'Send',
    update: 'Update',
    cancel: 'Cancel',
    selected: 'Selected:',
    create: 'Create',
    apply: 'Apply',
    close: 'Close',
    search: 'Search',
    creation: 'Creation',
    general: 'General',
    inputStringForSearch: 'Enter a search string',
    themeSelection: 'Theme selection',
    tinyMCETheme: 'Text editor theme',
    $vuetify: {
      ...en,
      dataIterator: {
        loadingText: 'Loading...',
      },
    },
  },
  ru: {
    notFoundPageHeadline: 'Страница не найдена',
    notFoundPageTitle: 'Страница, которую вы искали, не существует',
    notFoundPageGoBack: 'Вернуться на главную страницу',
    yes: 'Да',
    no: 'Нет',
    mainPage: 'Главная',
    login: 'Вход',
    languageSelection: 'Выбор языка',
    itemsPerPage: 'Записей на странице:',
    applyToAllRecords: 'Применить для всех найденных записей. Всего:',
    actionNotAllowEmptySelection: 'Для выполнения данного действия необходимо выбрать хотябы одну запись!',
    fixErrors: 'Исправьте ошибки',
    modelUpdated: 'Запись {id} обновлена',
    modelCreated: 'Запись {id} создана',
    confirmation: 'Подтверждение',
    confirm: 'Подтвердить',
    send: 'Отправить',
    update: 'Обновить',
    cancel: 'Отменить',
    selected: 'Выбрано:',
    create: 'Создать',
    search: 'Поиск',
    apply: 'Применить',
    close: 'Закрыть',
    creation: 'Создание',
    general: 'Основное',
    inputStringForSearch: 'Введите строку для поиска',
    themeSelection: 'Выбор темы',
    tinyMCETheme: 'Тема редактора текста',
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
