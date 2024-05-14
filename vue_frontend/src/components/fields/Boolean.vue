<template>
  <div>

    <v-switch
      :label="field.label"
      :model-value="value"
      :messages="field.help_text || []"
      :disabled="field.read_only"
    ></v-switch>

  </div>
</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'

export default {
  props: {
    ...defaultProps,
  },
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
