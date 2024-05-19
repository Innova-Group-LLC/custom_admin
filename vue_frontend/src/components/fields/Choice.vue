<template>
  <div>

    <v-select
      :clearable="true"
      :label="field.label"
      :model-value="value"
      :messages="field.help_text || []"
      :disabled="field.read_only"
      :loading="loading"

      :items="field.choices"
      item-title="display_name"
      item-value="value"
      :return-object="false"
    />

  </div>
</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'

const requiredFields = {
  choices: {type: Array, required: true},
  tag_style: {type: String, required: true},
}

export default {
  props: {
    ...defaultProps,
  },
  emits: ["changed"],
  data(props) {
    return {
      value: null,
    }
  },
  created() {
    validateProps(this, requiredFields)
    if (this.field.initial) {
      this.value = this.field.initial.value
    }
  },
  methods: {
    updateFormData(initFormData) {
      const value = initFormData[this.fieldSlug]
      if (value) {
        this.value = value.value
      }
    },
  },
}
</script>
