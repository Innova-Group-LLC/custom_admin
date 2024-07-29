import { toast } from "vue3-toastify"
import { getLang } from '/src/utils/auth'
import moment from 'moment'

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

export async function sendAction(kwargs) {
  return new Promise((resolve, reject) => {
    console.log(`Send action "${kwargs.action}"`, kwargs.pks, kwargs.sendToAll, kwargs.formData)

    let url = `${config_dataset.backend_prefix}${kwargs.viewname}/send_action/${kwargs.action}/`

    if (kwargs.filter_info) {
      const filter_info = encodeURIComponent(JSON.stringify(kwargs.filter_info))
      url = `${url}?filter_info=${filter_info}`
    }

    request({
      url: url,
      method: 'post',
      data: {
        pks: kwargs.pks,
        form_data: kwargs.formData,

        send_to_all: kwargs.sendToAll,
        relfilter: kwargs.relationNameFilter,
        relfilterid: kwargs.relfilterid,
      },
      headers: {
        'Accept-Language': getLang(),
      },
    }).then(response => {
      resolve(response)
    }).catch(error => {
      if (error.response) {
        if (error.response.status == 400) {

          if (error.response.data.action_messages) {
            toast(error.response.data.action_messages.join('<br>'), {
              "type": "error",
              "position": "top-center",
              "dangerouslyHTMLString": true
            })
          }
          reject(error.response)
        }
        else if (error.response.status == 500) {
          toast(`Error! Code: ${error.response.status}</br>Text: ${error.response.data}`, {
            "type": "error",
            "position": "top-center",
            "dangerouslyHTMLString": true
          })
          reject(null)
        }
      }
    })
  })
}
