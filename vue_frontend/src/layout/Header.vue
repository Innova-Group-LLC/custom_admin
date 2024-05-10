<template>
  <v-app-bar class="header-conatainer" height="unset">
    <v-app-bar-nav-icon variant="text" @click="toggleDrawer"/>

    <v-breadcrumbs :items="['Foo', 'Bar', 'Fizz']">
      <template v-slot:divider>
        <v-icon icon="mdi-chevron-right"></v-icon>
      </template>
    </v-breadcrumbs>

    <v-spacer></v-spacer>

    <v-btn icon>
      <v-icon>mdi-dots-vertical</v-icon>
    </v-btn>

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
