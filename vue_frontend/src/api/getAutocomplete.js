import request from '/src/utils/request'
import { getToken } from '/src/utils/auth'
import { config_dataset } from '/src/utils/settings'
import { getLang } from '/src/utils/auth'

export async function getAutocomplete(autocompleteInfo) {
  if (!getToken()) return

  let newFormData = {}
  for (const [field_name, field_value] of Object.entries(autocompleteInfo.form_data || {})) {
    if (field_value !== null && field_value !== undefined) {
      if (typeof field_value !== 'string' || field_value.length < 1000) {
        newFormData[field_name] = field_value
      }
    }
  }

  return await new Promise((resolve, reject) => {
    const url = `${config_dataset.backend_prefix}autocompete/${autocompleteInfo.app_label}/${autocompleteInfo.model_name}/`
    request({
      url: url,
      method: 'post',
      data: {
        search_string: autocompleteInfo.search_string,
        limit: autocompleteInfo.limit,
        viewname: autocompleteInfo.viewname,
        is_filter: autocompleteInfo.is_filter,
        field_slug: autocompleteInfo.field_slug,
        form_data: newFormData,
        existed_choices: autocompleteInfo.existed_choices,
        action_name: autocompleteInfo.actionName,
      },
      headers: {
        'Accept-Language': getLang(),
      },
      timeout: 1000 * 5,
    }).then(response => {
      if (response.data === undefined)
        reject('response.data is undefined')

      resolve(response.data)
    }).catch(error => {
      reject(error)
    })
  })
}
