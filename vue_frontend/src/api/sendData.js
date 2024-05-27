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

    for (const [fieldName, _field] of Object.entries(formData)) {
      if (_field instanceof Date) field = moment(_field).format('YYYY-MM-DDTHH:mm')
    }

    request({
      url: fillUrl,
      method: method,
      data: formData,
      headers: {
        'Accept-Language': getLang(),
      },
      timeout: 1000 * 5,
    }).then(response => resolve(response.data)).catch(error => reject(error))
  })
}
