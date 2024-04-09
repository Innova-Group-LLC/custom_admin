import Cookies from 'js-cookie'

var config_dataset = {
  title: 'Dev Admin',
  backend_prefix: process.env.VUE_APP_URL_PREFIX || 'http://localhost:8001/custom_admin/',
  base_admin_url: 'admin/',
  static_prefix: '',
}

if (process.env.NODE_ENV == 'production') {
  config_dataset = JSON.parse(document.getElementById("settings").dataset.json)
}

export var config_dataset
console.log('config_dataset', config_dataset, 'env', process.env.NODE_ENV)

const SETTINGS_COOKIE_NAME = 'SETTINGS'

export const wysiwygTypes = {
  'dark-first': 'Dark Blue',
  'dark-slim': 'Dark Slim',
  'lightgray': 'Light Gray',
}

const defaultSettings = {
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
