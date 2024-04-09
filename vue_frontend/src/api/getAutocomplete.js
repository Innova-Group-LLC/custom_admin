import request from '@/utils/request'
import { getToken } from '@/utils/auth'
import { config_dataset } from '@/utils/settings'

const completeUrl = config_dataset.backend_prefix + 'autocompete/'


export async function getAutocomplete(
  model_name,
  app_label,
  search_string,
  limit,
  viewname,
  field_slug,
  form_data,
  existed_choices,
) {
  if (!getToken()) return

  let newFormData = {}
  for (const [field_name, field_value] of Object.entries(form_data || {})) {
    if (field_value !== null && field_value !== undefined) {
      if (typeof field_value !== 'string' || field_value.length < 1000) {
        newFormData[field_name] = field_value
      }
    }
  }

  return await new Promise((resolve, reject) => {
    request({
      url: completeUrl,
      method: 'post',
      data: {
        model_name: model_name,
        app_label: app_label,
        search_string: search_string,
        limit: limit,
        viewname: viewname,
        field_slug: field_slug,
        form_data: newFormData,
        existed_choices: existed_choices,
      },
    }).then(response => {
      if (response.data === undefined)
        reject('response.data is undefined')

      resolve(response.data)
    }).catch(error => {
      reject(error)
    })
  })
}
