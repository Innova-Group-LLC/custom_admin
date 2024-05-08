<template>
  <el-menu
    default-active="2"
    class="el-menu-navbar"
  >
    <el-sub-menu index="1">
      <template #title>
        <el-icon><location /></el-icon>
        <span>Navigator One</span>
      </template>
      <el-menu-item-group title="Group One">
        <el-menu-item index="1-1">item one</el-menu-item>
        <el-menu-item index="1-2">item two</el-menu-item>
      </el-menu-item-group>
      <el-menu-item-group title="Group Two">
        <el-menu-item index="1-3">item three</el-menu-item>
      </el-menu-item-group>
      <el-sub-menu index="1-4">
        <template #title>item four</template>
        <el-menu-item index="1-4-1">item one</el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-menu-item index="2">
      <el-icon><icon-menu /></el-icon>
      <span>Navigator Two</span>
    </el-menu-item>
    <el-menu-item index="3" disabled>
      <el-icon><document /></el-icon>
      <span>Navigator Three</span>
    </el-menu-item>
    <el-menu-item index="4">
      <el-icon><setting /></el-icon>
      <span>Navigator Four</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'

import { getNavigationInfo } from '/src/api/scheme'

export default {
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},
    langs: {type: Object, required: true},
  },
  components: {
    Document,
    IconMenu,
    Location,
    Setting,
  },
  data() {
    return {
      navigation_info: null,
    }
  },
  created() {
    this.navigation_info = getNavigationInfo(this.$router, this.apiInfo)
  },
}
</script>
