<template>

  <div class="theme-picker">
    <div class="mb-3">
      <v-label class="mb-2 font-weight-medium">{{ $t('themeSelection') }}</v-label>
    </div>
      <v-btn-toggle v-model="currentTheme" group>
        <v-btn :base-color="theme.themes._value.blueLight.colors.primary" value="blueLight"></v-btn>
        <v-btn :base-color="theme.themes._value.blueDark.colors.secondary" value="blueDark"></v-btn>
      </v-btn-toggle>

      <v-btn-toggle v-model="currentTheme" group>
        <v-btn :base-color="theme.themes._value.greenLight.colors.primary" value="greenLight"></v-btn>
        <v-btn :base-color="theme.themes._value.greenDark.colors.primary" value="greenDark"></v-btn>
      </v-btn-toggle>

      <v-btn-toggle v-model="currentTheme" group>
        <v-btn :base-color="theme.themes._value.deepPurpleLight.colors.primary" value="deepPurpleLight"></v-btn>
        <v-btn :base-color="theme.themes._value.deepPurpleDark.colors.primary" value="deepPurpleDark"></v-btn>
      </v-btn-toggle>
  </div>

</template>

<script setup>
import { useTheme } from 'vuetify'
import { getSettings, setSettings } from '/src/utils/settings'

const theme = useTheme()

const currentTheme = ref(theme.global.name.value)

watch(currentTheme, async (newCurrentTheme, oldCurrentTheme) => {
  theme.global.name.value = newCurrentTheme
  let settings = getSettings()
  settings.theme = theme.global.name.value
  setSettings(settings)
})
</script>
