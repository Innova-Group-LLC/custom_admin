<template>
  <v-navigation-drawer>
    <v-list-item>
      <p class="text-h6">{{ getTitle() }}</p>
    </v-list-item>
    <v-divider></v-divider>

    <v-list v-model:opened="open">
      <v-list-group
        v-for="view in navigation_info"
        :value="view.meta.title "
        :key="view.meta.key"
      >
        <template v-slot:activator="{ props }">
          <v-list-item
            v-bind="props"
            :title="view.meta.title"
            :prepend-icon="view.meta.icon"
          ></v-list-item>
        </template>

        <v-list-item
          v-for="line in view.children" :key="line.meta.key"
          :prepend-icon="line.meta.icon"
          :title="line.meta.title"
          :value="line.path"
        ></v-list-item>
      </v-list-group>
    </v-list>

  </v-navigation-drawer>
</template>

<script>
import { config_dataset } from '/src/utils/settings'
import { getNavigationInfo } from '/src/api/scheme'

export default {
  props: {
    apiInfo: {type: Object, required: true},
  },
  components: {
  },
  data() {
    return {
      navigation_info: null,
      open: null,
    }
  },
  created() {
    this.navigation_info = getNavigationInfo(this.$router, this.apiInfo)
  },
  methods: {
    getTitle() {
      return config_dataset.title
    }
  }
}
</script>
