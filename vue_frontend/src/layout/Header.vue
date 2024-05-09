<template>
  <v-app-bar height="56">
    <v-app-bar-nav-icon variant="text" @click="toggleDrawer"/>

    <v-breadcrumbs :items="['Foo', 'Bar', 'Fizz']">
      <template v-slot:divider>
        <v-icon icon="mdi-chevron-right"></v-icon>
      </template>
    </v-breadcrumbs>

  </v-app-bar>
</template>

<script>

export default {
  props: {
  },
  data() {
    return {
      drawer: null,
    }
  },
  methods: {
    toggleDrawer() {
      this.$emit("toggleDrawer");
    },
  },
}
</script>
