<template>
  <v-layout class="rounded rounded-md">
    <template v-if="apiInfo">

      <Navbar :api-info="apiInfo" :settings="settings" />

      <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
        <Header :settings="settings" />

        Main Content
      </v-main>

    </template>
  </v-layout>
</template>

<script>
import Navbar from '/src/layout/Navbar.vue'
import Header from '/src/layout/Header.vue'

import { getApiInfo } from '/src/api/scheme'
import { getSettings } from '/src/utils/settings'
import { removeToken } from '/src/utils/auth'

export default {
  components: {
    Navbar,
    Header,
  },
  data() {
    return {
      apiInfo: null,
      settings: null,
      loading: true,
    }
  },
  async created() {
    this.settings = getSettings()

    getApiInfo().then(apiInfo => {
      this.apiInfo = apiInfo.data
      this.langs = apiInfo.langs
      this.loading = false
    }).catch(error => {
      this.loading = false
      console.error('API error:', error)
      if (error.response.status == 401) {
        removeToken()
        this.$router.push({ path: '/login' })
      }
    })
  },
  methods: {
  }
}
</script>
