<template>
  <v-btn icon @click.native="toggleTheme"><v-icon>mdi-palette</v-icon></v-btn>
</template>

<script setup>
import { useTheme } from 'vuetify'

const theme = useTheme()

function toggleTheme () {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
}
</script>
