<template>
  <div class="json-editor">
    <textarea ref="textarea" />
  </div>
</template>

<script>
import CodeMirror from 'codemirror'
import 'codemirror/addon/lint/lint.css'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/rubyblue.css'
require('script-loader!jsonlint')
import 'codemirror/mode/javascript/javascript'
import 'codemirror/addon/lint/lint'
import 'codemirror/addon/lint/json-lint'

export default {
  name: 'jsonfield',
  props: [
    'field', 'fieldSlug',
  ],
  data(props) {
    return {
      jsonEditor: null,

      // https://codemirror.net/5/demo/theme.html#default
      theme: 'default',
    }
  },
  mounted() {
    this.$nextTick(function () {
      this.jsonEditor = CodeMirror.fromTextArea(this.$refs.textarea, {
        lineNumbers: true,
        mode: 'application/json',
        lint: true,
        theme: this.theme,
      })

      this.jsonEditor.on('change', cm => {
        this.$emit('changed', cm.getValue())
      })
    })
  },
  methods: {
    updateFormData(initFormData) {
      let init = initFormData[this.fieldSlug]

      try {
        init = JSON.stringify(JSON.parse(init), null, 2)
      } catch (e) {
        console.error(`Json "${this.fieldSlug}" error:`, e)
      }

      this.jsonEditor.setValue(init)
    },
  },
}
</script>
