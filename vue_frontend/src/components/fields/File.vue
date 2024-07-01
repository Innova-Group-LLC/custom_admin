<template>

  <div>
    <v-file-input
      :density="density"
      :variant="variant"
      :label="field.label"
      :model-value="value"
      :messages="field.help_text || []"
      :disabled="readOnly"
      :loading="loading"

      :prepend-icon="null"
      :append-inner-icon="isImage() ? 'mdi-image' : 'mdi-file'"

      @update:modelValue="changeFile"
    ></v-file-input>

    <template v-if="isImage()">
      <v-img
        v-if="url"
        class="editor-image-preview"
        width="200"
        max-height="200"
        cover
        :src="url"
      />
    </template>
    <template v-else>
      <v-label>{{ url }}</v-label>
    </template>
  </div>

</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'
import { toast } from "vue3-toastify"

const requiredFields = {}

export default {
  props: {
    ...defaultProps,
  },
  emits: ["changed"],
  data(props) {
    return {
      url: null,

      // File object
      value: null,
    }
  },
  created() {
    validateProps(this, requiredFields)
  },
  methods: {
    updateFormData(initFormData) {
      let fileInfo = initFormData[this.fieldSlug] || {}
      this.url = fileInfo.url

      if (fileInfo && fileInfo.file) {
        this.value = this.dataURLtoFile(fileInfo.file, fileInfo.name)
        this.url = URL.createObjectURL(this.value)
      }
      else if (fileInfo.url) {
        this.value = new File([""], fileInfo.name);
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
      this.value = file
      this.url = null
      if (!file) {
        this.$emit('changed', null)
        return
      }

      this.url = URL.createObjectURL(this.value)

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
    isImage() {
      const many = [
        'image upload',
      ]
      return many.indexOf(this.field.type) !== -1
    }
  },
}
</script>
