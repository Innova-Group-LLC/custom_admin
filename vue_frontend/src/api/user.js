import request from '@/utils/request'
import Cookies from 'js-cookie'
import { setToken, removeToken, setLang } from '@/utils/auth'
import { config_dataset } from '@/utils/settings'

const loginUrl = config_dataset.backend_prefix + 'token-auth/'

function loginApi(data) {
  var post_data = {
    'username': data.username,
    'password': data.password,
    'phone': ''
  }
  return request({
    url: loginUrl,
    method: 'post',
    data: post_data
  })
}

export function login(userInfo) {
  console.assert(config_dataset.backend_prefix, 'backend url is not set!')

  const { username, password } = userInfo
  return new Promise((resolve, reject) => {
    loginApi(
      { username: username.trim(), password: password }
    ).then(response => {
      setToken(response.data.access, response.data.refresh)
      console.log('access_expiration', response.data.access_expiration)

      localStorage.setItem('name', response.data.user.username)
      localStorage.setItem('user_id', response.data.user.pk)
      setLang(response.data.user.language)
      resolve()
    }).catch(error => {
      reject(error)
    })
  })
}

export function resetToken() {
  return new Promise(resolve => {
    removeToken()
    resolve()
  })
}
