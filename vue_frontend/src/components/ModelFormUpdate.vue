<template>

  <div>
    <FieldsContainer
      ref="fieldscontainer"
      formType="edit"
      :api-info="apiInfo"
      :viewname="viewname"
      :loading="loading"

      @changed="value => formData = value"
    />

    <div class="model-form-bottom-actions">
      <v-btn
        v-if="canUpdate()"
        :text="$t('update')"
        variant="elevated"
        color="primary"
        @click="updateModel"
      />
    </div>
  </div>

</template>

<script>
import { getMethods } from '/src/api/scheme'
import { getDetail } from '/src/api/getDetail'
import { sendData } from '/src/api/sendData'
import { toast } from "vue3-toastify"

export default {
  props: {
    apiInfo: {type: Object, required: true},
    viewname: {type: String, required: true},
    group: {type: String, required: false},
    id: {type: String, required: true},
  },
  emits: ["closed"],
  data() {
    return {
      apiMethods: null,
      loading: true,
      formData: {},
    }
  },
  async created() {
    this.apiMethods = getMethods(this.viewname, this.apiInfo)
    this.retrieveData()
  },
  methods: {
    retrieveData() {
      const method = this.apiMethods['retrieve']
      if (!method) {
        console.error(`retrieve method is not found in the list of available methods`)
        return
      }

      this.loading = true
      getDetail(method.url.replace("{id}", this.id),
        method.methodHttp,
        this.sectionData
      ).then(response => {
        this.loading = false
        this.formData = response.data
        this.$refs.fieldscontainer.updateFormData(response.data)
      }).catch(error => {
        this.loading = false
        if (error.response && error.response.status === 404) {
          this.$router.push({ path: '/404' })
        }
        console.error('Get detail error:', error)
        toast(error, {
          "theme": "auto",
          "type": "error",
          "position": "top-center",
          "dangerouslyHTMLString": true
        })
      })
    },
    canUpdate() {
      return this.apiMethods['partial_update'] !== undefined
    },
    updateModel() {
      let method = this.apiMethods['partial_update']
      if (!method) {
        console.error(`partial_update method is not found in the list of available methods`)
        return
      }

      this.$refs.fieldscontainer.updateErrors({})
      this.loading = true
      sendData(
        method.url.replace("{id}", this.id),
        method.methodHttp,
        this.formData,
      ).then(response => {
        this.loading = false
        if (response) {
          let message = this.$t('modelUpdated').replace('{id}', response.id)
          toast(message, {"theme": "auto", "type": "success", "position": "top-center"})
        }
        this.$emit('closed')
      }).catch(error => {
        this.loading = false
        if (error.response) {
          this.$refs.fieldscontainer.updateErrors(error.response.data)
          toast(this.$t('fixErrors'), {"theme": "auto", "type": "error", "position": "top-center"})
          return
        }
        toast(error, {"theme": "auto", "type": "error", "position": "top-center"})
      })
    },
  },
}
</script>
