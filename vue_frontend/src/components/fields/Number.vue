<template>
  <div>

    <v-number-input
      :clearable="true"
      :label="field.label"
      :model-value="value"
      :messages="field.help_text || []"
      :disabled="field.read_only"

      :max="field.max_value"
      :min="field.min_value"

      :reverse="false"
      :hideInput="false"
      :inset="false"
    />

  </div>
</template>

<script>
import { VNumberInput } from 'vuetify/labs/VNumberInput'
import { defaultProps, validateProps } from '/src/utils/fields.js'

const requiredFields = [
  'max_value',
  'min_value',
]

export default {
  components: {
    VNumberInput,
  },
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
