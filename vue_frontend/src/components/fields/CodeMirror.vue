<template>
  <div class="json-editor" :class="{ 'read-only': field.read_only }">
    <textarea ref="textarea" />
  </div>
</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'

import CodeMirror from 'codemirror'
import 'codemirror/addon/lint/lint.css'
import 'codemirror/lib/codemirror.css'
import 'codemirror/mode/javascript/javascript'
import 'codemirror/addon/lint/lint'
import 'codemirror/addon/lint/json-lint'

import 'codemirror/theme/rubyblue.css'

import jsonlint from 'jsonlint-mod'
window.jsonlint = jsonlint;

const requiredFields = {
  choices: {type: Object, required: true},
  tag_style: {type: String, required: false},
}

export default {
  name: 'jsonfield',
  props: {
    ...defaultProps,
  },
  emits: ["changed"],
  data(props) {
    return {
      jsonEditor: null,
    }
  },
  mounted() {
    validateProps(this, requiredFields)

    this.$nextTick(function () {
      this.jsonEditor = CodeMirror.fromTextArea(this.$refs.textarea, {
        lineNumbers: true,
        mode: 'application/json',
        lint: true,

        // https://codemirror.net/5/demo/theme.html#default
        theme: 'rubyblue',

        readOnly: this.field.read_only,
      })

      this.jsonEditor.on('change', cm => {
        this.$emit('changed', cm.getValue())
      })
    })
  },
  methods: {
    updateFormData(initFormData) {
      let init = initFormData[this.fieldSlug] || ''
      this.jsonEditor.setValue(init)
    },
  },
}
</script>
