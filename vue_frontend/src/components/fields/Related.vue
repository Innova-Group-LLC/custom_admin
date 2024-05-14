<template>
  <div>

    <v-autocomplete
      :clearable="true"
      v-model="value"
      :label="field.label"
      :messages="field.help_text || []"
      :disabled="field.read_only"

      :items="choices"
      :multiple="field.type === 'multiple choice'"
      :loading="loading"
      chips
      closable-chips
      persistent-hint
      no-filter

      :search="search"
      @update:search="updateSearch"
    >
      <template v-slot:chip="{ props, item }">
        <v-chip
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

  </div>
</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'
import { toast } from "vue3-toastify";
import { getAutocomplete } from '/src/api/getAutocomplete'

const requiredFields = [
  'model_name',
  'app_label',
]

export default {
  props: {
    ...defaultProps,
  },
  data(props) {
    return {
      value: null,
      formData: null,
      loading: false,
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
      this.value = initFormData[this.fieldSlug]
    },
    updateSearch(search) {
      console.log('search', search)
      this.search = search
      this.updateChoices()
    },
    updateChoices() {
      getAutocomplete(
        this.field.model_name,
        this.field.app_label,
        this.search,
        30,
        this.viewname,
        this.fieldSlug,
        this.formData,
        this.value,
      ).then(response => {
        this.choices = response
        console.log(this.search, this.choices)
        this.loading = false
      }).catch(error => {

        this.loading = false
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
  },
}
</script>
