<template>
  <div v-loading="loadData" class="model-form-container">
    <div class="header-form" v-if="formInfo.showTitle">
      <h2 class="form-title">{{ getTitle() }}</h2>
      <i class="el-icon-close icon-close" @click="handleClose"></i>
    </div>

    <fieldscontainer
      ref="fieldscontainer"
      :api-info="apiInfo"
      :form-info="formInfo"
      :settings="settings"
      @changed="_updateFormData"
    />

    <div class="form-buttons">
      <el-button @click="handleClose">{{ $t('close') }}</el-button>
      <el-button type="primary" @click="sendAction" v-if="canAdd()">
        {{ getActionButtonTitle() }}
      </el-button>
    </div>
  </div>
</template>

<script>
import { getDetail } from '@/api/getDetail'
import { sendData } from '@/api/sendData'
import { Message } from 'element-ui'
import { getMethods } from '@/api/scheme'

export default {
  name: 'ModelForm',
  components: {
    "fieldscontainer": () => import('@/components/fields-container'),
  },
  props: {
    settings: {
      type: Object,
      required: true,
    },
    formInfo: {
      validator: function (value) {
        if (value.viewname == null) {
          console.error('model-form formInfo must contain viewname')
          return false
        }
        return ['create', 'update'].indexOf(value.formType) !== -1
      }
    },
    apiInfo: Object,
  },
  data() {
    return {
      sectionData: null,
      formData: {},
      loadData: false,
      apiMethods: null,
    }
  },
  async mounted() {
    this.loadData = true

    this.apiMethods = getMethods(this.formInfo.viewname, this.apiInfo)
    this.sectionData = this.apiInfo[this.formInfo.viewname]
    if (!this.sectionData) {
      console.error(`Error getting section data for model "${this.formInfo.viewname}"`)
      return
    }

    if (this.formInfo.formType === 'update') {
      getDetail(
        this.apiMethods['retrieve'].url.replace("{id}", this.formInfo.recordId),
        this.apiMethods['retrieve'].methodHttp,
        this.sectionData
      ).then(response => {
        this.formData = response
        for (const [field_slug, field] of Object.entries(this.sectionData.meta.serializer)) {
          if (field.type === 'datetime' && this.formData[field_slug]) {
            this.$set(this.formData, field_slug, new Date(this.formData[field_slug]))
          }
          else if (field.type === 'choice' && this.formData[field_slug]) {
            if (!field.read_only)
              this.$set(this.formData, field_slug, this.formData[field_slug].value || this.formData[field_slug])
            else
              this.$set(this.formData, field_slug, this.formData[field_slug].text || this.formData[field_slug].value)
          }
          else if (field.type === 'multiple choice' && this.formData[field_slug]) {
            let data = []
            this.formData[field_slug].forEach(element => {
              data.push(element.value)
            });
            this.formData[field_slug] = data;
          }
          else if (field.type === 'json' && this.formData[field_slug] && typeof this.formData[field_slug] === "object") {
            this.formData[field_slug] = JSON.stringify(this.formData[field_slug])
          }
        }

        this.loadData = false
        this.$refs.fieldscontainer.updateFormData(this.formData)
      }).catch(error => {
        this.loadData = false
        if (error.response && error.response.status === 404) {
          this.$router.push({ path: '/404' })
        }
        console.error('Get detail error:', error)
        Message({ message: error, type: 'error', duration: 5 * 1000 })
      })
    } else {
      this.loadData = false
      for (const [field_slug, field] of Object.entries(this.sectionData.meta.serializer)) {
        if (field.type === 'list' && !this.formData[field_slug]) {
          this.formData[field_slug] = []
        }
      }
    }
  },
  methods: {
    _updateFormData(formData) {
      this.formData = formData
    },
    canAdd() {
      if (this.formInfo.formType === 'create')
          return 'create' in this.apiMethods
      else
          return 'update' in this.apiMethods
    },
    getTitle() {
      if (this.formInfo.formType === 'create') {
        return this.$t('create_title').replace('{title}', this.sectionData.title)
      } else {
        return this.$t('edit_title').replace('title', this.sectionData.title).replace('{id}'. this.formInfo.recordId)
      }
    },
    getActionButtonTitle() {
      if (this.formInfo.formType === 'create') {
        return this.$t('create')
      } else {
        return this.$t('refresh')
      }
    },
    send() {
      this.$refs.fieldscontainer.updateErrors({})

      this.loadData = true

      let newData = JSON.parse(JSON.stringify(this.formData))
      for (const [field_slug, field] of Object.entries(this.sectionData.meta.serializer)) {
        if (field.type === 'json' && newData[field_slug] && typeof newData[field_slug] !== 'object') {
          try {
            newData[field_slug] = JSON.parse(newData[field_slug])
          } catch (e) {
            const error = `JSON ${field_slug} error: ${e}`
            Message({ message: error, type: 'error', duration: 3 * 1000 })
            console.error(error, newData[field_slug])
            this.loadData = false
            return
          }
        }
        else if (['image upload', 'file upload'].indexOf(field.type) >= 0) {
          if (newData[field_slug] && !newData[field_slug].includes('base64')) {
            delete newData[field_slug]
          }
        }
      }

      let method = this.formInfo.formType === 'create' ? 'create' : 'partial_update'
      sendData(
        this.apiMethods[method].url.replace("{id}", this.formInfo.recordId),
        this.apiMethods[method].methodHttp,
        newData,
        this.formInfo.relationNameFilter,
        this.formInfo.filterId,
      ).then(response => {
        if (response) {
          let message = null
          if (this.formInfo.formType == 'update') {
            message = this.$t('record_updated').replace('{id}', response.id)
          } else message = this.$t('record_created').replace('{id}', response.id)
          Message({ message: message, type: 'success', duration: 5 * 1000 })
        }
        this.$emit('close', response)
        this.$destroy();
      }).catch(error => {
        this.loadData = false
        if (error.response) {
          this.$refs.fieldscontainer.updateErrors(error.response.data)

          Message({ message: this.$t('fix_errors'), type: 'error', duration: 3 * 1000 })
        } else {
          Message({ message: error, type: 'error', duration: 3 * 1000 })
        }
      })
    },
    sendAction() {
      this.$refs.fieldscontainer.$refs.form.validate().then(valid => {
        this.send();
      }).catch(error => {
        Message({ message: this.$t('fix_errors'), type: 'error', duration: 1500 })
      })
    },
    handleClose() {
      this.$confirm(this.$t('close_form')).then(_ => {
        this.$emit('close', null)
        this.$destroy();
        done()
      }).catch(_ => {})
    },
  }
}
</script>
