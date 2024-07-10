import Cookies from 'js-cookie'

var config_dataset = {
  title: 'Dev Admin',
  logo_image: `${import.meta.env.VITE_APP_URL_PREFIX}/static/img/admin-logo.svg`,
  backend_prefix: `${import.meta.env.VITE_APP_URL_PREFIX}/custom_admin/`,
  static_prefix: '/static/custom_admin',
  version: '-',
}

if (import.meta.env.PROD) {
  config_dataset = JSON.parse(document.getElementById("settings").dataset.json)
  config_dataset.static_prefix = '/static/custom_admin'
}

export var config_dataset
console.log('config_dataset', config_dataset, 'prod', import.meta.env.PROD)

const SETTINGS_COOKIE_NAME = 'SETTINGS'
const VIEWSETS_SETTINGS = 'VIEWSETS_SETTINGS'

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

export function getViewsetsSettings(viewname, serializer) {
  let settings = localStorage.getItem(`${VIEWSETS_SETTINGS}_${viewname}`, { sameSite:'strict' })
  settings = settings ? JSON.parse(settings) : {headers: {}}

  for (const [field_slug, field] of Object.entries(serializer)) {
    if (settings.headers[field_slug] === undefined) {
      settings.headers[field_slug] = true
    }
  }
  return settings
}

export function setViesetsSettings(viewname, settings) {
  localStorage.setItem(`${VIEWSETS_SETTINGS}_${viewname}`, JSON.stringify(settings), { sameSite:'strict' })
}

export const tinyMCEThemes = [
  'lightgray',
  'dark-first',
  'dark-slim',
]

export function getTinyMCETheme() {
  let settings = getSettings()
  if (tinyMCEThemes.indexOf(settings.tinyMCETheme) !== -1) return settings.tinyMCETheme
  return tinyMCEThemes[0]
}
