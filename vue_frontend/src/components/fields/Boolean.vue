<template>

  <v-switch
    class="boolean-switch"
    :density="density"
    :variant="variant"
    :label="field.label"
    :model-value="value"
    :messages="field.help_text || []"
    :disabled="field.read_only"
    color="primary"
    :loading="loading"

    @update:modelValue="onChange"
  ></v-switch>

</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'

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
    validateProps(this)
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
