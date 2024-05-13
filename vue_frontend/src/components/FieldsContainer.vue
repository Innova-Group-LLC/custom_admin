<template>
  <v-container fluid class="fields-container">

    <v-tabs
      :class="{ 'hide-element': getGroups().length <= 1, 'container-tabs': true }"
      next-icon="mdi-arrow-right-bold-box-outline"
      prev-icon="mdi-arrow-left-bold-box-outline"
      show-arrows
      v-model="tab"
    >
      <v-tab
        v-for="(groupInfo, tab_id) in getGroups()"
        :key="groupInfo.title"
        :text="groupInfo.title"
        slim
      ></v-tab>
    </v-tabs>

    <template v-if="errors" v-for="error in errors['non_field_errors']">
      <v-alert
        :text="error"
        type="error"
      ></v-alert>
    </template>

    <v-tabs-window v-model="tab">
      <v-tabs-window-item
        v-for="(groupInfo, tab_id) in getGroups()"
        :key="groupInfo.title"
        :text="groupInfo.title"
      >
        <v-card
          v-for="(field, field_slug) in meta.serializer"
        >

          <v-row v-if="canBeDisplayed(field, field_slug, tab_id) && !isTranslation(field_slug)">
            <v-col cols="3">
              <v-list-subheader>{{ field.label }}</v-list-subheader>
            </v-col>

            <v-col cols="9" class="form-field-container">

              <component
                v-if="getFieldComponent(field)"
                :ref='`field_${field_slug}`'
                :field="field"
                :field-slug="field_slug"
                :viewname="viewname"
                :is="getFieldComponent(field)"

                @changed="value => _updateValue(value, field_slug)"
              />
              <template v-else>
                {{ field }}
              </template>

            </v-col>
          </v-row>

        </v-card>
      </v-tabs-window-item>
    </v-tabs-window>

  </v-container>
</template>

<script>
// Contains a list of tabs and a list of fields

import BooleanField from '/src/components/fields/Boolean.vue'
import StringField from '/src/components/fields/String.vue'
import NumberField from '/src/components/fields/Number.vue'
import ChoiceField from '/src/components/fields/Choice.vue'
import FileField from '/src/components/fields/File.vue'
import TinyMCEField from '/src/components/fields/TinyMCE/index.vue'
import JSONFormsField from '/src/components/fields/JSONForms.vue'
import CodeMirrorField from '/src/components/fields/CodeMirror.vue'
import RelatedField from '/src/components/fields/Related.vue'

export default {
  props: {
    apiInfo: {type: Object, required: true},
    formType: {
      type: String,
      required: true,
      validator: function (value) {
          return ['create', 'edit'].indexOf(value) !== -1
      }
    },

    // Required if no meta was provided
    viewname: {type: String, required: false},

    // Schema of this form, if not provided - it will be used from apiInfo
    meta: {
      type: Object,
      required: false,
      validator: function (value) {
        if (value.serializer == null) {
          console.error('fields-container meta must contain serializer')
          return false
        }
        return true
      },
      default(rawProps) {
        return rawProps.apiInfo[rawProps.viewname].meta
      }
    },

    relationNameFilter: {type: Object, required: false},
    filterId: {type: Object, required: false},
  },
  data() {
    return {
      tab: null,
      errors: null,
      formData: {},
      translationsTabs: {},
    }
  },
  watch: {
    formData: {
      handler: function(newValue) {
        if (newValue) {
          this.$emit('changed', newValue)
        }
      },
      deep: true
    }
  },
  methods: {
    getFieldComponent(field) {
      if (['boolean', 'BooleanFilter'].indexOf(field.type) !== -1) return BooleanField
      if (['integer', 'decimal'].indexOf(field.type) !== -1) return NumberField
      if (['list', 'choice'].indexOf(field.type) !== -1) return ChoiceField
      if (['image upload', 'file upload', 'svgfield'].indexOf(field.type) !== -1) return FileField

      if (['field', 'string', 'email', 'url', 'slug'].indexOf(field.type) !== -1) {
        if (field.wysiwyg) return TinyMCEField
        return StringField
      }
      if (field.type === 'json') {
        if (field.json_forms) return JSONFormsField
        return CodeMirrorField
      }

      if (['primary', 'primarymany'].indexOf(field.type) !== -1) return RelatedField

        //related: ['primary', 'primarymany'],
        //date: ['date'],
        //datetime: ['datetime'],
        //time: ['time'],
        //field: ['field'],
      return
    },
    getGroups() {
      if (this.meta.field_groups) return this.meta.field_groups
      return [{"title": ""}]
    },
    getTranslations() {
      return this.meta.translations || {}
    },
    isTranslation(field_slug) {
      for (const [slug, translations] of Object.entries(this.getTranslations())) {
        for (var i = 0; i < translations.length; i++) {
          if (translations[i].slug === field_slug) return true
        }
      }
      return false
    },
    canBeDisplayed(field, field_slug, tab_id) {
      if (this.formType === 'create' && (field.read_only || field.update_only)) {
        return false
      }
      if (this.formType !== 'create' && field.create_only) {
        return false
      }
      if (this.meta.field_groups && this.meta.field_groups !== null) {
        const currentTabFields = this.meta.field_groups[tab_id].fields
        if (currentTabFields && !currentTabFields.includes(field_slug)) return false
      }

      return true
    },
    _updateValue(value, field_slug) {
      this.formData[field_slug] = value

      for (const slug of Object.keys(this.meta.serializer)) {
        const target_field = this.$refs[`field_${slug}`]
        if (target_field === undefined) continue

        // Update all other fields
        if (field_slug !== slug) {
          target_field[0].updateFormData(this.formData)
        }
      }
    },
  },
}
</script>
