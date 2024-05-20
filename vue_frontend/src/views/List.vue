<template>
  <div class="list-page">

    <div class="list-above-block">

      <div class="header-row-filters">
        <Filters
          :filterset-fields="apiInfo[viewname].meta.filterset_fields"
          :search-fields="apiInfo[viewname].meta.search_fields"
          :filter-info-init="filterInfo"
          :settings="settings"
          @filtered="handleFilter"
        />
      </div>

      <div class="header-row-actions">
        <Create
          v-if="canAdd()"
          :api-info="apiInfo"

          :viewname="viewname"
          :relation-name-filter="relationNameFilter"
          :filter-id="filterId"
        />
      </div>

    </div>

    <v-data-table
      class="model-table"
      :items="pageData.data || []"
      :headers="headers"
      :loading="listLoading"
      :show-select="true"

      :items-per-page="pageInfo.limit"
      :page="pageInfo.page"

      @click:row="handleClick"
    >

      <template
        v-for="header in headers"
        v-slot:[`item.${header.key}`]="{ item }">

        <template v-if="header.field.type === 'primary'">
          <v-tooltip v-if="item[header.key]">
            #{{ item[header.key].id }}
            <template v-slot:activator="{ props }">
              <v-chip size="small" v-bind="props">{{ item[header.key].text }}</v-chip>
            </template>
          </v-tooltip>
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
                :color="header.field.tag_style[item[header.key].value]"
              >{{ item[header.key].text }}</v-chip>
            </template>
            <template v-else>
              {{ item[header.key].text }}
            </template>
          </template>
        </template>

        <template v-else-if="header.field.type === 'datetime'">
          {{ formatDateTime(item[header.key]) }}
        </template>

        <template v-else>
          <span class="cell-string">{{ item[header.key] }}</span>
        </template>
      </template>

      <template v-slot:bottom>
        <div class="table-bottom">

          <v-row justify="end" no-gutters>
            <v-select
              class="list-pagination-per-page"
              v-model="pageInfo.limit"
              :items="perPageOptions"
              @update:modelValue="changePagination"
            ></v-select>

            <v-pagination
              class="list-pagination"
              v-model="pageInfo.page"
              :length="getLength()"
              :total-visible="6"
              size="40"
              @update:modelValue="changePagination"
            ></v-pagination>
          </v-row>

        </div>
      </template>

    </v-data-table>

  </div>
</template>

<script>
import moment from 'moment'
import { getMethods } from '/src/api/scheme'
import { getList } from '/src/api/getList'
import { getSettings, setSettings } from '/src/utils/settings'

import Create from '/src/components/Create.vue'
import Filters from '/src/components/Filters.vue'

export default {
  components: {
    Create,
    Filters,
  },
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},

    viewname: {type: String, required: false},
    group: {type: String, required: false},
    relationNameFilter: {type: String, required: false},
    filterId: {type: String, required: false},
  },
  data() {
    return {
      headers: {},
      perPageOptions: [25, 50, 100, 150],
      listLoading: true,
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

      selectedAction: null,
      actionToAll: false,
      actionDialog: {
        visible: false,
        formData: {},
        actionInfo: {},
        meta: {},
        title: null,
        loading: false,
      },
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
      console.error(`Page ${this.viewname} not found in ${Object.keys(this.apiInfo)}`)
      this.$router.push({ path: '/404' })
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

      const search = this.$route.query.search
      if (search) this.filterInfo.search = search

      for (const [filter_name, filter] of Object.entries(this.apiInfo[this.viewname].meta.filterset_fields)) {
        if (['DateTimeField', 'DateFromToRangeFilter'].indexOf(filter.type) >= 0) {
          const filter_after = this.$route.query[`${filter_name}_after`]
          if (filter_after)
            this.filterInfo.filters[`${filter_name}_after`] = filter_after

          const filter_before = this.$route.query[`${filter_name}_before`]
          if (filter_before)
            this.filterInfo.filters[`${filter_name}_before`] = filter_before
        }
        else {
          const filter_value = this.$route.query[filter_name]
          if (filter_value != null && filter_value != undefined)
            this.$set(this.filterInfo.filters, filter_name, filter_value)
        }
      }
    },
    serializeQuery() {
      // Change url params only if group presented
      if (!this.group) return

      let newQuery = {}
      if (this.pageInfo.page) newQuery.page = this.pageInfo.page
      if (this.pageInfo.limit) newQuery.limit = this.pageInfo.limit

      if (this.ordering) newQuery.ordering = this.ordering
      if (this.filterInfo.search) newQuery.search = this.filterInfo.search

      for (const [filter_name, filter_value] of Object.entries(this.filterInfo.filters)) {
        if (filter_value)
          newQuery[filter_name] = filter_value
      }

      this.$router.push({name: this.$route.name, query: newQuery})
    },
    async getListData() {
      this.listLoading = true
      getList({
        url: this.apiMethods['list'].url,
        method: this.apiMethods['list'].methodHttp,
        pageInfo: this.pageInfo,
        filters: this.filterInfo.filters,
        search: this.filterInfo.search,
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
        // Message({ message: error, type: 'error', duration: 5 * 1000 })
      })
    },
    getHeaders() {
      let result = []

      for (const name of this.sectionData.meta.filds_list) {

        const field = this.sectionData.meta.serializer[name]
        if (!field) {
          console.error(`Field ${field_name} is not presented in serializer fields`)
          return
        }

        if (this.canDisplayInList(field, name)) {
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
          result.push(headerData)
        }
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

      this.serializeQuery()
      this.getListData()
    },
    getLength() {
      return parseInt((this.pageData.count || 0) / this.pageInfo.limit)
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
    clickRow(row, column, event) {
      if (column.label && column.label.toLowerCase() === 'id') {
        if (this.canRetrieve())
          this.openDetail(this.viewname, row.id)
      }
    },
    handleClick(click, row) {
      const edit_url = `/${this.sectionData.group}/${this.viewname}/${row.item.id}/update`
      this.$router.push({ path: edit_url } )
    },
    handleFilter(newFilterInfo) {
      this.pageInfo.page = 1
      this.filterInfo = newFilterInfo
      this.serializeQuery()
      this.getListData()
    },
  }
}
</script>
