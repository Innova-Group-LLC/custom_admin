import axios from 'axios'

import { getToken, removeToken } from '/src/utils/auth'
import { config_dataset } from '/src/utils/settings'

const service = axios.create({
  baseURL: config_dataset.backend_prefix,
  timeout: null,
})

service.interceptors.request.use(
  config => {
    let token = getToken()
    if (token !== null && token !== undefined) {
      config.headers['Authorization'] = config_dataset.auth_header_prefix + ' ' + token
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
