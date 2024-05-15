<template>

  <v-file-input
    :label="field.label"
    :model-value="value"
    :messages="field.help_text || []"
    :disabled="field.read_only"
    @update:modelValue="changeFile"
  ></v-file-input>

</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'
import { toast } from "vue3-toastify";

const requiredFields = [
]

export default {
  props: {
    ...defaultProps,
  },
  emits: ["changed"],
  data(props) {
    return {
      temp: null,
      value: null,
    }
  },
  created() {
    validateProps(this, requiredFields)
  },
  methods: {
    updateFormData(initFormData) {
      let file_info = initFormData[this.fieldSlug]
      if (file_info) {
        this.value = this.dataURLtoFile(file_info.file, file_info.name)
      }
    },
    dataURLtoFile(dataurl, filename) {
      var arr = dataurl.split(','),
          mime = arr[0].match(/:(.*?);/)[1],
          bstr = atob(arr[arr.length - 1]),
          n = bstr.length,
          u8arr = new Uint8Array(n);
      while(n--){
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], filename, {type:mime});
    },
    toDataUrl(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
      })
    },
    changeFile(file) {
      const name = file.name.replaceAll(",", "").slice(0, 100);
      this.toDataUrl(file).then(result => {
        const newVal = {
          name: name,
          file: result,
        }
        this.$emit('changed', newVal)
      }).catch(error => {
        const message = `${this.fieldSlug} convert error: ${error}`;
        console.error(message)
        toast(message, {
          "limit": 3,
          "theme": "auto",
          "type": "error",
          "position": "top-center",
          "dangerouslyHTMLString": true
        })
      })
    },
  },
}
</script>
