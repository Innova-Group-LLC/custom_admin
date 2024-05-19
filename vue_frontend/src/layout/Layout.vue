<template>
  <v-layout class="h-screen">

    <template v-if="apiInfo">

      <Navbar ref="navbar" :api-info="apiInfo" :settings="settings"/>

      <Header
        :api-info="apiInfo"
        :settings="settings"
        :langs="langs"
        @toggle-drawer="toggleDrawer()"
      />

      <v-main class="d-flex page-container">
        <router-view :key="$route.fullPath" :api-info="apiInfo" :settings="settings"/>
      </v-main>

    </template>

    <template v-else-if="loading">

      <v-container fluid class="fill-height h-screen">
        <v-row>
          <v-col class="d-flex justify-center">
            <v-progress-circular
              :size="50"
              color="primary"
              indeterminate
            ></v-progress-circular>
          </v-col>
        </v-row>
      </v-container>

    </template>

  </v-layout>
</template>

<script>
import { toast } from "vue3-toastify";

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
      langs: null,
    }
  },
  async created() {
    this.settings = getSettings()

    getApiInfo().then(apiInfo => {
      this.apiInfo = apiInfo.sections
      this.langs = apiInfo.languages
      this.loading = false
    }).catch(error => {
      this.loading = false
      console.error('API error:', error)
      toast(error, {
        "theme": "auto",
        "type": "error",
        "position": "top-center",
        "dangerouslyHTMLString": true
      })
      if (error.response && error.response.status == 401) {
        removeToken()
        this.$router.push({ path: '/login' })
      }
    })
  },
  methods: {
    toggleDrawer() {
      this.$refs.navbar.toggleDrawer()
    },
  }
}
</script>
