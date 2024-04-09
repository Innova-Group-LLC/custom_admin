import request from '@/utils/request'


export function getDetail(url, method, sectionData) {
  return new Promise((resolve, reject) => {
    request({
      url: url, method: method
    }).then(response => {
      resolve(response.data)
    }).catch(error => reject(error))
  })
}
