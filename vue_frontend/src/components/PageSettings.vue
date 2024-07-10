<template>
  <v-dialog
    max-width="1200"
    content-class="dialog-top-position"
    v-model="open"
    class="create-dialog"
  >
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn
        v-bind="activatorProps"
        @click="open = true"

        variant="outlined"
        density="compact"
        class="button-icon"
        color="secondary"
        icon="mdi-cog-outline"
      />
    </template>

    <template v-slot:default="{ isActive }">
      <v-card v-if="open">

        <v-card-title class="d-flex justify-space-between align-center">
          <span>{{ getTitle() }}: {{ $t('sectionSettings') }}</span>

          <v-btn
            icon="mdi-close"
            variant="text"
            density="compact"
            @click="isActive.value = false"
          ></v-btn>
        </v-card-title>

        <div class="page-settings-content">
          <v-container v-if="settings">
            <v-row>

              <template v-for="(field, field_slug) in serializer">
                <v-col
                  cols="12"
                  md="4"
                  v-if="canDisplayInList(field, field_slug)"
                >
                  <v-switch
                    :model-value="settings.headers[field_slug]"
                    :rules="nameRules"
                    :label="field.label"
                    color="primary"
                    @update:modelValue="value => onChange(value, field_slug)"
                  ></v-switch>
                </v-col>
              </template>

            </v-row>
          </v-container>
        </div>

      </v-card>
    </template>
  </v-dialog>
</template>

<script>
import { getViewsetsSettings, setViesetsSettings } from '/src/utils/settings'

export default {
  props: {
    apiInfo: {type: Object, required: true},
    viewname: {type: String, required: false},
  },
  emits: ["changed"],
  data() {
    return {
      open: false,
      serializer: null,
      settings: {},
    }
  },
  async created() {
    const meta = this.apiInfo[this.viewname].meta
    this.serializer = meta.serializer
    this.settings = getViewsetsSettings(this.viewname, this.serializer)
  },
  methods: {
    getTitle() {
      return this.apiInfo[this.viewname].title
    },
    canDisplayInList(field, field_name) {
      const sectionData = this.apiInfo[this.viewname]
      if (!field.write_only && (!sectionData.meta.filds_list || sectionData.meta.filds_list.indexOf(field_name) !== -1)) {
        return true
      }
      return false
    },
    onChange(newValue, field_slug) {
      this.settings.headers[field_slug] = newValue
      setViesetsSettings(this.viewname, this.settings)
      this.$emit('changed', this.settings)
    },
  },
}
</script>
