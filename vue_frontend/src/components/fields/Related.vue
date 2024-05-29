<template>

  <v-autocomplete
    :density="density"
    :variant="variant"
    :clearable="true"
    v-model="value"
    :label="field.label"
    :messages="field.help_text || []"
    :disabled="field.read_only"

    :items="choices"
    :multiple="isMany()"
    :loading="loading || apiLoading"
    chips
    closable-chips
    persistent-hint
    no-filter

    :return-object="false"
    item-value="id"
    item-title="text"

    :append-inner-icon="isMany() ? 'mdi-relation-many-to-many' : 'mdi-relation-many-to-one'"

    :search="search"
    @update:search="updateSearch"
    @update:modelValue="onChange"
  >
    <template v-slot:chip="{ props, item }">
      <v-chip
        class="autocomplete-chip"
        v-bind="props"
        :text="item.raw.text"
      ></v-chip>
    </template>

    <template v-slot:item="{ props, item }">
      <v-list-item
        v-bind="props"
        :title="item.raw.text"
      ></v-list-item>
    </template>
  </v-autocomplete>

</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'
import { toast } from "vue3-toastify"
import { getAutocomplete } from '/src/api/getAutocomplete'

const requiredFields = {
  model_name: {type: String, required: false},
  app_label: {type: String, required: false},
}

export default {
  props: {
    ...defaultProps,
  },
  emits: ["changed"],
  data(props) {
    return {
      value: null,
      formData: null,
      apiLoading: false,
      choices: [],
      search: '',
    }
  },
  created() {
    validateProps(this, requiredFields)
    this.value = this.field.initial

    if (!this.field.read_only) {
      this.updateChoices()
    }
  },
  methods: {
    updateFormData(initFormData) {
      this.formData = initFormData
      const value = initFormData[this.fieldSlug]

      if (this.isMany()) {
        let newValue = []
        for (const v of value || []) {
          if (typeof v === 'object') {
            if (this.field.read_only) {
              this.choices = [v]
            }
            newValue.push(v.id)
          } else {
            newValue.push(v)
          }
        }
        this.value = newValue
      } else {
        if (typeof value === 'object') {
          if (this.field.read_only) {
            this.choices = [value]
          }
          this.value = value.id
        } else {
          this.value = value
        }
      }

      if (!this.field.read_only) {
        this.updateChoices()
      }
    },
    updateSearch(search) {
      this.search = search
      this.updateChoices()
    },
    updateChoices() {
      getAutocomplete(
        this.field.model_name,
        this.field.app_label,
        this.search || '',
        30,
        this.viewname,
        this.fieldSlug,
        this.formData,
        this.isMany() ? this.value : this.value ? [this.value] : [],
      ).then(response => {
        this.choices = response
        this.apiLoading = false
      }).catch(error => {

        this.apiLoading = false
        let error_message = `Autocomplete ${this.field.model_name}.${this.field.app_label} search:"${this.search}" error:"${error}"`
        console.error(error_message)
        toast(error_message, {
          "limit": 3,
          "theme": "auto",
          "type": "error",
          "position": "top-center",
          "dangerouslyHTMLString": true
        })
      })
    },
    onChange(newValue) {
      this.value = newValue
      this.$emit('changed', this.value)
    },
    isMany() {
      const many = [
        'primarymany',
        'multiple choice',
        'ModelMultipleChoiceFilter',
      ]
      return many.indexOf(this.field.type) !== -1
    },
  },
}
</script>
