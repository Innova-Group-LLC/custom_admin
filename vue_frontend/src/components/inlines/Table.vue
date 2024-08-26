<template>
  <div class="list-page">

    <div class="inline-filters">
      <Filters
        v-if="method.filterset_fields"
        :settings="settings"
        :filterset-fields="method.filterset_fields"
        :filter-info-init="filterInfo"
        @filtered="handleFilter"
      />
    </div>

    <template v-if="inlineData && inlineData.messages">
      <div class="table-messages">
      <v-alert
        v-for="message in inlineData.messages"
        :key="message.title"
        :title="message.title"
        :type="message.type"
        density="compact"
        variant="tonal"
      />
      </div>
    </template>

    <v-data-table
      v-if="!listLoading"
      class="model-table"
      :items="inlineData.data || []"
      :loading="listLoading"

      :items-per-page="pageInfo.limit"
      :page="pageInfo.page"

      height="unset"
    >

      <template v-for="column in inlineData.columns" v-slot:[`item.${column}`]="{ item }">
        <div :class="{ 'table-cell': true }">
          <div class="cell-string" v-html="item[column]" v-if="isHTML(column)"></div>
          <div class="cell-string" v-else>{{ item[column] }}</div>
        </div>
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
              v-if="getLength() > 0"
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

    <template v-else-if="listLoading">
      <div class="chart-loader">
        <v-progress-circular
          :size="50"
          color="primary"
          indeterminate
        ></v-progress-circular>
      </div>
    </template>

  </div>
</template>

<script>
import { getSettings, setSettings } from '/src/utils/settings'
import { toast } from "vue3-toastify"
import { getList } from '/src/api/getList'

export default {
  props: {
    pk: {type: String, required: true},
    method: {type: Object, required: true},
    settings: {type: Object, required: true},
  },
  emits: ["changed"],
  data(props) {
    return {
      perPageOptions: [25, 50, 100, 150],
      inlineData: {},
      listLoading: false,
      numPages: 0,
      filterInfo: {
        search: null,
        filters: {},
      },
      pageInfo: {
        page: 1,
        limit: 25,
      },
      selectedAction: null,
    }
  },
  async created() {
    this.pageInfo = {
      page: 1,
      limit: getSettings().page_size || 25,
    }
    this.getInlineData()
  },
  methods: {
    isHTML(column) {
      const info = this.inlineData.columns_info[column] || {}
      return info.html
    },
    getInlineData() {
      this.listLoading = true
      this.inlineData = {}
      this.errors = null

      const url = this.method.url.replace("{pk}", this.pk)
      getList({
        url: url,
        method: this.method.methodHttp,
        pageInfo: this.pageInfo,
        filter_info: this.filterInfo,
      }).then(response => {
        this.inlineData = response
        this.numPages = this.inlineData.num_pages

        this.listLoading = false
      }).catch(error => {
        this.listLoading = false
        console.error(`Get inline data error from ${url}:` + error, this.pageInfo)
        toast(error, {
          "theme": "auto",
          "type": "error",
          "position": "top-center",
          "dangerouslyHTMLString": true
        })
      })
    },
    getLength() {
      return this.numPages || 0
    },
    changePagination() {
      let settings = getSettings()
      settings.page_size = this.pageInfo.limit,
      setSettings(settings)

      this.getInlineData()
    },
    handleFilter(newFilterInfo) {
      this.filterInfo = newFilterInfo
      this.getInlineData()
    },
  },
}
</script>
