import Cookies from 'js-cookie'

const TokenKey = 'vadmin_token'
const TokenRefreshKey = 'vadmin_refresh_token'

const LANGUAGE_COOKIE_NAME = process.env.VUE_APP_LANGUAGE_COOKIE_NAME || 'LANGUAGE'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token, refresh_token) {
  Cookies.set(TokenKey, token)
  Cookies.set(TokenRefreshKey, refresh_token)
}

export function removeToken() {
  Cookies.remove(TokenKey)
  Cookies.remove(TokenRefreshKey)
}

export function getLang() {
  let lang = Cookies.get(LANGUAGE_COOKIE_NAME, { sameSite:'strict' }) || 'ru'
  return lang
}

export function setLang(langSlug) {
  Cookies.set(LANGUAGE_COOKIE_NAME, langSlug, { sameSite:'strict' })
}
