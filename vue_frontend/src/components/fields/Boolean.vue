<template>
  <div>

    <v-switch
      :label="field.label"
      :model-value="value"
      :messages="field.help_text || []"
      :disabled="field.read_only"
      color="var(--color-darken-2)"
      :loading="loading"
    ></v-switch>

  </div>
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
  },
}
</script>
