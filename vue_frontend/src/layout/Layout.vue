<template>
  <div class="common-layout" v-loading="loading">
    <el-container v-if="apiInfo">

      <el-header>
        <header/>
      </el-header>

      <el-container>

        <el-aside width="200px">
          <navbar :api-info="apiInfo" :langs="langs" :settings="settings"/>
        </el-aside>

        <el-main>Main</el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'

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
      console.error('Error getting API data:' + error)
      ElMessage({ message: error, type: 'error', duration: 5 * 1000 })
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
