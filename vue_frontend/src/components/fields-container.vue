<template>
  <el-form
    ref="form"
    class="data-form"
    label-position="left"
    label-width="200px"
    size="mini"
    :model="formData"
  >
    <el-tabs v-model="activeTab" :class="meta.field_groups? '' : 'hide-header'">
      <el-tab-pane
        :label="groupInfo.title"
        v-for="(groupInfo, tab_id) in getGroups()"
        :key="groupInfo.title"
      >

        <template v-if="errors" v-for="error in errors['non_field_errors']">
          <el-alert :title="error" type="error" class="form-error" />
        </template>

        <template
          v-for="(field, field_slug) in meta.serializer"
        >

          <template v-if="canBeDisplayed(field, field_slug, tab_id) && !isTranslation(field_slug)">
            <template v-if="Object.keys(getTranslations()).indexOf(field_slug) === -1">
              <fieldelement
                :ref='`field_${field_slug}`'
                :label="field.label"
                :field_slug="field_slug"
                :field="field"
                :form-info="formInfo"
                :api-info="apiInfo"
                :settings="settings"
                @changed="value => _updateValue(value, field_slug)"

                :init-form-data="formData"
              />
            </template>
            <template v-else>

              <el-form-item
                :label="field.label"
                :prop="field_slug"
                label-width="230px"
                :class="{'is-required': field.required}"
              >
                <el-tabs class="translation-tabs" type="border-card">
                  <template v-for="translation in getTranslations()[field_slug]">
                    <el-tab-pane
                      v-model="translationsTabs[field_slug]"
                      :label="translation.lang_translation"
                      :key="translation.lang_slug"
                      lazy
                    >

                      <fieldelement
                        v-if="meta.serializer[translation.slug]"
                        :label-width="'0px'"
                        :ref='`field_${translation.slug}`'
                        :placeholder="meta.serializer[translation.slug].label"
                        :field_slug="translation.slug"
                        :field="meta.serializer[translation.slug]"
                        :form-info="formInfo"
                        :api-info="apiInfo"
                        :settings="settings"
                        @changed="value => _updateValue(value, translation.slug)"

                        :init-form-data="formData"
                      />
                      <template v-else>
                        <span class="error-text">Field {{ translation.slug }} not found in serializer</span>
                      </template>

                    </el-tab-pane>
                  </template>
                </el-tabs>
              </el-form-item>

            </template>
          </template>

        </template>

      </el-tab-pane>
    </el-tabs>
  </el-form>
</template>

<script>
import FieldElement from '@/components/field-element'
import { getLang } from '@/utils/auth'

export default {
  name: 'FieldsContainer',
  props: {
    settings: {
      type: Object,
      required: true,
    },
    formInfo: {
      validator: function (value) {
        return ['create', 'update'].indexOf(value.formType) !== -1
      }
    },
    apiInfo: Object,
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
        return this.apiInfo[this.formInfo.viewname].meta
      }
    },
  },
  components: {
    fieldelement: FieldElement,
  },
  data() {
    return {
      formData: {},
      errors: {},
      apiMethods: null,
      temp: {},
      activeTab: 0,
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
    getTranslations() {
      return this.meta.translations || {}
    },
    getGroups() {
      if (this.meta.field_groups) return this.meta.field_groups
      return [{"title": ""}]
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
      if (this.formInfo.formType === 'create' && (field.read_only || field.update_only)) {
        return false
      }
      if (this.formInfo.formType !== 'create' && field.create_only) {
        return false
      }
      if (this.meta.field_groups && this.meta.field_groups !== null) {
        const currentTabFields = this.meta.field_groups[tab_id].fields
        if (currentTabFields && !currentTabFields.includes(field_slug)) return false
      }

      return true
    },
    updateErrors(newErrors) {
      this.errors = newErrors

      for (const [slug, value] of Object.entries(this.meta.serializer)) {
        const field = this.$refs[`field_${slug}`]
        if (field === undefined) continue

        field[0].updateError(this.errors[slug])
      }
    },
    updateFormData(newData) {
      // Update form date from outside
      this.formData = newData

      for (const [field_slug, value] of Object.entries(this.meta.serializer)) {
        const field = this.$refs[`field_${field_slug}`]
        if (field === undefined) continue

        field[0].updateFormData(this.formData)
      }
    },
    _updateValue(value, field_slug) {
      this.$set(this.formData, field_slug, value)

      for (const [slug, value] of Object.entries(this.meta.serializer)) {
        const field = this.$refs[`field_${slug}`]
        // console.log('field_slug', field_slug, 'value', 'slug', slug, 'field', field)
        if (field === undefined) continue

        // Update all other fields
        if (field_slug !== slug) {
          field[0].updateFormData(this.formData)
        }
      }
    },
  }
}
</script>
