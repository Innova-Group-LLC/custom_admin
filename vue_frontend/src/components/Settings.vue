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

  </v-navigation-drawer>

</template>

<script>
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
    }
  },
  created() {
  },
  methods: {
    toggle() {
      this.drawer = !this.drawer
    }
  },
}
</script>
