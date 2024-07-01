<template>
  <v-number-input
    :density="density"
    :variant="variant"
    :clearable="true"
    :label="field.label"
    :model-value="value"
    :messages="field.help_text || []"
    :disabled="readOnly"
    :loading="loading"

    :max="field.max_value"
    :min="field.min_value"

    :reverse="false"
    :hideInput="false"
    :inset="false"

    @update:modelValue="onChange"
  />

</template>

<script>
import { VNumberInput } from 'vuetify/labs/VNumberInput'
import { defaultProps, validateProps } from '/src/utils/fields.js'

const requiredFields = {
  max_value: {type: Number, required: false},
  min_value: {type: Number, required: false},
}

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
    onChange(newValue) {
      this.value = newValue
      this.$emit('changed', this.value)
    },
  },
}
</script>
