<template>
  <div>
    <JsonForms
      :data="data"
      :renderers="renderers"
      :schema="field.json_forms.schema"
      :uischema="field.json_forms.uischema"
      :readonly="readOnly"

      @change="onChange"
    />

    <v-expansion-panels class="jsonforms-source-json">
      <v-expansion-panel>
        <v-expansion-panel-title><v-icon icon="mdi-cog-outline" size="x-small"/> <p>Source JSON</p></v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-label>{{ data }}</v-label>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

  </div>
</template>

<script>
import { toast } from "vue3-toastify"
import { defaultProps, validateProps } from '/src/utils/fields.js'

//import { vanillaRenderers } from '@jsonforms/vue-vanilla';

 import { vuetifyRenderers } from '@jsonforms/vue-vuetify';

const renderers = [
  ...vuetifyRenderers,
//  ...vanillaRenderers,
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
      this.data = formData[this.fieldSlug] || {}
    },
    onChange(event) {
      this.data = event.data;
      if (event.errors.length > 0) {
        console.error('JSONForms', event.errors)
        let errorMessage = []
        for (const error of event.errors) {
          errorMessage.push(`<b>${error.instancePath}</b> ${error.message}`)
        }
        toast(
          `${this.viewname}.${this.fieldSlug} json forms errors:</br>${errorMessage.join('<br>')}`,
          {"theme": "auto", "type": "error", "position": "top-center", "dangerouslyHTMLString": true}
        )
      }
      this.$emit('changed', this.data)
    },
  },
}
</script>
