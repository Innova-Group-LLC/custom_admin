<template>
  <div class="dashboard-page">

    <el-card class="dashboard-box-card" v-for="view in sidebarInfo()" :key="view.meta.key">
      <div slot="header">
        <i :class="view.meta.icon" v-if="view.meta && view.meta.icon"></i>
        <span class="dashboard-title">{{ view.meta.title }}</span>
      </div>

      <div v-for="line in view.children" :key="line.meta.key">

        <router-link :to="line.path" replace>
          <div class="dashboard-link">{{ line.meta.title }}</div>
        </router-link>

      </div>
    </el-card>

  </div>
</template>

<script>
import { getSidebarInfo } from '@/api/scheme'

export default {
  name: 'Dashboard',
  props: ['apiInfo'],
  methods: {
    sidebarInfo() {
      return getSidebarInfo(this.$router, this.apiInfo)
    },
  }
}
</script>
