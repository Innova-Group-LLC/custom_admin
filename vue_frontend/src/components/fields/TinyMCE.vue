<template>
  <div>

    TinyMCE
    {{ field }}

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
    changed(value) {
      this.$emit('changed', value)
    },
  },
}
</script>
