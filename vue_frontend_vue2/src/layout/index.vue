<template>
  <div :class="classObj" class="app-wrapper" v-loading="loading">
    <template v-if="apiInfo" >
      <sidebar class="sidebar-container" :api-info="apiInfo"/>
      <div class="main-container">
        <div :class="{'fixed-header':fixedHeader}">
          <navbar :api-info="apiInfo" :langs="langs" :settings="settings"/>
        </div>
        <app-main :api-info="apiInfo" :settings="settings"/>
      </div>
    </template>
  </div>
</template>

<script>
import { Navbar, Sidebar, AppMain } from './components'
import { Message } from 'element-ui'
import { getApiInfo } from '@/api/scheme'
import { getSettings } from '@/utils/settings'
import { removeToken } from '@/utils/auth'

export default {
  name: 'Layout',
  components: {
    Navbar,
    Sidebar,
    AppMain
  },
  data() {
    return {
      apiInfo: null,
      settings: null,
      sidebarOpenValue: null,
      device: localStorage.getItem('device'),
      fixedHeader: localStorage.getItem('fixedHeader'),
      loading: true,
    }
  },
  async created() {
    this.settings = getSettings()

    this.sidebarOpen = JSON.parse(localStorage.getItem('sidebarOpen'))
    if (this.sidebarOpen === null) { this.sidebarOpen = true }

    getApiInfo().then(apiInfo => {
      this.apiInfo = apiInfo.sections
      this.langs = apiInfo.languages
      this.loading = false
    }).catch(error => {
      this.loading = false
      console.error('Error getting API data:' + error)
      Message({ message: error, type: 'error', duration: 5 * 1000 })
      if (error.response.status == 401) {
        removeToken()
        this.$router.push({ path: '/login' })
      }
    })
  },
  computed: {
    sidebarOpen: {
      get: function() {
        return this.sidebarOpenValue
      },
      set: function(value) {
        this.sidebarOpenValue = value
        localStorage.setItem('sidebarOpen', value)
      }
    },
    classObj() {
      return {
        hideSidebar: !this.sidebarOpen,
        openSidebar: this.sidebarOpen,
        withoutAnimation: localStorage.withoutAnimation,
        // mobile: this.device === 'mobile'
      }
    }
  },
  methods: {
    handleClickOutside() {
      localStorage.withoutAnimation = false
    }
  }
}
</script>

<style lang="scss" scoped>
 @import "~@/styles/mixin.scss";
 @import "~@/styles/variables.scss";

 .app-wrapper {
     @include clearfix;
     position: relative;
     height: 100%;
     width: 100%;
     &.mobile.openSidebar{
         position: fixed;
         top: 0;
     }
 }
 .drawer-bg {
     background: #000;
     opacity: 0.3;
     width: 100%;
     top: 0;
     height: 100%;
     position: absolute;
     z-index: 999;
 }

 .fixed-header {
     position: fixed;
     top: 0;
     right: 0;
     z-index: 9;
     width: calc(100% - #{$sideBarWidth});
     transition: width 0.28s;
 }

 .hideSidebar .fixed-header {
     width: calc(100% - 54px)
 }

 .mobile .fixed-header {
     width: 100%;
 }
</style>
