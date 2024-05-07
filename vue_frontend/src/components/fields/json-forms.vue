<template>
  <div class="json-forms-container">
    <json-forms
      :data="data"
      :renderers="renderers"
      :schema="field.json_forms.schema"
      :uischema="field.json_forms.uischema"
      :readonly="disabled"
      @change="onChange"
    />
    <div v-if="isDev()">
      {{ data }}
    </div>
  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api';
import { JsonForms } from "@jsonforms/vue2"
import { defaultStyles, mergeStyles, vanillaRenderers } from '@jsonforms/vue2-vanilla'

const myStyles = mergeStyles(defaultStyles, {control: { root: 'my-control' }})

const renderers = [
  ...vanillaRenderers,
];

export default defineComponent({
  name: 'jsonforms',
  props: [
    'field', 'fieldSlug', 'disabled',
  ],
  data(props) {
    return {
      // freeze renderers for performance gains
      renderers: Object.freeze(renderers),
      data: {},
    }
  },
  components: {
    JsonForms,
  },
  created() {
  },
  methods: {
    isDev() {
      return process.env.NODE_ENV != 'production'
    },
    updateFormData(formData) {
      this.data = JSON.parse(formData[this.fieldSlug] || '{}')
    },
    onChange(event) {
      this.data = event.data;
      this.$emit('changed', JSON.stringify(this.data))
    }
  },
  provide() {
    return {
      styles: myStyles,
    };
  },
})
</script>
