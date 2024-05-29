<template>

  <v-col>
    <v-row>
        <v-switch :label="$t('darkTheme')" v-model="dark" @click="toggleTheme" color="primary"></v-switch>
    </v-row>
  </v-col>

</template>

<script setup>
import { useTheme } from 'vuetify'

import { getSettings, setSettings } from '/src/utils/settings'

const theme = useTheme()

const dark = ref(theme.global.current.value.dark)

function toggleTheme() {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
  let settings = getSettings()
  settings.theme = theme.global.name.value
  setSettings(settings)
}
</script>
