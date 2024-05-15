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
          <v-tabs-window-item value="general">
            <FieldsContainer
              ref="fieldscontainer"
              formType="create"
              :api-info="apiInfo"
              :viewname="viewname"
            />
          </v-tabs-window-item>

          <v-tabs-window-item value="option-2">
            <v-card flat>
              <v-card-text>
                <p>
                  Morbi nec metus. Suspendisse faucibus, nunc et pellentesque egestas, lacus ante convallis tellus, vitae iaculis lacus elit id tortor. Sed mollis, eros et ultrices tempus, mauris ipsum aliquam libero, non adipiscing dolor urna a orci. Curabitur ligula sapien, tincidunt non, euismod vitae, posuere imperdiet, leo. Nunc sed turpis.
                </p>

                <p>
                  Suspendisse feugiat. Suspendisse faucibus, nunc et pellentesque egestas, lacus ante convallis tellus, vitae iaculis lacus elit id tortor. Proin viverra, ligula sit amet ultrices semper, ligula arcu tristique sapien, a accumsan nisi mauris ac eros. In hac habitasse platea dictumst. Fusce ac felis sit amet ligula pharetra condimentum.
                </p>

                <p>
                  Sed consequat, leo eget bibendum sodales, augue velit cursus nunc, quis gravida magna mi a libero. Nam commodo suscipit quam. In consectetuer turpis ut velit. Sed cursus turpis vitae tortor. Aliquam eu nunc.
                </p>

                <p>
                  Etiam ut purus mattis mauris sodales aliquam. Ut varius tincidunt libero. Aenean viverra rhoncus pede. Duis leo. Fusce fermentum odio nec arcu.
                </p>

                <p class="mb-0">
                  Donec venenatis vulputate lorem. Aenean viverra rhoncus pede. In dui magna, posuere eget, vestibulum et, tempor auctor, justo. Fusce commodo aliquam arcu. Suspendisse enim turpis, dictum sed, iaculis a, condimentum nec, nisi.
                </p>
              </v-card-text>
            </v-card>
          </v-tabs-window-item>

          <v-tabs-window-item value="option-3">
            <v-card flat>
              <v-card-text>
                <p>
                  Fusce a quam. Phasellus nec sem in justo pellentesque facilisis. Nam eget dui. Proin viverra, ligula sit amet ultrices semper, ligula arcu tristique sapien, a accumsan nisi mauris ac eros. In dui magna, posuere eget, vestibulum et, tempor auctor, justo.
                </p>

                <p class="mb-0">
                  Cras sagittis. Phasellus nec sem in justo pellentesque facilisis. Proin sapien ipsum, porta a, auctor quis, euismod ut, mi. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nam at tortor in tellus interdum sagittis.
                </p>
              </v-card-text>
            </v-card>
          </v-tabs-window-item>
        </v-tabs-window>
      </div>
    </v-card>
  </div>
</template>

<script>
import { getMethods } from '/src/api/scheme'

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
  },
  methods: {
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
  },
  gotoList() {
    // TODO
  }
}
</script>
