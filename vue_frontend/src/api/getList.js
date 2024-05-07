import request from '/src/utils/request'

export function getList(kwargs) {
  return new Promise((resolve, reject) => {
    let urlsParams = JSON.parse(JSON.stringify(kwargs.pageInfo || {}))

    if (kwargs.search) urlsParams.search = kwargs.search
    if (kwargs.ordering) urlsParams.ordering = kwargs.ordering

    if (kwargs.relationNameFilter) {
      urlsParams.relfilter = kwargs.relationNameFilter
      urlsParams.relfilterid = kwargs.filterId
    }

    if (kwargs.inline_action) {
      urlsParams.inline_action = kwargs.inline_action
    }

    if (kwargs.filters) {
      for (const [filter_slug, filter_data] of Object.entries(kwargs.filters)) {
        if (filter_data != null && filter_data != undefined) {
          urlsParams[filter_slug] = filter_data
        }
      }
    }
    let params = new URLSearchParams()
    for(const [k, v]  of Object.entries(urlsParams)){
      if (Array.isArray(v)){
          v.forEach(element => {
          params.append(k, element)
        });
      } else {
        params.set(k,v)
      }
    }

    const fillUrl = `${kwargs.url}?${params.toString()}`
    request({
      url: fillUrl, method: kwargs.method
    }).then(response => {
      if (kwargs.inline_action) {
        resolve(response)
        return
      }

      resolve(response.data)
    }).catch(error => reject(error))
  })
}
