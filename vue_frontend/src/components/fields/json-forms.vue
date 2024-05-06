<template>
  <div>
    field.json_forms: {{ field.json_forms }}
    <json-forms
      :data="data"
      :renderers="renderers"
      :schema="schema"
      :uischema="uischema"
      :readonly="disabled"
      @change="onChange"
    />
  </div>
</template>

<script>
import { JsonForms } from "@jsonforms/vue2";
import { defaultStyles, mergeStyles, vanillaRenderers } from '@jsonforms/vue2-vanilla'

const myStyles = mergeStyles(defaultStyles, {control: { root: 'my-control' }});

const renderers = [
  ...vanillaRenderers,
];

const schema = {
  "type": "object",
  "properties": {
    "comments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "date": {
            "type": "string",
            "format": "date"
          },
          "message": {
            "type": "string",
            "maxLength": 5
          },
          "enum": {
            "type": "string",
            "enum": [
              "foo",
              "bar"
            ]
          }
        }
      }
    }
  }
}

const uischema = {
  "type": "VerticalLayout",
  "elements": [
    {
      "type": "Control",
      "scope": "#/properties/comments"
    }
  ]
}

export default {
  name: 'jsonforms',
  props: [
    'field', 'fieldSlug', 'disabled',
  ],
  data(props) {
    return {
      // freeze renderers for performance gains
      renderers: Object.freeze(renderers),
      data: {},
      schema,
      uischema,
    }
  },
  components: {
    JsonForms,
  },
  created() {
  },
  methods: {
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
}
</script>
