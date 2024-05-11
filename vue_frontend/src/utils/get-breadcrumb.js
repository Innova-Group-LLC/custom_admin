import i18n from '/src/plugins/i18n'

export function getDetailUrl(route, relationNameFilter) {
  let fromPath = route.query.from ? urlParameterToDict(route.query.from) : []
  if (relationNameFilter) {
    fromPath.push({
      'viewname': route.params.viewname,
      'id': route.params.id,
      'tab': route.query.tab,
    })
  }
  return fromPath.length > 0 ? { from: dictParameterToUrl(fromPath) } : {}
}

export function getBreadcrumbs(apiInfo, router, route) {
  let path = []

  path.unshift({
    title: i18n.global.t('mainPage'),
    to: '/dashboard',
  })

  let fromPath = route.query.from ? urlParameterToDict(route.query.from) : []

  let index = 0
  for (const itemInfo of fromPath) {
    let sectionData = apiInfo[itemInfo.viewname]

    const from = dictParameterToUrl(fromPath.slice(0, index))
    const edit_url = `/${sectionData.group}/${itemInfo.viewname}/${itemInfo.id}/update?tab=${itemInfo.tab}&from=${from}`

    path.push({
      title: `${sectionData.title} #${itemInfo.id}`,
      to: edit_url,
      group: sectionData.group,
      viewname: itemInfo.viewname,
      id: itemInfo.id,
    })
    index += 1
  }

  if (route.name === 'edit') {
    let sectionData = apiInfo[route.params.viewname]
    path.push({
      title: `${sectionData.title} #${route.params.id}`,
      viewname: route.params.viewname,
      id: route.params.id,
    })
  }
  else if (route.name === 'create') {
    path.push({
      title: 'создание',
      viewname: route.params.viewname,
    })
  }
  else if (route.name === 'list') {
    let sectionData = apiInfo[route.params.viewname]
    path.push({
      title: `${sectionData.title}`,
      viewname: route.params.viewname,
    })
  }
  else {
    if (route.meta.title) {
      path.push({title: route.meta.title})
    }
  }

  if (path[0].id !== undefined) {
    const itemInfo = path[0]
    let sectionData = apiInfo[itemInfo.viewname]

    const list_url = `/${sectionData.group}/${itemInfo.viewname}/list`
    path.unshift({
      title: `${sectionData.title}`,
      to: list_url,
      group: sectionData.group,
      viewname: itemInfo.viewname,
    })
  }
  return path
}
