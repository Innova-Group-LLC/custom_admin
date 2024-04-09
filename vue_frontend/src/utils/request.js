import axios from 'axios'
import { Message } from 'element-ui'
import { getToken, removeToken } from '@/utils/auth'
import { config_dataset } from '@/utils/settings'

const service = axios.create({
  baseURL: config_dataset.backend_prefix,
  timeout: null,
})

service.interceptors.request.use(
  config => {
    let token = getToken()
    if (token !== null && token !== undefined) {
      let authorization_prefix = process.env.VUE_APP_AUTHORIZATION_PREFIX || 'Bearer'
      config.headers['Authorization'] = authorization_prefix + ' ' + token
    }
    config.headers['Accept'] = 'application/json'
    return config
  },
  error => {
    console.error('Config error: ' + error)
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response && error.response.status === 403) removeToken()
    return Promise.reject(error)
  }
)

export default service
