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
        :class="{'tab-error': isTabError(groupInfo)}"
      ></v-tab>
    </v-tabs>

    <template v-if="errors" v-for="error in errors['non_field_errors']">
      <v-alert
        :text="error"
        type="error"
      ></v-alert>
    </template>

    <v-tabs-window v-model="tab" class="fields-content">
      <v-tabs-window-item
        v-for="(groupInfo, tab_id) in getGroups()"
        :key="groupInfo.title"
        :text="groupInfo.title"
        :eager="true"
      >
        <div v-for="(field, field_slug) in serializer">

          <v-row class="fields-cell" v-if="canBeDisplayed(field, field_slug, tab_id) && !isTranslation(field_slug)">
            <v-col cols="3">
              <v-list-subheader>
                <p class="form-title">{{ field.label }}</p> <p v-if="field.required" class="required-title">*</p>
              </v-list-subheader>
            </v-col>

            <v-col cols="9" class="form-field-container">

              <!-- Translations -->
              <template v-if="Object.keys(translations).indexOf(field_slug) !== -1">
                <v-tabs
                  v-model="translationsTabs[field_slug]"
                  bg-color="rgb(var(--v-theme-light2))"
                >
                  <v-tab
                    v-for="translation in translations[field_slug]"
                    :key="translation.lang_slug"
                    :text="translation.lang_translation"
                    :value="translation.lang_slug"
                  ></v-tab>
                </v-tabs>

                <v-tabs-window v-model="translationsTabs[field_slug]">
                  <v-tabs-window-item
                    v-for="translation in translations[field_slug]"
                    :key="translation.lang_slug"
                    :value="translation.lang_slug"
                    transition="fade"
                    reverse-transition="fade"
                    :eager="true"
                  >
                    <v-card flat>
                      <component
                        v-if="getFieldComponent(field)"
                        :is="getFieldComponent(field)"

                        density="comfortable"
                        variant="filled"
                        :ref="getRefString(translation.slug)"
                        :field="field"
                        :field-slug="translation.slug"
                        :viewname="viewname"
                        :loading="loading"
                        :action-name="actionName"
                        :read-only="readOnly || field.read_only"

                        @changed="value => _updateValue(value, translation.slug)"
                      />
                      <template v-else>
                        {{ field }}
                      </template>
                    </v-card>
                  </v-tabs-window-item>
                </v-tabs-window>
              </template>

              <template v-else>
                <component
                  v-if="getFieldComponent(field)"
                  :is="getFieldComponent(field)"

                  density="comfortable"
                  variant="filled"
                  :ref="getRefString(field_slug)"
                  :field="field"
                  :field-slug="field_slug"
                  :viewname="viewname"
                  :loading="loading"
                  :action-name="actionName"
                  :read-only="readOnly || field.read_only"

                  :relation-name-filter="relationNameFilter"
                  :filter-id="filterId"

                  @changed="value => _updateValue(value, field_slug)"
                />
                <template v-else>
                  {{ field }}
                </template>
              </template>

              <template v-if="errors && errors[field_slug]">
                <p class="form-error" v-for="error in errors[field_slug]">{{ error }}</p>
              </template>

            </v-col>
          </v-row>

        </div>
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
import JSONFormsField from '/src/components/fields/JSONForms.vue'
import JSONEditorField from '/src/components/fields/JSONEditor.vue'
import RelatedField from '/src/components/fields/Related.vue'
import DateTimeField from '/src/components/fields/DateTime.vue'

import TinyMCEField from '/src/components/fields/TinyMCE/index.vue'
import CKEditor from '/src/components/fields/CKEditor.vue'

const wysiwyg = TinyMCEField;

export default {
  props: {
    apiInfo: {type: Object, required: true},
    loading: {type: Boolean, required: false},
    readOnly: {type: Boolean, required: false},
    formType: {
      type: String,
      required: true,
      validator: function (value) {
          return ['create', 'edit'].indexOf(value) !== -1
      }
    },

    // Required if no meta was provided
    viewname: {type: String, required: false},
    formSerializer: {type: Object, required: false},

    relationNameFilter: {type: Object, required: false},
    filterId: {type: Object, required: false},

    actionName: {type: String, required: false},
  },
  emits: ["changed"],
  data() {
    return {
      tab: null,
      errors: {},
      formData: {},
      translationsTabs: {},
      fieldGroups: null,
      serializer: null,
      translations: {},
    }
  },
  created() {
    if (this.viewname) {
      const meta = this.apiInfo[this.viewname].meta
      this.serializer = meta.serializer
      this.fieldGroups = meta.field_groups
      this.translations = meta.translations || {}
    }
    else if (this.formSerializer) {
      this.serializer = this.formSerializer
    }
    else {
      console.log('viewname or formSerializer required')
    }
  },
  methods: {
    getFieldComponent(field) {
      if (['boolean'].indexOf(field.type) !== -1) return BooleanField
      if (['integer', 'decimal', 'float'].indexOf(field.type) !== -1) return NumberField
      if (['list', 'choice'].indexOf(field.type) !== -1) return ChoiceField
      if (['image upload', 'file upload', 'svgfield'].indexOf(field.type) !== -1) return FileField
      if (['datetime', 'date', 'time'].indexOf(field.type) !== -1) return DateTimeField
      if (['primary', 'primarymany'].indexOf(field.type) !== -1) return RelatedField

      if (['field', 'string', 'email', 'url', 'slug'].indexOf(field.type) !== -1) {
        if (field.wysiwyg) return wysiwyg
        return StringField
      }
      if (field.type === 'json') {
        if (field.json_forms) return JSONFormsField
        return JSONEditorField
      }

      return
    },
    getGroups() {
      if (this.fieldGroups) return this.fieldGroups
      return [{"title": ""}]
    },
    isTranslation(field_slug) {
      for (const [slug, translations] of Object.entries(this.translations)) {
        for (var i = 0; i < translations.length; i++) {
          if (translations[i].slug === field_slug) return true
        }
      }
      return false
    },
    canBeDisplayed(field, field_slug, tab_id) {
      if (this.formType === 'create' && (this.readOnly || field.update_only)) {
        return false
      }
      if (this.formType !== 'create' && field.create_only) {
        return false
      }
      if (this.fieldGroups && this.fieldGroups !== null) {
        const currentTabFields = this.fieldGroups[tab_id].fields
        if (currentTabFields && !currentTabFields.includes(field_slug)) return false
      }

      return true
    },
    getRefString(slug) {
      return `field_${slug}`
    },
    updateErrors(newErrors) {
      this.errors = newErrors
    },
    updateFormData(newData) {
      // Update form date from outside
      this.formData = newData

      for (const [field_slug, value] of Object.entries(this.serializer)) {
        const ref = this.getRefString(field_slug)
        const field = this.$refs[ref]

        if (field === undefined) continue

        field[0].updateFormData(this.formData)
      }
    },
    _updateValue(value, field_slug) {
      if (this.formData[field_slug] === value) return

      this.formData[field_slug] = value

      for (const slug of Object.keys(this.serializer)) {
        const target_field = this.$refs[this.getRefString(slug)]
        if (target_field === undefined) continue

        // Update all other fields
        if (field_slug !== slug) {
          target_field[0].updateFormData(this.formData)
        }
      }
      this.$emit('changed', this.formData)
    },
    isTabError(groupInfo) {
      if (!groupInfo.fields) return false

      for (const error_field of Object.keys(this.errors)) {
        if (groupInfo.fields.indexOf(error_field) !== -1) {
          return true
        }
      }
      return false
    },
  },
}
</script>
