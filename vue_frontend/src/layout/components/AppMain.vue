<template>
  <section class="app-main">
    <transition name="fade-transform" mode="out-in">
      <router-view :key="path" :api-info="apiInfo" :settings="settings"/>
    </transition>
  </section>
</template>

<script>
export default {
  name: 'AppMain',
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},
  },
  computed: {
    path() {
      return this.$route.path
    }
  }
}
</script>

<style scoped>
.app-main {
  /*50 = navbar  */
  min-height: calc(100vh - 50px);
  width: 100%;
  position: relative;
  overflow: hidden;
}
.fixed-header+.app-main {
  padding-top: 50px;
}
</style>

<style lang="scss">
// fix css style bug in open el-dialog
.el-popup-parent--hidden {
  .fixed-header {
    padding-right: 15px;
  }
}
</style>
