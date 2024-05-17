<template>
  <div class="edit-page">
    <v-card>
      <div class="d-flex flex-row">
        <v-tabs
          v-model="tab"
          direction="vertical"
        >
          <v-tab
            :text="$t('general')"
            value="general"
            v-if="isDisplayMainTab()"
          ></v-tab>

          <template v-for="(method, methodName) in apiMethods">
            <v-tab
              v-if="method.inline_type"
              :text="method.name"
              :value="method.name"
              :prepend-icon="method.icon"
            >
            </v-tab>
          </template>

          <template v-for="relationData in sectionData.meta.related_inlines">
            <v-tab
              :text="relationData.title"
              :value="relationData.inline_slug"
              :prepend-icon="relationData.icon"
            >
            </v-tab>
          </template>
        </v-tabs>

        <v-tabs-window v-model="tab" class="edit-tabs h-screen w-100">

          <!-- Main tab -->
          <v-tabs-window-item value="general">
            <FieldsContainer
              ref="fieldscontainer"
              formType="edit"
              :api-info="apiInfo"
              :viewname="viewname"
              :loading="loading"
            />
          </v-tabs-window-item>

          <!-- Inlines non ORM -->
          <template v-for="(method, methodName) in apiMethods">
            <v-tabs-window-item
              v-if="method.inline_type"
              :value="method.name"
            >
              <component
                :is="getInlineComponent(method)"
              />
            </v-tabs-window-item>
          </template>

          <!-- Inline with ORM -->
          <template v-for="relationData in sectionData.meta.related_inlines">
            <v-tabs-window-item
              v-if="relationData.inline_slug"
              :value="relationData.inline_slug"
            >
              TODO RELATED
            </v-tabs-window-item>
          </template>

        </v-tabs-window>
      </div>
    </v-card>
  </div>
</template>

<script>
import { getMethods } from '/src/api/scheme'
import { getDetail } from '/src/api/getDetail'

import ChartInline from '/src/components/inlines/Chart.vue'
import TableInline from '/src/components/inlines/Table.vue'

export default {
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
      tab: null,
      apiMethods: null,
      sectionData: null,
      loading: true,
    }
  },
  async created() {
    this.apiMethods = getMethods(this.viewname, this.apiInfo)
    if (!this.apiMethods) {
      console.error(`getMethods return null for viewname:"${this.viewname}"`)
    }
    this.sectionData = this.apiInfo[this.viewname]

    this.deserializeQuery()

    if (!this.isDisplayMainTab() && this.currentTab == null) {
      const method = Object.keys(this.apiMethods)[0]
      this.currentTab = method
    }
    this.retrieveData()
  },
  methods: {
    getInlineComponent(method) {
      if (method.inline_type === 'table') return TableInline
      if (method.inline_type === 'graph') return ChartInline
      console.error(`Inline not found for inline_type "${method.inline_type}"`)
    },
    isDisplayMainTab() {
      return this.sectionData && this.sectionData.meta && this.sectionData.meta.filds_list
    },
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
    retrieveData() {
      this.loading = true
      const method = this.apiMethods['retrieve']
      getDetail(method.url.replace("{id}", this.id),
        method.methodHttp,
        this.sectionData
      ).then(response => {
        this.formData = response
        this.loading = false
        this.$refs.fieldscontainer.updateFormData(this.formData)
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
