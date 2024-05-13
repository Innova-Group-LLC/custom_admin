import request from '/src/utils/request'
import { getToken, getLang } from '/src/utils/auth'
import { config_dataset } from '/src/utils/settings'

const schemeUrl = config_dataset.backend_prefix + 'get_sections/'

export async function getApiInfo() {
  return await new Promise((resolve, reject) => {
    if (!getToken()) return

    request({
      url: schemeUrl,
      method: 'get',
      headers: {
        'Accept-Language': getLang(),
      },
    }).then(response => {
      if (import.meta.env.NODE_ENV !== 'production') {
        console.table(response.data.sections)
      }
      resolve(response.data)
    }).catch(error => {
      reject(error)
    })
  })
}

export function getNavigationInfo(router, apiInfo) {
  if (!apiInfo) {
    console.error('getNavigationInfo error: apiInfo is null')
    return
  }

  const sections = {}

  for (const [viewname, schemeGroup] of Object.entries(apiInfo)) {
    if (schemeGroup.hide_in_navigation) continue

    const sectionData = {
      meta: {
        title: schemeGroup.group_title,
        icon: schemeGroup.group_icon,
        key: schemeGroup.group,
      },
      children: []
    }
    if (!(schemeGroup.group in sections)) {
      sections[schemeGroup.group] = sectionData
    }

    const list_url = `/${schemeGroup.group}/${viewname}/list`
    const subSection = {
      path: list_url,
      meta: {
        key: viewname,
        title: schemeGroup.title,
        icon: schemeGroup.icon,
        viewname: viewname,
      }
    }
    sections[schemeGroup.group].children.push(subSection)
  }
  return Object.values(sections)
}

export function getMethods(viewname, apiInfo) {
  if (!apiInfo) {
    console.error('getMethods error: apiInfo is null')
    return
  }
  if (!viewname) {
    console.error('getMethods error: viewname is null')
    return
  }
  if (!(viewname in apiInfo)) {
    console.error(`getMethods error: apiInfo does not contains viewname "${viewname}"`)
    return
  }

  let methods = {}

  for (const [routeKey, routeData] of Object.entries(apiInfo[viewname].routers)) {

    for (const [methodHttp, methodName] of Object.entries(routeData.mapping)) {
      let url = config_dataset.backend_prefix + `${viewname}/`

      if (routeData.detail) {
        url = `${url}{id}/`
      }
      if (routeData.inline_type) {
        url = `${url}${methodName}/`
      }
      const actionData = {
        name: routeData.name,
        detail: routeData.detail,
        methodHttp: methodHttp,
        url: url,
        routeKey: routeKey,

        inline_type: routeData.inline_type,
        filterset_fields: routeData.filterset_fields,
        actions: routeData.actions,
      }
      methods[methodName] = actionData
    }
  }
  return methods
}
