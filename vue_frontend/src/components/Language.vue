<template>

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

</template>

<script>
import { setLang } from '/src/utils/auth'

export default {
  props: {
    langs: {type: Object, required: true},
  },
  methods: {
    changeLang(langSlug) {
      setLang(langSlug)
      document.location.reload()
    },
  },
}
</script>
