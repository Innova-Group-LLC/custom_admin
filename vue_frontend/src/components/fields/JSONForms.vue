<template>
  <div>

    JSONForms
    {{ field }}

  </div>
</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'

const requiredFields = [
]

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
    validateProps(this, requiredFields)
    this.value = this.field.initial
  },
  methods: {
    updateFormData(initFormData) {
      this.value = initFormData[this.fieldSlug]
    },
    changed(value) {
      this.$emit('changed', value)
    },
  },
}
</script>
