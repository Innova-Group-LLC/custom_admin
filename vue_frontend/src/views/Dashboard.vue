<template>
  <div class="dashboard-page">

      <div class="dashboard-element" cols="12" md="3" v-for="view in navigation_info" :key="view.meta.key">
        <v-card
          class="mx-auto"
          :prepend-icon="view.meta.icon"
          width="400"
        >
          <template v-slot:title>
            <span class="font-weight-black">{{ view.meta.title }}</span>
          </template>

          <v-card-text class="bg-surface-light pt-4">

            <v-list>
              <v-list-item
                v-for="line in view.children"
                :key="line.meta.key"
                :title="line.meta.title"
                :prepend-icon="line.meta.icon"
                :to="line.path"
              ></v-list-item>
            </v-list>

          </v-card-text>
        </v-card>

      </div>

  </div>
</template>

<script>
import { getNavigationInfo } from '/src/api/scheme'
import { config_dataset } from '/src/utils/settings'

export default {
  props: {
    apiInfo: {type: Object, required: true},
  },
  data() {
    return {
      navigation_info: null,
    }
  },
  watch: {
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = `${this.$t('mainPage')} | ${config_dataset.title}`
      }
    },
  },
  created() {
    this.navigation_info = getNavigationInfo(this.$router, this.apiInfo)
  },
}
</script>
