<template>
  <json-forms
    :data="data"
    :renderers="renderers"
    :schema="field.json_forms.schema"
    :uischema="field.json_forms.uischema"
    :readonly="field.read_only"
    @change="onChange"
  />
</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'

import { vuetifyRenderers } from '@jsonforms/vue-vuetify';

const renderers = [
  ...vuetifyRenderers,
];

const requiredFields = {
  json_forms: {type: Object, required: true},
}

export default {
  props: {
    ...defaultProps,
  },
  emits: ["changed"],
  data(props) {
    return {
      renderers: Object.freeze(renderers),
      data: {},
    }
  },
  created() {
    validateProps(this, requiredFields)
  },
  methods: {
    updateFormData(formData) {
      this.data = JSON.parse(formData[this.fieldSlug] || '{}')
    },
    onChange(event) {
      this.data = event.data;
      this.$emit('changed', JSON.stringify(this.data))
    },
  },
}
</script>
