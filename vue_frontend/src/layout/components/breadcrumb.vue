<template>
  <el-breadcrumb class="app-breadcrumb" separator-class="el-icon-arrow-right">

    <template v-for="page in path">
      <el-breadcrumb-item :to="{ path: page.url }" replace>{{ page.title }}</el-breadcrumb-item>
    </template>

  </el-breadcrumb>
</template>

<script>
import pathToRegexp from 'path-to-regexp'
import { getBreadcrumbs } from '@/utils/get-breadcrumb'

export default {
  data() {
    return {
      path: [],
    }
  },
  props: {
    apiInfo: {type: Object, required: true},
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
    getBreadcrumbInfo() {
      this.path = getBreadcrumbs(this.apiInfo, this.$router, this.$route)
    },
    openLink(url) {
      this.$router.push({ path: url } )
    }
  }
}
</script>

<style lang="scss" scoped>
.app-breadcrumb.el-breadcrumb {
  display: inline-block;
  font-size: 14px;
  line-height: 50px;
  margin-left: 8px;

  .no-redirect {
    color: #97a8be;
    cursor: text;
  }
}
</style>
