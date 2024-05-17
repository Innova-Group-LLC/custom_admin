import i18n from '/src/plugins/i18n'

export function getBreadcrumbs(apiInfo, router, route) {
  let path = []

  path.unshift({
    title: i18n.global.t('mainPage'),
    to: '/dashboard',
  })

  if (['edit', 'list'].indexOf(route.name) !== -1) {
    let sectionData = apiInfo[route.params.viewname]
    const list_url = `/${sectionData.group}/${route.params.viewname}/list`
    path.push({
      to: list_url,
      title: `${sectionData.title}`,
      viewname: route.params.viewname,
    })
  }

  if (route.name === 'edit') {
    let sectionData = apiInfo[route.params.viewname]
    const edit_url = `/${sectionData.group}/${route.params.viewname}/${route.params.id}/update`
    path.push({
      to: edit_url,
      title: `${sectionData.title} #${route.params.id}`,
      viewname: route.params.viewname,
      id: route.params.id,
    })
  }

  return path
}
