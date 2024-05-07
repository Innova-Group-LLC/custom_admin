<template>
  <div class="image-upload">
    <div class="upload-info">
      <template v-if="field.type === 'svgfield'">
        <el-upload
          action="https://jsonplaceholder.typicode.com/posts/"
          accept="image/svg+xml"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload"
        >
          <label class="upload-button el-button el-button--primary">{{ $t('select') }}</label>
        </el-upload>
      </template>

      <template v-else>
        <label :for="inputId" class="upload-button el-button el-button--primary" >{{ $t('select') }}</label>
        <input
          hidden
          type="file"
          ref="fileInput"
          :id="inputId"
          :class="field.type"
          @change="changeFile"
        >
      </template>
    </div>

    <template v-if="temp || defaultSVGComponent">
      <el-link
        v-if="field.type === 'file upload'"
        class="file-link"
        :href="temp"
        target="_blank">{{ temp.slice(-80) }}
      </el-link>

      <template v-else-if="temp">
        <div hidden>{{ temp }}</div>
        <el-image
          class="image-field"
          :src="temp"
          :href="temp"
        />
      </template>
      <div class="image-field" v-else-if="defaultSVGComponent" v-html="defaultSVGComponent"/>
      <i class="file-remove el-icon-delete" @click="removeFile"></i>
    </template>
  </div>
</template>

<script>

export default {
  name: 'filefield',
  props: [
    'field', 'fieldSlug',
  ],
  data(props) {
    return {
      temp: null,
      defaultSVGComponent: null,
      inputId: props.fieldSlug + new Date().getTime()
    }
  },
  created() {
    this.setDefaultValue(this.initValue)
  },
  methods: {
    updateFormData(formData) {
      const init = formData[this.fieldSlug]
      if (this.temp === null || this.temp === undefined) {
        this.setDefaultValue(init)
      }
    },
    setDefaultValue(initValue) {
      if (initValue) {
        if (['image upload', 'file upload'].indexOf(this.field.type) !== -1) {
          this.temp = initValue
        }
        else if (this.field.type === 'svgfield') {
          this.defaultSVGComponent = initValue
        }
      }
    },
    toBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
      })
    },
    changeFile(value) {
      const file = value.target.files[0]
      this.temp = URL.createObjectURL(file)

      const name = file.name.replaceAll(",", "").slice(0, 100);
      this.toBase64(file).then(base64 => {
        const newVal = `${name},${base64}`
        this.$emit('changed', newVal)
      }).catch(error => {
        const message = `Error for convert file to base64 for ${fieldSlug}`;
        console.error(message)
        Message({ message: message, type: 'error', duration: 3 * 1000 })
      })
    },
    removeFile() {
      this.temp = null
      this.defaultSVGComponent = null
      this.$refs.fileInput.value = null

      this.$emit('changed', null)
    },
    handleAvatarSuccess(res, file) {
      this.temp = URL.createObjectURL(file.raw)
      const reader = new FileReader();
      reader.readAsText(file.raw);

      reader.onload = () => (this.$emit('changed', reader.result));
    },
    beforeAvatarUpload(file) {
      const isSVG = file.type === "image/svg+xml";
      const isLt2M = file.size / 1024 < 100;

      if (!isSVG) {
        this.$message.error("Icon picture must be SVG format!");
      }
      if (!isLt2M) {
        this.$message.error("Icon picture size can not exceed 100kb!");
      }

      return isSVG && isLt2M;
    },
  }
}
</script>
