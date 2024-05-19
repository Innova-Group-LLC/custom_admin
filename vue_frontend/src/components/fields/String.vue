<template>
  <div>

    <v-textarea
      v-if="field.multilined"
      :clearable="true"
      :label="field.label"
      :model-value="value"
      :messages="field.help_text || []"
      :disabled="field.read_only"
      :loading="loading"
    />

    <v-text-field
      v-else
      :clearable="true"
      :label="field.label"
      :model-value="value"
      :messages="field.help_text || []"
      :disabled="field.read_only"
    />

  </div>
</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'

const requiredFields = {
  wysiwyg: {type: Boolean, required: false},
  multilined: {type: Boolean, required: false},
  tag_style: {type: String, required: false},
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
    this.value = this.field.initial
  },
  methods: {
    updateFormData(initFormData) {
      this.value = initFormData[this.fieldSlug]
    },
  },
}
</script>
