import moment from 'moment';
import { getLang } from '/src/utils/auth'

import request from '/src/utils/request'

export async function sendData(url, method, formData, relationNameFilter, filterId) {
  return new Promise((resolve, reject) => {
    let urlsParams = {}
    
    if (relationNameFilter) {
      urlsParams.relfilter = relationNameFilter
      urlsParams.relfilterid = filterId
    }
    
    let params = new URLSearchParams(urlsParams)
    const fillUrl = `${url}?${params}`

    for (const [fieldName, field] of Object.entries(formData)) {
      if (field instanceof Date) field = moment(field).format('YYYY-MM-DDTHH:mm')
    }

    request({
      url: fillUrl,
      method: method,
      data: formData,
      headers: {
        'Accept-Language': getLang(),
      }
    }).then(response => resolve(response.data)).catch(error => reject(error))
  })
}
