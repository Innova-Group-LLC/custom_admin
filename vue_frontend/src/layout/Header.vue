<template>
  <v-app-bar>
    <v-app-bar-nav-icon variant="text" @click="toggleDrawer"/>

    <v-breadcrumbs :items="path">
      <template v-slot:divider>
        <v-icon icon="mdi-chevron-right"></v-icon>
      </template>
    </v-breadcrumbs>

    <v-spacer></v-spacer>

    <Theme/>

    <Language :langs="langs"/>

    <v-btn icon @click.native="logout"><v-icon>mdi-logout</v-icon></v-btn>

  </v-app-bar>
</template>

<script>
import Language from '/src/components/Language.vue'
import Theme from '/src/components/Theme.vue'
import { getBreadcrumbs } from '/src/utils/get-breadcrumb'
import { setLang, removeToken } from '/src/utils/auth'

export default {
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},
    langs: {type: Object, required: true},
  },
  components: {
    Language,
    Theme,
  },
  data() {
    return {
      drawer: null,
      path: [],
    }
  },
  watch: {
    $route() {
      this.getBreadcrumbInfo()
    }
  },
  created() {
    this.getBreadcrumbInfo()
  },
  methods: {
    toggleDrawer() {
      this.$emit("toggleDrawer");
    },
    getBreadcrumbInfo() {
      this.path = getBreadcrumbs(this.apiInfo, this.$router, this.$route)
    },
    changeLang(langSlug) {
      setLang(langSlug)
      document.location.reload()
    },
    logout() {
      removeToken()
      this.$router.push({ path: '/login' })
    },
  },
}
</script>
