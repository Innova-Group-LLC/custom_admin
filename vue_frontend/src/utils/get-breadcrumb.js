import i18n from '/src/plugins/i18n'

export function getBreadcrumbs(apiInfo, router, route) {
  let path = []

  path.unshift({
    title: i18n.global.t('mainPage'),
    to: '/dashboard',
  })

  let sectionData = apiInfo[route.params.viewname]
  if (!sectionData) return path

  if (['edit', 'list'].indexOf(route.name) !== -1) {
    const list_url = `/${sectionData.group}/${route.params.viewname}/list`
    path.push({
      to: list_url,
      title: `${sectionData.title}`,
      viewname: route.params.viewname,
    })
  }

  if (route.name === 'edit') {
    const edit_url = `/${sectionData.group}/${route.params.viewname}/${route.params.pk}/update`
    path.push({
      to: edit_url,
      title: `${sectionData.title} #${route.params.pk}`,
      viewname: route.params.viewname,
      pk: route.params.pk,
    })
  }

  return path
}
