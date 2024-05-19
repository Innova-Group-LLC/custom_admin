<template>

  <FieldsContainer
    ref="fieldscontainer"
    formType="edit"
    :api-info="apiInfo"
    :viewname="viewname"
    :loading="loading"
  />

</template>

<script>
import { getMethods } from '/src/api/scheme'
import { getDetail } from '/src/api/getDetail'
import { toast } from "vue3-toastify"

export default {
  props: {
    apiInfo: {type: Object, required: true},
    viewname: {type: String, required: true},
    group: {type: String, required: false},
    id: {type: String, required: true},
  },
  data() {
    return {
      apiMethods: null,
      loading: true,
    }
  },
  async created() {
    this.apiMethods = getMethods(this.viewname, this.apiInfo)
    this.retrieveData()
  },
  methods: {
    retrieveData() {
      this.loading = true
      const method = this.apiMethods['retrieve']
      if (!method) {
        console.error(`${this.viewname} apiMethods is not contain retrieve method`)
      }
      getDetail(method.url.replace("{id}", this.id),
        method.methodHttp,
        this.sectionData
      ).then(response => {
        this.loading = false
        this.$refs.fieldscontainer.updateFormData(response)
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
    }
  },
}
</script>
