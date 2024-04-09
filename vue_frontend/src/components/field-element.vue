<template>
  <div>
    <template v-if="getCustomField(formInfo.viewname, field_slug)">
      <keep-alive>
        <component
          ref="field-element"
          :is="getCustomField(formInfo.viewname, field_slug)"
          :error="error"
          :field="field"
          :field-slug="field_slug"
          @changed="_updateValue"
        />
      </keep-alive>
    </template>

    <template v-else>
      <el-form-item
        :label="label"
        :prop="field_slug"
        :label-width="labelWidth"
        :class="{'is-required': field.required}"
      >

        <el-date-picker
          ref="field-element"
          v-if="field.type === 'datetime'"
          v-model="fieldValue"
          type="datetime"
          :placeholder="$t('select_datetime')"
          value-format="yyyy-MM-ddTHH:mm:ss"
          :class="field.type"
          :disabled="field.read_only"
        />

        <el-date-picker
          ref="field-element"
          v-else-if="field.type === 'date'"
          v-model="fieldValue"
          type="date"
          placeholder="$t('chose_date')"
          value-format="yyyy-MM-dd"
          :class="field.type"
          :disabled="field.read_only"
        />

        <div v-else-if="types.choice.indexOf(field.type) >= 0">
          <el-select
            ref="field-element"
            v-model="fieldValue"
            :multiple="field.type === 'multiple choice'"
            :class="field.type"
            :disabled="field.read_only"
          >
            <el-option
              v-for="item in field.choices"
              :key="item.value"
              :label="item.display_name"
              :value="item.value">
            </el-option>
          </el-select>
        </div>

        <div v-else-if="types.string.indexOf(field.type) >= 0">
          <template v-if="!field.wysiwyg">
            <el-input
              ref="field-element"
              :type="field.multilined ? 'textarea' : ''"
              v-model="fieldValue"
              class="string"
              :maxlength="field.max_length"
              :disabled="field.read_only"
              :placeholder="placeholder"
            />
          </template>
          <template v-else>
            <fieldwysiwyg
              ref="field-element"
              :field="field"
              :field-slug="field_slug"
              :disabled="field.read_only"
              @changed="_updateValue"
              :skin="settings.wysiwygSkin"
            />
          </template>
        </div>

        <el-input-number
          v-else-if="field.type === 'integer'"
          ref="field-element"
          v-model="fieldValue"
          :min="field.min_value"
          :max="field.max_value"
          :name="field.type"
          :disabled="field.read_only"
        />

        <el-input-number
          ref="field-element"
          v-else-if="field.type === 'decimal'"
          v-model="fieldValue"
          :precision="precision"
          :step="0.1"
          :min="field.mininternal_value"
          :max="field.maxinternal_value"
          @change="_updateValue"
          :disabled="field.read_only"
        />

        <el-time-picker
          ref="field-element"
          v-else-if="field.type === 'time'"
          v-model="fieldValue"
          :placeholder="$t('chose_time')"
          value-format="hh:mm:ss"
          :class="field.type"
          :disabled="field.read_only"
        />

        <div v-else-if="types.related.indexOf(field.type) >= 0" class="form-tags">
          <tagsfield
            ref="field-element"
            :model-name="field.model_name"
            :app-label="field.app_label"
            :viewname="formInfo.viewname"
            :type="field.type"
            :class="field.type"
            :max-tags="field.type === 'primary'? 1 : null"
            :placeholder="field.type === 'primary'? $t('select_one_choice') : $t('select_choices')"
            :disabled="field.read_only"
            :add="true"
            :api-info="apiInfo"
            :field-slug="field_slug"
            :init-form-data="initFormData"
            :settings="settings"

            :instance-id="formInfo.recordId"
            :relation-name-filter="formInfo.relationNameFilter"
            :filter-id="formInfo.filterId"

            @changed="_updateValue"
          />
        </div>

        <el-switch
          ref="field-element"
          v-else-if="field.type === 'boolean'"
          v-model="fieldValue"
          :class="field.type"
          :disabled="field.read_only"
        />

        <template v-else-if="types.file.indexOf(field.type) >= 0">
          <filefield
            ref="field-element"
            :field="field"
            :field-slug="field_slug"
            @changed="_updateValue"
          />
        </template>

        <template v-else-if="types.json.indexOf(field.type) >= 0">
          <jsonfield
            ref="field-element"
            :field="field"
            :field-slug="field_slug"
            @changed="_updateValue"
          />
        </template>

        <el-input
          ref="field-element"
          v-else-if="['field'].indexOf(field.type) >= 0"
          v-model="fieldValue"
          class="string"
          :maxlength="field.max_length"
          :disabled="field.read_only"
        />

        <div v-else>{{ field.type }} "{{ field.label }}": {{ fieldValue }}</div>

        <span class="help-text" v-if="field.help_text">{{ field.help_text }}</span>

        <div class="errors" v-if="error">
          <span class="error-text" v-for="(e, field_slug) in error">
            {{ e }}
          </span>
        </div>

      </el-form-item>

      <div class="el-form-item-delimiter"></div>
    </template>
  </div>
</template>

<script>
import JsonField from '@/components/fields/json-field'
import TagsField from '@/components/fields/tags-field'
import FileField from '@/components/fields/file-field'
import FieldWysiwyg from '@/components/fields/field-wysiwyg/index'
import { getCustomField } from '@/components/custom-fields'

export default {
  name: 'FieldElement',
  props: {
    settings: {
      type: Object,
      required: true,
    },
    field_slug: {
      type: String,
      required: true,
    },
    field: {
      type: Object,
      required: true,
    },
    precision: {
      type: Number,
      default: 2,
    },
    formInfo: {
      type: Object,
      required: true,
    },
    apiInfo: {
      type: Object,
      required: true,
    },
    labelWidth: {
      type: String,
      default: '230px',
    },
    label: {
      type: String,
      required: false,
    },
    initFormData: {
      required: false,
    },
    placeholder: {
      type: String,
      required: false,
    },
  },
  components: {
    tagsfield: TagsField,
    filefield: FileField,
    jsonfield: JsonField,
    fieldwysiwyg: FieldWysiwyg,
  },
  data() {
    return {
      types: {
        string: ['string', 'email', 'url', 'slug'],
        choice: ['list', 'choice', 'multiple choice'],
        related: ['primary', 'primarymany'],
        file: ['image upload', 'file upload', 'svgfield'],
        json: ['json'],
      },
      getCustomField,
      typesMap: {
        integer: 'number',
        string: 'string',
        boolean: 'boolean',
        email: 'string',
        choice: 'string',
      },
      internal_value: '',
      internal_error: null,
    }
  },
  computed: {
    error: {
      get() {
        return this.internal_error
      },
      set(val) {
        this.internal_error = val
        this.$emit('update_error', val)
      }
    },
    fieldValue: {
      get() {
        return this.internal_value
      },
      set(val) {
        if (this.internal_value !== val) {
          this.internal_value = val
          this.$emit('changed', val)
        }
      }
    },
  },
  created() {
    this.updateFormData(this.initFormData)
  },
  methods: {
    updateFormData(formData) {
      let value = formData[this.field_slug]
      if (this.types.string.indexOf(this.field.type) >= 0 && value === null) {
        value = ''
      }
      this.internal_value = value

      // Send formData inside field
      const field = this.$refs['field-element']
      if (field !== undefined && typeof field.updateFormData === 'function') {
        field.updateFormData(formData)
      }
    },
    updateError(value) {
      this.error = value
    },
    _updateValue(value) {
      this.fieldValue = value
    }
  },
}
</script>
