<template>
  <div class="edit-page">

    EDIT TODO

  </div>
</template>

<script>
import ModelForm from '/src/components/ModelForm.vue'

export default {
  components: {
    ModelForm
  },
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},

    group: {type: String, required: false},
    viewname: {type: String, required: false},
    id: {type: String, required: false},
    inline: {type: Boolean, required: false},
    mode: {type: String, required: false},
  },
  data() {
    return {
      apiMethods: null,
      sectionData: null,
    }
  },
  async created() {
    this.apiMethods = getMethods(this.formInfo.viewname, this.apiInfo)
    if (!this.apiMethods) {
      console.error(`getMethods return null for viewname:"${this.formInfo.viewname}"`)
    }
    this.sectionData = this.apiInfo[this.formInfo.viewname]

    this.deserializeQuery()

    if (!this.isDisplayMainTab() && this.currentTab == null) {
      const method = Object.keys(this.apiMethods)[0]
      this.currentTab = method
    }
  },
  methods: {
    deserializeQuery() {
      const tab = this.inline ? this.$route.query.inlineTab : this.$route.query.tab
      if (tab) {
        this.currentTab = tab
      }
    },
    serializeQuery() {
      let newQuery = JSON.parse(JSON.stringify(this.$route.query))

      delete newQuery.inlineTab
      if (this.currentTab) {
        if (this.inline) {
          newQuery.inlineTab = this.currentTab
        }
        else {
          newQuery.tab = this.currentTab
        }
      }

      this.$router.replace({name: this.$route.name, query: newQuery})
    },
  },
  gotoList() {
    // TODO
  }
}
</script>
