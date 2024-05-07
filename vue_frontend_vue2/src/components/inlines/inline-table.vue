<template>
  <div class="inline-container" v-loading="loadData">
    <filters
      @filtered="handleFilter"
      :filterset-fields="method.filterset_fields"
      v-if="method.filterset_fields"
      :filter-info-init="filterInfo"
      :settings="settings"
    />

    <template v-if="inlineData && inlineData.messages">
      <el-alert
        v-for="error in inlineData.messages"
        :title="error.title"
        :type="error.type"
        :key="error.title"
      />
    </template>

    <template v-if="inlineData && inlineData.data">
      <el-table
        :data="inlineData.data"
        stripe
        border
        fit
        highlight-current-row
        height="calc(100vh - 260px)"
      >
        <el-table-column
          v-for="column in inlineData.columns"
          :key="column"
          :prop="column"
          :label="column"
          :min-width="170"
          :width="getColumnInfo(column, 'width')"
          :fixed="getColumnInfo(column, 'fixed')"
        >
          <template #default="scope">

            <template v-if="getColumnInfo(column, 'html')">
              <span v-html="scope.row[scope.column.property]"/>
            </template>
            <template v-else>
              {{ scope.row[scope.column.property] }}
            </template>

          </template>
        </el-table-column>
      </el-table>

    </template>

    <div class="below-list-section">
      <div class="actions-section" v-if="Object.keys(method.actions).length > 0">
        <el-select class="action-selector" v-model="selectedAction" :placeholder="$t('select_action')">
          <el-option
            v-for="(action_info, key) in method.actions"
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
        v-show="count > 0"
        :total="count"
        :page.sync="pageInfo.page"
        :limit.sync="pageInfo.limit"
        @pagination="changePagination"
      />
    </div>

  </div>
</template>

<script>
import { Message } from 'element-ui'
import { getList } from '@/api/getList'
import Filters from '@/components/filters'
import Pagination from '@/components/list-pagination'
import { downloadContent } from '@/api/sendAction'

export default {
  name: 'InlineTable',
  props: {
    settings: {type: Object, required: true},

    id: {type: String, required: true},
    method: {type: Object, required: true},
  },
  components: {
    Pagination,
    Filters,
  },
  data() {
    return {
      inlineData: null,
      loadData: true,
      count: 0,
      filterInfo: {
        search: null,
        filters: {},
      },
      defaultPageInfo: {
        page: 1,
        limit: 25,
      },
      selectedAction: null,
    }
  },
  async created() {
    this.pageInfo = JSON.parse(JSON.stringify(this.defaultPageInfo))
    this.getInlineData()
  },
  methods: {
    getColumnInfo(column_name, info_name) {
      if (!this.inlineData) return
      const column_info = this.inlineData.columns_info[column_name]
      if (column_info) {
        return column_info[info_name]
      }
    },
    columnWidth(column_name) {
      if (!this.inlineData) return
      const column_info = this.inlineData.columns_info[column_name]
      if (column_info) {
        return column_info['width']
      }
    },
    changePagination() {
      this.getInlineData()
    },
    handleFilter(newFilterInfo) {
      this.filterInfo = newFilterInfo
      this.count = 0
      this.pageInfo = JSON.parse(JSON.stringify(this.defaultPageInfo))
      this.getInlineData()
    },
    getInlineData() {
      this.loadData = true
      this.inlineData = null
      this.errors = null

      const url = this.method.url.replace("{id}", this.id)
      getList({
        url: url,
        method: this.method.methodHttp,
        pageInfo: this.pageInfo,
        filters: this.filterInfo.filters,
        search: this.filterInfo.search,
      }).then(response => {
        this.inlineData = response
        this.count = this.inlineData.count

        this.loadData = false
      }).catch(error => {
        this.loadData = false
        console.error(`Get inline data error from ${url}:` + error, this.pageInfo)
        Message({ message: error, type: 'error', duration: 5 * 1000 })
      })
    },
    sendAction() {
      this.loadData = true
      this.inlineData = null
      const url = this.method.url.replace("{id}", this.id)
      getList({
        url: url,
        method: this.method.methodHttp,
        pageInfo: this.pageInfo,
        filters: this.filterInfo.filters,
        search: this.filterInfo.search,
        inline_action: this.selectedAction,
      }).then(response => {
        if(response.headers['content-type'] === 'text/csv') {
          const fileName = response.headers['pragma'] || `${moment().format('DD.MM.YYYY_HH:MM')}.csv`
          downloadContent(response.data, fileName, response.headers['content-type'])
        }
        else if (response.data.action_messages) {
          Message({ message: response.data.action_messages.join('<br>'), type: 'success', duration: 5 * 1000 , dangerouslyUseHTMLString: true,})
        }
        this.getInlineData()
      }).catch(error => {
        this.loadData = false
        console.error(`Get inline data error from ${url}:` + error, this.pageInfo)
        Message({ message: error, type: 'error', duration: 5 * 1000 })
      })
    },
    actionButton() {
      if (this.loadData) return
      if (!this.selectedAction) {
        Message({ message: this.$t('no_action'), type: 'info', duration: 5 * 1000 })
        return
      }
      this.sendAction()
    }
  }
}
</script>
