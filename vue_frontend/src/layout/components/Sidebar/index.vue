<template>
  <div :class="{'has-logo':showLogo}">
    <logo v-if="showLogo" :collapse="isCollapse" />
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu
        :default-active="active"
        :collapse="false"
        :collapse-transition="false"
        :background-color="variables.menuBg"
        :text-color="variables.menuText"
        :unique-opened="false"
        :active-text-color="variables.menuActiveText"
        mode="vertical"
      >

        <app-link :key="link.title" :to="link.url" v-for="link in staticLinks">
          <el-menu-item :index="link.url"class="submenu-title-noDropdown">
            <item :icon="link.icon" v-if="link.icon"/>
            <item :title="link.title" :_static="true" />
          </el-menu-item>
        </app-link>

        <sidebar-item
          v-for="viewname in sidebarInfo()"
          :key="viewname.meta.key"
          :item="viewname"
          :base-path="viewname.path"
        />
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script>
import variables from '/src/styles/variables.scss'

import Logo from './Logo.vue'
import Item from './Item.vue'
import SidebarItem from './SidebarItem.vue'
import AppLink from './Link.vue'
import { getSidebarInfo } from '/src/api/scheme'
import { getBreadcrumbs } from '/src/utils/get-breadcrumb'

export default {
  components: { SidebarItem, Logo, AppLink, Item },
  props: ['apiInfo'],
  data() {
    return {
      active: [],
      openeds: null,
      staticLinks: [
        {
          url: '/dashboard',
          icon: 'el-icon-s-home',
          title: this.$t('main_page'),
        },
      ]
    }
  },
  watch: {
    $route() {
      this.updateActive()
    }
  },
  created() {
    this.updateActive()
  },
  methods: {
    sidebarInfo() {
      return getSidebarInfo(this.$router, this.apiInfo)
    },
    updateActive() {
      if (this.$route.params) {
        const path = getBreadcrumbs(this.apiInfo, this.$router, this.$route)

        if (path.length > 0) this.active = path[0].viewname
      }
    }
  },
  computed: {
    defaultOpeneds() {
    },
    showLogo() {
      return localStorage.closeLogo
    },
    variables() {
      return variables
    },
    isCollapse() {
      return !this.$parent.sidebarOpen
    }
  }
}
</script>
