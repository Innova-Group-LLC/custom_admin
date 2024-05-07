import { config_dataset } from '@/utils/settings'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${config_dataset.title}`
  }
  return `${config_dataset.title}`
}
