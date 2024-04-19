<template>
  <div class="list-page-container">
    <div v-if="sectionData">

      <filters
        @filtered="handleFilter"
        :filterset-fields="apiInfo[viewname].meta.filterset_fields"
        :search-fields="apiInfo[viewname].meta.search_fields"
        :filter-info-init="filterInfo"
        :ref="`filter_${viewname}`"
        :settings="settings"
      />

      <el-button
        v-if="sectionData && canAdd()"
        class="list-button"
        style="float: right;"
        type="primary"
        icon="el-icon-edit"
        @click="handleCreate"
      >{{ $t('add') }}</el-button>

      <el-table
        ref="table"
        :key="viewname"
        v-loading="listLoading"
        :data="pageData.data"
        :default-sort="getDefaultSort()"
        @sort-change="sortChange"
        @selection-change="val => multipleSelection = val"
        @cell-click="clickRow"
        class="list-table"
        border
        highlight-current-row
        stripe
        border
        fit
        height="calc(100vh - 260px)"
      >
        <el-table-column
          fixed
          type="selection"
          width="40"
        >
        </el-table-column>

        <template
          v-for="(field, name) in orderedSeializer()"
          v-if="canDisplayInList(field, name)"
        >
          <el-table-column
            :fixed='isColumnFixed("id")'
            v-if="name === 'id'"
            :key="`${viewname}_id_${name}`"
            :prop="name"
            :label="field.label"
            :class-name="field.type + ' id-column ' + (canRetrieve() ? 'retrieve' : '')"
            :min-width="80"
            show-overflow-tooltip
            :sortable="sectionData.meta.ordering_fields.indexOf(name) >= 0"
          >
            <template slot="header" slot-scope="scope">
              <el-tooltip class="item" effect="light" :content="`${field.label} ${$t('of_record')} '${sectionData.title}'`" placement="top">
                <div class='id-column-header-label'>
                  {{ field.label }}
                  <i class="el-icon-question"></i>
                </div>
              </el-tooltip>
            </template>
          </el-table-column>

          <el-table-column
            v-else
            :fixed='isColumnFixed(name)'
            :key="`${viewname}_${name}`"
            :min-width="170"
            :prop="name"
            :label="field.label"
            :class-name="field.type"
            show-overflow-tooltip
            :sortable="sectionData.meta.ordering_fields.indexOf(name) >= 0"
          >
            <template slot-scope="scope">
              <i class="el-icon-check boolean-true" v-if="scope.row[name] === true"></i>
              <i class="el-icon-close boolean-false" v-else-if="scope.row[name] === false"></i>
              <template v-else-if="field.type === 'datetime'">
                {{ formatDateTime(scope.row[name]) }}
              </template>
              <template v-else-if="field.type === 'decimal'">
                {{ parseFloat(scope.row[name]).toFixed(scope.row['precision'] || 2) }}
              </template>
              <template v-else-if="field.type === 'primarymany'">
                {{ formatMany(scope.row[name]) }}
              </template>
              <template v-else-if="field.type === 'multiple choice'">
                {{ formatMany(scope.row[name]) }}
              </template>
              <template v-else-if="field.type === 'file upload'">
                <a :href="scope.row[name]">{{ formatFileName(scope.row[name]) }}</a>
              </template>
              <template v-else-if="scope.row[name] && scope.row[name].text !== undefined">
                <template v-if="scope.row[name].text">{{ scope.row[name].text }}</template><template v-else>id: {{ scope.row[name].id }}</template>
              </template>
              <template v-else>{{ stripHtml(scope.row[name]) }}</template>
            </template>
          </el-table-column>

        </template>

        <el-table-column
          :label="$t('operations')"
          :min-width="200"
          v-if="hasInlineActions()"
          fixed="right"
        >
          <template slot-scope="scope">
            <template v-for="(action_info, key) in sectionData.meta.actions">
              <el-button
                v-if="action_info.inline_type"
                size="mini"
                :type="action_info.inline_type"
                @click="actionButtonInline(key, scope.row)">{{ action_info.name }}</el-button>
            </template>
          </template>
        </el-table-column>

      </el-table>

      <div class="below-list-section">
        <div class="actions-section" v-if="Object.keys(this.sectionData.meta.actions).length > 0">
          <el-button class="selection-button list-button" @click="toggleSelection()">{{ $t('remove_selection') }}</el-button>

          <el-tooltip class="item" effect="light" placement="top">
            <div slot="content">
              {{ $t('execute_for_all_tooltip') }}
              <br/>
              {{ $t('execute_for_all_tooltip_under') }}
            </div>
            <el-checkbox class="action-run-for-all" v-model="actionToAll">{{ $t('execute_for_all') }} <i class="el-icon-question"></i></el-checkbox>
          </el-tooltip>

          <el-select class="action-selector" v-model="selectedAction" :placeholder="$t('select_action')">
            <el-option
              v-for="(action_info, key) in this.sectionData.meta.actions"
              v-if="!action_info.inline_only"
              :key="`action_${key}`"
              :label="action_info.name"
              :value="key">
            </el-option>
          </el-select>
          <el-button class="selection-button list-button run-action" @click="actionButton" type="primary">{{ $t('execute') }}</el-button>
        </div>

        <div class="below-list-delimeter"/>

        <pagination
          class="pagination"
          v-show="pageData.count > 0"
          :total="pageData.count ? pageData.count : 0"
          :page.sync="pageInfo.page"
          :limit.sync="pageInfo.limit"
          @pagination="changePagination()"
        />
      </div>

      <el-dialog
        title="create-dialog"
        :visible.sync="dialogVisible"
        width="90%"
        top="2vh"
        custom-class="create-dialog"
        :destroy-on-close="true"
        :close-on-click-modal="false"
        :close-on-press-escape="false"
      >
        <modelform
          :form-info="formInfo"
          :api-info="apiInfo"
          @close="createClose"
          :settings="settings"
          v-if="dialogVisible"
        />
      </el-dialog>

      <el-dialog
        :visible.sync="actionDialog.visible"
        width="70%"
        top="10vh"
        :destroy-on-close="true"
        :close-on-click-modal="false"
        :close-on-press-escape="false"
        v-loading="actionDialog.loading"
      >
        <h2 class="form-title" v-if="actionDialog.actionInfo">{{ actionDialog.actionInfo.name }}</h2>
        <span class="form-desctiption" v-if="actionDialog.actionInfo && actionDialog.actionInfo.description">{{ actionDialog.actionInfo.description }}</span>

        <fieldscontainer
          v-if="actionDialog.visible"
          ref="fieldscontainer"
          :api-info="apiInfo"
          :meta="actionDialog.meta"
          :form-info="actionDialog.formInfo"
          @changed="value => updateActionForm(value)"
          :settings="settings"
        />

        <span slot="footer" class="dialog-footer">
          <el-button @click="actionDialog.visible = false">{{ $t('close') }}</el-button>
          <el-button type="primary" @click="sendActionForm()">{{ $t('execute') }}</el-button>
        </span>
      </el-dialog>

    </div>
  </div>
</template>

<script>
import moment from 'moment'

import { getList } from '@/api/getList'
import { sendAction } from '@/api/sendAction'
import { parseTime } from '@/utils'
import { Message } from 'element-ui'
import { getMethods } from '@/api/scheme'
import { appendBreadcrumb } from '@/utils/get-breadcrumb'

import ModelForm from '@/components/model-form'
import Pagination from '@/components/list-pagination'
import Filters from '@/components/filters'

export default {
  name: 'list',
  components: {
    Pagination,
    "filters": Filters,
    "modelform": ModelForm,
    "fieldscontainer": () => import('@/components/fields-container'),
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
      formInfo: null,
      dialogVisible: false,
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
      limit: this.getPaginationSize(),
    }

    this.apiMethods = getMethods(this.viewname, this.apiInfo)

    this.sectionData = this.apiInfo[this.viewname]
    if (!this.sectionData) {
      console.error(`Page ${this.viewname} not found in ${Object.keys(this.apiInfo)}`)
      this.$router.push({ path: '/404' })
      return
    }

    this.deserializeQuery()
    this.getListData()
  },
  methods: {
    hasInlineActions() {
      for (const [inline_key, inline_info] of Object.entries(this.sectionData.meta.actions)) {
        if (inline_info.inline_type) return true
      }
      return false
    },
    isColumnFixed(columnName) {
      return this.sectionData.meta.fixed_columns && this.sectionData.meta.fixed_columns.includes(columnName)
    },
    canAdd() {
      return 'create' in this.apiMethods
    },
    canRetrieve() {
      return 'retrieve' in this.apiMethods
    },
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
    openDetail(viewname, id) {
      const edit_url = `/${this.sectionData.group}/${viewname}/${id}/update`
      const breadcrumbs = appendBreadcrumb(this.$route, this.relationNameFilter)
      this.$router.push({ path: edit_url, query: breadcrumbs } )
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
        Message({ message: error, type: 'error', duration: 5 * 1000 })
      })
    },
    orderedSeializer() {
      if (this.sectionData.meta.filds_list) {
        let result = {}
        for (const filter_name of this.sectionData.meta.filds_list) {
          result[filter_name] = this.sectionData.meta.serializer[filter_name]
        }
        return result
      }
      return this.sectionData.meta.serializer
    },
    canDisplayInList(field, field_name) {
      if (!field) {
        console.error(`Field ${field_name} is not presented in serializer fields`)
        return
      }
      if (!field.write_only && (!this.sectionData.meta.filds_list || this.sectionData.meta.filds_list.indexOf(field_name) !== -1)) {
        return true
      }
      return false
    },
    handleFilter(newFilterInfo) {
      this.pageInfo.page = 1
      this.filterInfo = newFilterInfo
      this.serializeQuery()
      this.getListData()
    },
    changePagination() {
      localStorage.setItem('paginationSize', this.pageInfo.limit)
      this.serializeQuery()
      this.getListData()
    },
    getPaginationSize() {
      let paginationSize = localStorage.getItem('paginationSize')
      if (paginationSize) {
        return Number(paginationSize)
      }
      return 25
    },
    sortChange(data) {
      const desc = data.order === 'descending'? '-' : ''
      this.ordering = `${desc}${data.prop}`
      this.serializeQuery()
      this.getListData()
    },
    getDefaultSort() {
      if (this.ordering) {
        return {
          prop: this.ordering.startsWith('-') ? this.ordering.slice(1) : this.ordering,
          order: this.ordering.startsWith('-') ? 'descending' : null,
        }
      }
      return {prop: 'id', order: null}
    },
    clickRow(row, column, event) {
      if (column.label && column.label.toLowerCase() === 'id') {
        if (this.canRetrieve())
          this.openDetail(this.viewname, row.id)
      }
    },
    clicDoublekRow(row, column, event) {
      if (this.canRetrieve())
        this.openDetail(this.viewname, row.id)
    },
    handleCreate() {
      this.formInfo = {
        formType: 'create',
        recordId: null,
        viewname: this.viewname,
        showTitle: true,
        relationNameFilter: this.relationNameFilter,
        filterId: this.filterId,
      }
      this.dialogVisible = true
    },
    createClose(response) {
      if (response) this.getListData()

      this.dialogVisible = false
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    actionButton() {
      if (this.listLoading) return
      if (!this.selectedAction) {
        Message({ message: this.$t('no_action'), type: 'info', duration: 5 * 1000 })
        return
      }
      if (!this.actionToAll && this.$refs.table.selection.length === 0) {
        Message({ message: this.$t('no_record'), type: 'info', duration: 5 * 1000 })
        return
      }

      this.clickAction()
    },
    clickAction() {
      const actionInfo = this.sectionData.meta.actions[this.selectedAction]
      if (actionInfo.form_serializer) {
        this.actionDialog.formInfo = {
          formType: 'create',
        }
        this.actionDialog.actionInfo = actionInfo
        this.actionDialog.formData = {}
        this.actionDialog.meta = {
          serializer: actionInfo.form_serializer
        }
        this.actionDialog.visible = true
      }
      else {
        // Run simple admin action
        this.actionDialog.loading = true
        sendAction(
          this.viewname,
          this.selectedAction,
          this.$refs.table.selection.map(item => item.id),
          this.actionToAll,
          null
        ).then(response => {
          this.actionDialog.loading = false
          this.getListData()
        }).catch(error => {
          this.actionDialog.loading = false
        })
      }
    },
    actionButtonInline(selectedAction, row) {
      this.selectedAction = selectedAction
      this.$refs.table.clearSelection()
      this.$refs.table.toggleRowSelection(row)
      console.log(row, this.$refs.table.selection)
      this.clickAction()
    },
    sendActionForm() {
      this.$refs.fieldscontainer.$refs.form.validate().then(valid => {
        // Run admin action with form
        this.$refs.fieldscontainer.updateErrors({})

        sendAction(
          this.viewname,
          this.selectedAction,
          this.$refs.table.selection.map(item => item.id),
          this.actionToAll,
          this.actionDialog.formData
        ).then(response => {
          this.actionDialog.visible = false
          this.getListData()
        }).catch(error => {
          if (error) {
            this.$refs.fieldscontainer.updateErrors(error)
            Message({ message: this.$t('fix_errors'), type: 'error', duration: 3 * 1000 })
          }
        })

      }).catch(error => {
        Message({ message: this.$t('fix_errors'), type: 'error', duration: 1500 })
      })
    },
    toggleSelection(rows) {
      if (rows) {
        rows.forEach(row => {
          this.$refs.table.toggleRowSelection(row)
        })
      } else {
        this.$refs.table.clearSelection()
      }
    },
    formatDateTime(dateString) {
      if (dateString) {
        return moment(dateString).format('YYYY-MM-DD HH:mm')
      }
    },
    formatMany(data) {
      if (data === undefined || data === null) return '-'

      let result = []
      for (const d of data) {
        result.push(d.hasOwnProperty('text') ? d.text : d.display_name)
      }
      return result.join(', ')
    },
    formatFileName(data) {
      if (data) {
        return data.split("/").pop()
      }
    },
    updateActionForm(value) {
      this.$set(this.actionDialog, 'formData', value)
    },
    stripHtml(text)
    {
      if (text === null || text === undefined) return

      let tmp = document.createElement("DIV");
      tmp.innerHTML = text;
      return tmp.textContent || tmp.innerText || "";
    }
  }
}
</script>
