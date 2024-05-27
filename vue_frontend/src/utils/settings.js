import Cookies from 'js-cookie'

var config_dataset = {
  title: 'Dev Admin',
  backend_prefix: import.meta.env.VITE_APP_URL_PREFIX,
  static_prefix: '/static/custom_admin',
}

if (import.meta.env.PROD) {
  config_dataset = JSON.parse(document.getElementById("settings").dataset.json)
  config_dataset.static_prefix = '/static/custom_admin'
}

export var config_dataset
console.log('config_dataset', config_dataset, 'prod', import.meta.env.PROD)

const SETTINGS_COOKIE_NAME = 'SETTINGS'

export const wysiwygTypes = {
  'dark-first': 'Dark Blue',
  'dark-slim': 'Dark Slim',
  'lightgray': 'Light Gray',
}

const defaultSettings = {
  page_size: 25,
  theme: 'light',
  wysiwygSkin: 'dark-first',
}

export function getSettings() {
  const settings = Cookies.get(SETTINGS_COOKIE_NAME, { sameSite:'strict' })
  if (settings == null) {
    return defaultSettings
  }
  return JSON.parse(settings)
}

export function setSettings(settings) {
  Cookies.set(SETTINGS_COOKIE_NAME, JSON.stringify(settings), { sameSite:'strict' })
}
