<template>
  <div class="languages-block">
    <el-dropdown :show-timeout="10">

      <span class="el-dropdown-link">
        <img class="lang-icon" :src="getImageUrl($i18n.locale)"/>
      </span>

      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item
          class="lang-option"
          @click.native="changeLang(slug)"
          :key="slug"
          v-for="(title, slug) in langs"
        >
          <img class="lang-icon":src="getImageUrl(slug)"/>
          <span>{{ title }}</span>
        </el-dropdown-item>
      </el-dropdown-menu>

    </el-dropdown>
  </div>
</template>

<script>
import { setLang } from '/src/utils/auth'

export default {
  props: ['langs'],
  data() {
    return {
    }
  },
  methods: {
    getImageUrl(locale) {
      const langs_map = {
        'en': 'gb',
        'cs': 'cz',
        'kk': 'kz',
      }
      const l = langs_map[locale] || locale
      return `https://hatscripts.github.io/circle-flags/flags/${l}.svg`
    },
    changeLang(langSlug) {
      setLang(langSlug)
      document.location.reload()
    }
  }
}
</script>
