<template>
  <JsonEditorVue v-model="value"/>
</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'

import JsonEditorVue from 'json-editor-vue'

export default {
  components: {
    JsonEditorVue,
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
  watch: {
    value(val){
      this.$emit('changed', val)
    }
  },
  methods: {
    updateFormData(initFormData) {
      this.value = initFormData[this.fieldSlug] || {}
    },
  },
}
</script>
