<template>
  <ckeditor
    :editor="editor"
    v-model="value"
    :config="editorConfig"
    :disabled="readOnly"
    @input="onChange"
  />
</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'
import CKEditor from '@ckeditor/ckeditor5-vue'

import { ClassicEditor, Bold, Essentials, Italic, Mention, Paragraph, Undo } from 'ckeditor5'

import 'ckeditor5/ckeditor5.css';

const requiredFields = {
  wysiwyg: {type: Boolean, required: false},
  multilined: {type: Boolean, required: false},
  tag_style: {type: String, required: false},
}

export default {
  components: {
    ckeditor: CKEditor.component
  },
  props: {
    ...defaultProps,
  },
  emits: ["changed"],
  data(props) {
    return {
      value: null,
      editor: ClassicEditor,
      editorConfig: {
        plugins: [ Bold, Essentials, Italic, Mention, Paragraph, Undo ],
        toolbar: [ 'undo', 'redo', '|', 'bold', 'italic' ],
      },
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
    onChange(newValue) {
      this.value = newValue
      this.$emit('changed', this.value)
    },
  },
}
</script>
