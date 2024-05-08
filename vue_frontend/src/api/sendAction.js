import { ElMessage } from 'element-plus'
import moment from 'moment';

import request from '/src/utils/request'
import { config_dataset } from '/src/utils/settings'


export function downloadContent(data, fileName, type) {
  const eElelent = document.createEvent('MouseEvents')
  const aElement = document.createElement('a')
  aElement.download = fileName
  const blob = new Blob([data], {type: type})
  aElement.href = window.URL.createObjectURL(blob)
  aElement.dataset.downloadurl = [type, aElement.download, aElement.href].join(':')
  eElelent.initEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
  aElement.dispatchEvent(eElelent)
}

export async function sendAction(viewname, action, ids, sendToAll, formData) {
  return new Promise((resolve, reject) => {
    console.log('Send action', action, ids, sendToAll, formData)

    const url = `${config_dataset.backend_prefix}${viewname}/send_action/`
    request({
      url: url,
      method: 'post',
      data: {
        action: action,
        ids: ids,
        send_to_all: sendToAll,
        form_data: formData,
      },
      headers: {
        // 'Content-Type': 'multipart/form-data'
      }
    }).then(response => {
      if(response.headers['content-type'] === 'text/csv') {
        const fileName = response.headers['pragma'] || `${moment().format('DD.MM.YYYY_HH:MM')}.csv`
        downloadContent(
          response.data, fileName, response.headers['content-type']
        )
      }
      else {
        ElMessage({ message: response.data.action_messages.join('<br>'), type: 'success', duration: 5 * 1000 , dangerouslyUseHTMLString: true,})
      }
      resolve(response)
    }).catch(error => {
      if (error.response) {
        if (error.response.status == 400) {

          if (error.response.data.action_messages) {
            ElMessage({ message: error.response.data.action_messages.join('<br>'), type: 'error', duration: 5 * 1000 , dangerouslyUseHTMLString: true,})
          }
          reject(error.response.data)
        }
        else if (error.response.status == 500) {
          ElMessage({ message: `Error; Status code: ${error.response.status}`, type: 'error', duration: 5 * 1000 })
          reject(null)
        }
      }
    })
  })
}
