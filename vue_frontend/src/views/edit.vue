<template>
  <div v-if="apiMethods" class="edit-container">

    <template v-if="mode == 'update'">
      <el-tabs
        :type="inline ? '' : 'border-card'"
        @tab-click="openInline"
        v-model="currentTab"
        :tab-position="inline ? 'top' : 'right'"
        class="edit-page-tabs"
        :class="{ 'inline-tabs': inline}"
        :before-leave="beforeLeave"
      >
        <el-tab-pane
          class="model-form-tab"
          :label="$t('main')"
          v-if="isDisplayMainTab(formInfo.viewname)"
          lazy
        >
          <modelform
            :form-info="formInfo"
            :api-info="apiInfo"
            :settings="settings"
            @close="handleCloseCreateForm"
          />
        </el-tab-pane>

        <template v-for="(method, methodName) in apiMethods">
          <el-tab-pane
            v-if="method.inline_type"
            :label="method.name"
            :key="method.name"
            :name="methodName"
            lazy
          >
            <inlinetable
              v-if="method.inline_type === 'table'"
              :method="method"
              :id="id"
              :settings="settings"
              :ref="'tab'"
            />
            <inlinegraph
              v-else-if="method.inline_type === 'graph'"
              :method="method"
              :id="id"
              :settings="settings"
              :ref="'tab'"
            />
            <template v-else>
              method: {{ method }}
            </template>
          </el-tab-pane>
        </template>

        <el-tab-pane
          v-for="relationData in sectionData.meta.related_inlines"
          :label="relationData.title"
          :key="relationData.inline_slug"
          :name="relationData.inline_slug"
          lazy
        >
          <list
            :viewname="relationData.viewset_name"
            :settings="settings"
            :api-info="apiInfo"
            :relation-name-filter="relationData.back_relation_name"
            :filterId="id"
            v-if="relationData.back_relation_name"
            :ref="'tab'"
          />
          <edit
            :settings="settings"
            :viewname="relationData.viewset_name"
            :api-info="apiInfo"
            :id="id"
            :inline="true"
            mode="update"
            v-else
            :ref="'tab'"
          />
        </el-tab-pane>

      </el-tabs>
    </template>

    <template v-else>
      <modelform
        :form-info="formInfo"
        :api-info="apiInfo"
        :settings="settings"
        @close="handleCloseCreateForm"
      />
    </template>
  </div>
</template>

<script>
import { parseTime } from '@/utils'
import ModelForm from '@/components/model-form'
import { getMethods } from '@/api/scheme'
import List from '@/views/list'
import InlineTable from '@/components/inlines/inline-table'
import InlineGraph from '@/components/inlines/inline-graph'

export default {
  name: 'ComplexTable',
  components: {
    "modelform": ModelForm,
    "list": List,
    "edit": () => import('@/views/edit'),

    "inlinetable": InlineTable,
    "inlinegraph": InlineGraph,
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
      currentTab: null,
      formInfo: {
        formType: this.mode,
        recordId: this.id,
        viewname: this.viewname,
        showTitle: false,
        apiMethods: null,
      },
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
    beforeLeave(activeName, oldActiveName) {
      // const oldTab = this.$refs[`tab`]
      // if (oldTab) {
      //   oldTab[0].$destroy()
      // }
      this.currentTab = null
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
    openInline(tab, event) {
      this.serializeQuery()
    },
    handleCloseCreateForm(response) {
      if (window.history.length > 2) {
        this.$router.go(-1)
        return
      }

      const list_url = `${this.group}/${this.viewname}/list`
      this.$router.push({ path: list_url, query: this.$route.query })
    }
  }
}
</script>
