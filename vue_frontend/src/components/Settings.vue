<template>

  <v-navigation-drawer
    class="settings-container"
    v-model="drawer"
    location="right"
    hide-overlay
    temporary
    absolute
    width="300"
  >
    <Theme/>

    <div class="settings-section">
      <v-label class="mb-2 font-weight-medium">{{ $t('tinyMCETheme') }}</v-label>

      <v-select :value="tinyMCETheme" :items="getTinymcethemes()" @update:modelValue="changeTinymcetheme"></v-select>
    </div>


    <template v-slot:append>
      <div class="settings-append">
        <v-label>Version:</v-label> {{ getConfig().version }}
      </div>
    </template>

  </v-navigation-drawer>

</template>

<script>
import { getSettings, setSettings, tinyMCEThemes, getTinyMCETheme } from '/src/utils/settings'
import { config_dataset } from '/src/utils/settings'
import Theme from '/src/components/Theme.vue'

export default {
  components: {
    Theme,
  },
  props: {
  },
  data(props) {
    return {
      drawer: null,
      tinyMCETheme: getTinyMCETheme(),
    }
  },
  created() {
  },
  methods: {
    getTinymcethemes() {
      return tinyMCEThemes
    },
    toggle() {
      this.drawer = !this.drawer
    },
    getConfig() {
      return config_dataset
    },
    changeTinymcetheme(value) {
      let settings = getSettings()
      settings.tinyMCETheme = value
      setSettings(settings)
      this.emitter.emit("settings-changed", settings);
    }
  },
}
</script>
