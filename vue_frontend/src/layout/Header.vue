<template>
  <v-app-bar class="header-conatainer" height="unset">
    <v-app-bar-nav-icon variant="text" @click="toggleDrawer"/>

    <v-breadcrumbs :items="path">
      <template v-slot:divider>
        <v-icon icon="mdi-chevron-right"></v-icon>
      </template>
    </v-breadcrumbs>

    <v-spacer></v-spacer>

    <v-dialog max-width="500">
      <template v-slot:activator="{ props: activatorProps }">
        <v-btn icon v-bind="activatorProps"><v-icon>mdi-translate</v-icon></v-btn>
      </template>

      <template v-slot:default="{ isActive }">
        <v-card>

          <v-card-title class="d-flex justify-space-between align-center">
            <div class="text-h5 text-medium-emphasis ps-2">
              {{ $t('languageSelection') }}
            </div>

            <v-btn
              icon="mdi-close"
              variant="text"
              @click="isActive.value = false"
            ></v-btn>
          </v-card-title>

          <v-card-text>
            <v-list>
              <v-list-item
                v-for="(title, slug) in langs"
                :key="slug"
                :title="title"
                @click.native="changeLang(slug)"
              ></v-list-item>
            </v-list>
          </v-card-text>

        </v-card>
      </template>
    </v-dialog>

    <v-btn icon><v-icon>mdi-logout</v-icon></v-btn>

  </v-app-bar>
</template>

<script>
import { getBreadcrumbs } from '/src/utils/get-breadcrumb'
import { setLang } from '/src/utils/auth'

export default {
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},
    langs: {type: Object, required: true},
  },
  data() {
    return {
      drawer: null,
      path: [],
    }
  },
  watch: {
    $route() {
      this.getBreadcrumbInfo()
    }
  },
  created() {
    this.getBreadcrumbInfo()
  },
  methods: {
    toggleDrawer() {
      this.$emit("toggleDrawer");
    },
    getBreadcrumbInfo() {
      this.path = getBreadcrumbs(this.apiInfo, this.$router, this.$route)
    },
    changeLang(langSlug) {
      setLang(langSlug)
      document.location.reload()
    },
  },
}
</script>
