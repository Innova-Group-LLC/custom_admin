<template>
  <div :class="{ 'edit-content': true, 'inline-view': inline }">
    <v-card>
      <div class="edit-card-container">
        <v-tabs
          v-model="currentTab"
          :direction="inline ? 'horizontal' : 'vertical'"
          @update:modelValue="updateTab"
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

        <v-tabs-window
          v-model="currentTab"
          class="edit-page-tabs"
        >

          <!-- Main tab -->
          <v-tabs-window-item
            v-if="isDisplayMainTab()"
            value="general"
            transition="fade"
            reverse-transition="fade"
          >
            <ModelFormUpdate
              :api-info="apiInfo"
              :viewname="viewname"
              :id="id"
              :group="group"

              @closed="modelFormClosed"
            />
          </v-tabs-window-item>

          <!-- Inlines non ORM -->
          <template v-for="(method, methodName) in apiMethods">
            <v-tabs-window-item
              v-if="method.inline_type"
              :value="method.name"
              transition="fade"
              reverse-transition="fade"
            >
              <component
                v-if="getInlineComponent(method)"
                :is="getInlineComponent(method)"

                :id="id"
                :method="method"
                :settings="settings"
              />
              <template v-else>
                Component not found for {{ method }}
              </template>
            </v-tabs-window-item>
          </template>

          <!-- Inline with ORM -->
          <template v-for="relationData in sectionData.meta.related_inlines">
            <v-tabs-window-item
              v-if="relationData.inline_slug"
              :value="relationData.inline_slug"
              transition="fade"
              reverse-transition="fade"
            >

              <List
                v-if="relationData.back_relation_name"
                :api-info="apiInfo"
                :viewname="relationData.viewset_name"
                :settings="settings"
                :relation-name-filter="relationData.back_relation_name"
                :filterId="id"
              />
              <Edit
                v-else
                :settings="settings"
                :viewname="relationData.viewset_name"
                :api-info="apiInfo"
                :id="id"
                :inline="true"
                mode="update"
              />

            </v-tabs-window-item>
          </template>

        </v-tabs-window>
      </div>
    </v-card>
  </div>
</template>

<script>
import { getMethods } from '/src/api/scheme'

import ModelFormUpdate from '/src/components/ModelFormUpdate.vue'
import ChartInline from '/src/components/inlines/Chart.vue'
import TableInline from '/src/components/inlines/Table.vue'

export default {
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},

    // If its inside inline
    inline: {type: Boolean, required: false},

    group: {type: String, required: false},
    viewname: {type: String, required: false},
    id: {type: String, required: false},
    mode: {type: String, required: false},
  },
  components: {
    ModelFormUpdate,
  },
  data() {
    return {
      currentTab: null,
      apiMethods: null,
      sectionData: null,
    }
  },
  created() {
    this.apiMethods = getMethods(this.viewname, this.apiInfo)
    this.sectionData = this.apiInfo[this.viewname]

    this.deserializeQuery()
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
    updateTab() {
      this.serializeQuery()
    },
    modelFormClosed() {
      const list_url = `/${this.group}/${this.viewname}/list`
      this.$router.push({ path: list_url })
    },
  },
}
</script>
