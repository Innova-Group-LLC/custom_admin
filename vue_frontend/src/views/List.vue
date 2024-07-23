<template>
  <div class="list-page" v-if="sectionData">

    <div class="list-above-block">

      <div class="header-row-filters">
        <Filters
          :filterset-fields="sectionData.meta.filterset_fields"
          :search-fields="sectionData.meta.search_fields"
          :filter-info-init="filterInfo"
          :settings="settings"
          :viewname="viewname"
          @filtered="handleFilter"
        />
      </div>

      <div class="header-row-actions">
        <div class="table-button">
          <ModelFormCreate
            v-if="canAdd()"
            :api-info="apiInfo"

            :viewname="viewname"
            :relation-name-filter="relationNameFilter"
            :filter-id="filterId"

            @created="createdEvent"
          />
        </div>
        <div class="table-button">
          <PageSettings
            :api-info="apiInfo"
            :viewname="viewname"
            @changed="settingsChanged"
          />
        </div>
      </div>

    </div>

    <v-data-table
      class="model-table"
      color="primary"

      v-model="selected"
      :items="pageData.data || []"
      :headers="headers"
      :loading="listLoading"
      :show-select="true"

      :items-per-page="pageInfo.limit"
      :page="pageInfo.page"

      @update:sortBy="updateSortBy"
      @click:row="clickRow"
    >
      <template
        v-for="(header, index) in headers"
        v-slot:[`item.${header.key}`]="{ item }"
      >

        <div @click="handleClick(index, item)" :class="{ 'table-cell': true, 'table-link': index === 0 && canRetrieve() }">

          <template v-if="header.field.type === 'primary'">
            <v-tooltip v-if="item[header.key]">
              #{{ item[header.key].pk }}
              <template v-slot:activator="{ props }">
                <v-chip size="small" v-bind="props">{{ item[header.key].text }}</v-chip>
              </template>
            </v-tooltip>
          </template>

          <template v-else-if="header.field.type === 'primarymany'">
            <template v-if="item[header.key]">
              <v-chip v-for="tag in item[header.key]" size="small">{{ tag.text }}</v-chip>
            </template>
          </template>

          <template v-else-if="header.field.type === 'boolean'">
            <v-icon color="green-darken-2" icon="mdi-check" size="small" v-if="item[header.key]"/>
            <v-icon color="red-darken-2" icon="mdi-close" size="small" v-else/>
          </template>

          <template v-else-if="header.field.type === 'choice'">
            <template v-if="item[header.key]">
              <template v-if="Object.keys(header.field.tag_style || {}).length > 0">
                <v-chip
                  size="small"
                  :color="header.field.tag_style[item[header.key]]"
                >{{ getChoiceTitle(item, header) }}</v-chip>
              </template>
              <template v-else>
                {{ getChoiceTitle(item, header) }}
              </template>
            </template>
          </template>

          <template v-else-if="header.field.type === 'datetime'">
            <span class="cell-string">{{ formatDateTime(item[header.key]) }}</span>
          </template>

          <template v-else-if="header.field.type === 'image upload' && header.field.list_preview">
            <v-img
              v-if="item[header.key] && item[header.key].url"
              class="image-preview"
              width="100"
              max-height="100"
              cover
              :src="item[header.key].url"
            />
          </template>

          <template v-else-if="header.field.type === 'file upload'">
            <span class="cell-string" v-if="item[header.key]">{{ item[header.key].name }}</span>
            <span class="cell-string" v-else>{{ item[header.key] }}</span>
          </template>

          <template v-else>
            <div :class="header.field.type" style="display: none" />
            <span class="cell-string">{{ item[header.key] }}</span>
          </template>
        </div>
      </template>

      <template v-slot:bottom></template>

      <template v-slot:header.data-table-select="{ on, props }">
        <v-tooltip :text="`${$t('applyToAllRecords')} ${getTotalCount()}`">
          <template v-slot:activator="{ props }">
            <div v-bind="props" class="select-to-all">
              <v-checkbox
                v-model="actionToAll"
                color="var(--color-darken-2)"
                density="compact"
              />
            </div>
          </template>
        </v-tooltip>
      </template>

    </v-data-table>

    <div class="table-bottom">

      <div class="table-bottom-cell" v-if="hasActons()">
        <v-label class="info">{{ $t('selected') }} <p class="selected-count">{{ getSelectedCount()}}/{{ getTotalCount() }}</p></v-label>
      </div>

      <div class="table-bottom-cell actions-cell">
        <template
          v-for="(action_info, key) in this.sectionData.meta.actions"
        >
          <v-btn
            size="small"
            class="action-button"
            :variant="action_info.variant || 'flat'"
            :prepend-icon="action_info.icon"
            :base-color="action_info.base_color || 'secondary'"
            @click="pressAction(action_info, key)"
          >
            {{ action_info.name }}
          </v-btn>
        </template>
      </div>

      <div class="table-bottom-cell">

        <v-tooltip location="start" :text="$t('itemsPerPage')">
          <template v-slot:activator="{ props }">
            <div v-bind="props">
              <v-select
                class="list-pagination-per-page"
                v-model="pageInfo.limit"
                :items="perPageOptions"
                @update:modelValue="changePagination"
              ></v-select>
            </div>
          </template>
        </v-tooltip>

        <v-label class="info">{{ getTotalCount() }}</v-label>

        <v-pagination
          class="list-pagination"
          v-model="pageInfo.page"
          :length="getLength()"
          :total-visible="5"
          size="40"
          @update:modelValue="changePagination"
        ></v-pagination>
      </div>

    </div>

    <v-dialog v-model="actionDialogConfirmation" max-width="500">
      <v-card>

        <v-card-title class="d-flex justify-space-between align-center">
          <span>{{ $t('confirmation') }}: {{ getActionInfo().name }}</span>

          <v-btn
            icon="mdi-close"
            variant="text"
            density="compact"
            @click="actionDialogConfirmation = false"
          ></v-btn>
        </v-card-title>

        <v-card-text>
          <p>{{ getActionInfo().confirmation_text }}</p>
          <v-label class="info">{{ $t('selected') }} <p class="selected-count">{{ getSelectedCount()}}/{{ getTotalCount() }}</p></v-label>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn :text="$t('cancel')" variant="elevated" @click="actionDialogConfirmation = false"></v-btn>
          <v-btn :text="$t('confirm')" variant="tonal" color="primary" @click="applyAction"></v-btn>
        </v-card-actions>

      </v-card>
    </v-dialog>

    <v-dialog persistent v-model="actionFormDialogOpen" max-width="1200">
      <v-card>

        <v-card-title class="d-flex justify-space-between align-center">
          <span>{{ getActionInfo().name }}</span>

          <v-btn
            icon="mdi-close"
            variant="text"
            density="compact"
            @click="actionFormDialogOpen = false"
          ></v-btn>
        </v-card-title>

        <div class="action-description" v-html="getActionInfo().description"></div>

        <FieldsContainer
          ref="fieldscontainer"
          formType="create"
          :api-info="apiInfo"
          :form-serializer="getActionInfo().form_serializer"
          :loading="actionLoading"
          :action-name="actionSelected"

          @changed="value => actionFormData = value"
        />

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn :text="$t('cancel')" variant="elevated" @click="actionFormDialogOpen = false"></v-btn>
          <v-btn :text="$t('send')" variant="tonal" color="primary" @click="applyAction"></v-btn>
        </v-card-actions>

      </v-card>
    </v-dialog>

    <v-dialog v-model="persistentMessageDialog" max-width="1200">
      <v-card>

        <v-card-text v-html="persistentMessage"></v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn :text="$t('close')" variant="elevated" @click="persistentMessageDialog = false"></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script>
import { getViewsetsSettings } from '/src/utils/settings'
import moment from 'moment'
import { toast } from "vue3-toastify"
import { getMethods } from '/src/api/scheme'
import { getList } from '/src/api/getList'
import { getSettings, setSettings, config_dataset } from '/src/utils/settings'
import { sendAction, downloadContent } from '/src/api/sendAction'

import ModelFormCreate from '/src/components/ModelFormCreate.vue'
import PageSettings from '/src/components/PageSettings.vue'
import Filters from '/src/components/Filters.vue'

export default {
  components: {
    ModelFormCreate,
    Filters,
    PageSettings,
  },
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},

    viewname: {type: String, required: false},
    group: {type: String, required: false},
    relationNameFilter: {type: String, required: false},
    filterId: {type: String, required: false},
  },
  watch: {
    $route: {
      immediate: true,
      handler(to, from) {
        const title = (this.apiInfo[this.viewname] || {}).title
        document.title = `${title} | ${config_dataset.title}`
      }
    },
  },
  data() {
    return {
      selected: [],
      headers: {},
      perPageOptions: [25, 50, 100, 150],
      listLoading: false,
      pageData: {
        data: null,
        count: null
      },
      pageInfo: null,
      ordering: null,
      filterInfo: {
        search: null,
        filters: {},
      },
      sectionData: null,
      apiMethods: null,

      actionToAll: false,
      actionFormData: null,
      actionDialogConfirmation: false,
      actionFormDialogOpen: false,
      actionSelected: null,
      actionLoading: false,

      persistentMessageDialog: false,
      persistentMessage: null,
    }
  },
  created() {
    this.pageInfo = {
      page: 1,
      limit: getSettings().page_size || 25,
    }

    this.apiMethods = getMethods(this.viewname, this.apiInfo)

    this.sectionData = this.apiInfo[this.viewname]
    if (!this.sectionData) {
      console.error(`Page ${this.viewname} not found`)
      gthis.$router.push({ path: '/404' })
      return
    }

    this.headers = this.getHeaders()
    this.deserializeQuery()
    this.getListData()
  },
  methods: {
    deserializeQuery() {
      // Change url params only if group presented
      if (!this.group) return

      const page = this.$route.query.page
      if (page) this.pageInfo.page = parseInt(page)
      const limit = this.$route.query.limit
      if (limit) this.pageInfo.limit = parseInt(limit)

      const ordering = this.$route.query.ordering
      if (ordering) this.ordering = ordering

      // Deserialize filters
      if (this.$route.query.filter_info) {
        this.filterInfo = JSON.parse(decodeURIComponent(this.$route.query.filter_info))
      }
    },
    serializeQuery() {
      // Change url params only if group presented
      if (!this.group) return

      let newQuery = {}
      if (this.pageInfo.page) newQuery.page = this.pageInfo.page
      if (this.pageInfo.limit) newQuery.limit = this.pageInfo.limit

      if (this.ordering) newQuery.ordering = this.ordering

      // Serialize filters
      if (Object.keys(this.filterInfo).length > 0) {
        newQuery.filter_info = encodeURIComponent(JSON.stringify(this.filterInfo))
      }

      this.$router.push({name: this.$route.name, query: newQuery})
    },
    async getListData() {
      const method = this.apiMethods['list']
      if (!method) {
        console.error(`list method is not found in the list of available methods`)
        return
      }

      this.listLoading = true
      getList({
        url: method.url,
        method: method.methodHttp,
        pageInfo: this.pageInfo,
        filter_info: this.filterInfo,
        ordering: this.ordering,

        relationNameFilter: this.relationNameFilter,
        filterId: this.filterId,
      }).then(response => {
        this.pageData.data = response.results
        this.pageData.headers = response.headers
        this.pageData.count = response.count

        this.listLoading = false
      }).catch(error => {
        this.listLoading = false
        console.error('Get list error:' + error)
        toast(`Error: ${error}`, {
          "limit": 3, "theme": "auto", "type": "warning", "position": "top-center",
        })
      })
    },
    getHeader(field, name) {
      if (!this.canDisplayInList(field, name)) return

      let headerData = {
        title: field.label,
        align: field.align || 'start',
        minWidth: field.min_width || '150',
        sortable: this.sectionData.meta.ordering_fields.indexOf(name) >= 0,
        key: name,
        field: field,
      }
      if (this.isColumnFixed(name)) {
        headerData['fixed'] = true
        headerData['width'] = field.width || '150'
      }
      if (name === 'id') {
        headerData['minWidth'] = field.width || '50'
        headerData['width'] = field.width || '50'
      }
      return headerData
    },
    getHeaders() {
      let result = []

      const settings = getViewsetsSettings(this.viewname, this.sectionData.meta.serializer)

      if (!this.sectionData.meta.filds_list) {
        for (const [name, field] of Object.entries(this.sectionData.meta.serializer)) {

          if (!settings.headers[name]) continue

          const headerData = this.getHeader(field, name)
          if (headerData) result.push(headerData)
        }
        return result
      }

      for (const name of this.sectionData.meta.filds_list) {

        const field = this.sectionData.meta.serializer[name]
        if (!field) {
          console.error(`Field ${field_name} is not presented in serializer fields`)
          return
        }

        if (!settings.headers[name]) continue

        const headerData = this.getHeader(field, name)
        if (headerData) result.push(headerData)
      }
      return result
    },
    isColumnFixed(columnName) {
      return this.sectionData.meta.fixed_columns && this.sectionData.meta.fixed_columns.includes(columnName)
    },
    canDisplayInList(field, field_name) {
      if (!field.write_only && (!this.sectionData.meta.filds_list || this.sectionData.meta.filds_list.indexOf(field_name) !== -1)) {
        return true
      }
      return false
    },
    changePagination() {
      let settings = getSettings()
      settings.page_size = this.pageInfo.limit,
      setSettings(settings)

      this.selected = []
      this.serializeQuery()
      this.getListData()
    },
    getLength() {
      return Math.ceil((this.pageData.count || 0) / this.pageInfo.limit)
    },
    formatDateTime(dateString) {
      if (dateString) {
        return moment(dateString).format('YYYY-MM-DD HH:mm')
      }
    },
    canAdd() {
      return 'create' in this.apiMethods
    },
    canRetrieve() {
      return 'retrieve' in this.apiMethods
    },
    clickRow(event, row) {
      if (event.ctrlKey) {
        if (!this.selected.includes(row.item.id)) {
          this.selected.push(row.item.id)
        } else {
          this.selected.splice(this.selected.indexOf(row.item.id), 1);
        }
      }
    },
    handleClick(index, row) {
      if (index == 0 && this.canRetrieve()) {
        const pkValue = row[this.sectionData.meta.pk_name]

        if (!this.sectionData.meta.pk_name || !pkValue) {
          console.error(`PK value "${this.sectionData.meta.pk_name}" not found in row:`, row)
          return
        }

        const edit_url = `/${this.sectionData.group}/${this.viewname}/${pkValue}/update`
        this.$router.push({ path: edit_url } )
      }
    },
    handleFilter(newFilterInfo) {
      this.pageInfo.page = 1
      this.filterInfo = newFilterInfo
      this.serializeQuery()
      this.getListData()
    },
    updateSortBy(options) {
      if (!options[0]) {
        this.ordering = null
      } else {
        const desc = options[0].order === 'desc'? '-' : ''
        const field_slug = options[0].key
        this.ordering = `${desc}${field_slug}`
      }

      this.serializeQuery()
      this.getListData()
    },
    hasActons() {
      return Object.keys(this.sectionData.meta.actions).length > 0
    },
    getSelectedCount() {
      if (this.actionToAll) return this.getTotalCount()
      return this.selected ? this.selected.length : 0
    },
    getTotalCount() {
      return this.pageData.count || 0
    },
    pressAction(actionInfo, actionKey) {
      if (!actionInfo.allow_empty_selection && !this.actionToAll && this.selected.length === 0) {
        toast(this.$t('actionNotAllowEmptySelection'), {
          "limit": 3, "theme": "auto", "type": "warning", "position": "top-center",
        })
        return
      }

      this.actionFormData = null
      this.actionMeta = null
      this.actionSelected = actionKey

      // Action form
      if (actionInfo.form_serializer) {
        this.actionFormDialogOpen = true
      } else {
        // Confirmation window
        if (actionInfo.confirmation_text) {
          this.actionDialogConfirmation = true
        }
        else {
          this.applyAction()
        }
      }
    },
    getActionInfo() {
      return this.sectionData.meta.actions[this.actionSelected]
    },
    applyAction() {
      this.actionLoading = false
      sendAction({
        viewname: this.viewname,
        action: this.actionSelected,
        pks: this.selected,
        formData: this.actionFormData || {},
        sendToAll: this.actionToAll,
        relationNameFilter: this.relationNameFilter,
        relfilterid: this.filterId,
      }).then(response => {

        if(response.headers['content-type'] !== 'application/json') {
          const fileName = response.headers['pragma'] || `${moment().format('DD.MM.YYYY_HH:MM')}.csv`
          downloadContent(
            response.data, fileName, response.headers['content-type']
          )
        }
        else {
          if (response.data.action_messages) {
            toast(response.data.action_messages.join('<br>'), {
              "type": "success",
              "position": "top-center",
              "dangerouslyHTMLString": true
            })
          }
          if (response.data.persistent_message) {
            this.persistentMessageDialog = true
            this.persistentMessage = response.data.persistent_message
          }
        }

        this.actionDialogConfirmation = false
        this.actionFormDialogOpen = false
        this.actionLoading = false
        this.selected = []
        this.getListData()
      }).catch(response => {
        this.actionLoading = false
        if (response.data) {
          this.$refs.fieldscontainer.updateErrors(response.data)
        }
      })
    },
    createdEvent() {
      this.deserializeQuery()
      this.getListData()
    },
    getChoiceTitle(item, header) {
      const value = item[header.key]
      if (!header.field.choices) return value

      for (const choice of header.field.choices) {
        if (choice.value === value) return choice.display_name
      }
      return value
    },
    settingsChanged() {
      this.headers = this.getHeaders()
    },
  }
}
</script>
