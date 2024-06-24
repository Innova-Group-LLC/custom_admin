<template>
  <JsonEditorVue v-model="value" :class="{ 'jse-theme-dark': this.$vuetify.theme.current.dark }"/>
</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'
import 'vanilla-jsoneditor/themes/jse-theme-dark.css'

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

      if (typeof this.value !== 'object') {
        this.value = JSON.parse(this.value)
      }
    },
  },
}
</script>
