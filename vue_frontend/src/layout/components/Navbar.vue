<template>
  <div class="navbar">
    <hamburger :is-active="this.$parent.sidebarOpen" class="hamburger-container" @toggleClick="toggleSideBar" />

    <breadcrumb class="breadcrumb-container" :api-info="apiInfo" />

    <div class="right-menu">
      <ChangeLanguage :langs="langs"/>

      <SiteSettings :settings="settings"/>

      <el-dropdown class="avatar-container" trigger="click">
        <div class="avatar-wrapper">
          <span class="user-avatar">{{ name }}</span>
          <i class="el-icon-caret-bottom" />
        </div>
        <el-dropdown-menu slot="dropdown" class="user-dropdown">
          <el-dropdown-item @click.native="logout">
            <span style="display:block;">{{ $t('log_out') }}</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import Breadcrumb from '/src/layout/components/breadcrumb.vue'
import ChangeLanguage from '/src/layout/components/ChangeLanguage.vue'
import SiteSettings from '/src/layout/components/SiteSettings.vue'
import Hamburger from '/src/layout/components/hamburger.vue'
import { removeToken } from '/src/utils/auth'

export default {
  components: {
    Breadcrumb,
    Hamburger,
    ChangeLanguage,
    SiteSettings,
  },
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},
    langs: {type: Object, required: true},
  },
  data() {
    return {
      name: localStorage.getItem('name')
    }
  },
  methods: {
    toggleSideBar() {
      this.$parent.sidebarOpen = !this.$parent.sidebarOpen
    },
    async logout() {
      removeToken()
      this.$router.push({ path: '/login' })
    }
  }
}
</script>

<style lang="scss" scoped>
 .navbar {
     height: 50px;
     overflow: hidden;
     position: relative;
     background: #fff;
     box-shadow: 0 1px 4px rgba(0,21,41,.08);

     .hamburger-container {
         line-height: 46px;
         height: 100%;
         float: left;
         cursor: pointer;
         transition: background .3s;
         -webkit-tap-highlight-color:transparent;

         &:hover {
             background: rgba(0, 0, 0, .025)
         }
     }

     .breadcrumb-container {
         float: left;
     }

     .right-menu {
         float: right;
         height: 100%;
         line-height: 50px;

         &:focus {
             outline: none;
         }

         .right-menu-item {
             display: inline-block;
             padding: 0 8px;
             height: 100%;
             font-size: 18px;
             color: #5a5e66;
             vertical-align: text-bottom;

             &.hover-effect {
                 cursor: pointer;
                 transition: background .3s;

                 &:hover {
                     background: rgba(0, 0, 0, .025)
                 }
             }
         }

         .avatar-container {
             margin-right: 30px;
             margin-left: 10px;

             .avatar-wrapper {
                 margin-top: 5px;
                 position: relative;

                 .user-avatar {
                     cursor: pointer;
                     width: 40px;
                     height: 40px;
                     border-radius: 10px;
                 }

                 .el-icon-caret-bottom {
                     cursor: pointer;
                     position: absolute;
                     right: -20px;
                     top: 18px;
                     font-size: 12px;
                 }
             }
         }
     }
 }
</style>
