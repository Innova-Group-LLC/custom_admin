<template>
  <div>

    <Filters
      v-if="method.filterset_fields"
      :settings="settings"
      :filterset-fields="method.filterset_fields"
      :filter-info-init="filterInfo"
      @filtered="handleFilter"
    />

    <template v-if="inlineData && inlineData.messages">
      <v-alert
        v-for="error in inlineData.messages"
        :key="error.title"
        :title="error.title"
        :type="error.type"
        density="compact"
        variant="tonal"
      />
    </template>

    <v-data-table
      class="model-table"
      :items="inlineData.data || []"
      :loading="listLoading"

      :items-per-page="pageInfo.limit"
      :page="pageInfo.page"

      height="unset"
    >

      <template v-for="column in inlineData.columns" v-slot:[`item.${column}`]="{ item }">
        <div v-html="item[column]" v-if="isHTML(column)"></div>
        <div v-else>{{ item[column] }}</div>
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
              v-if="count > 0"
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
import { getSettings, setSettings } from '/src/utils/settings'
import { toast } from "vue3-toastify"
import { getList } from '/src/api/getList'

export default {
  props: {
    id: {type: String, required: true},
    method: {type: Object, required: true},
    settings: {type: Object, required: true},
  },
  emits: ["changed"],
  data(props) {
    return {
      perPageOptions: [25, 50, 100, 150],
      inlineData: {},
      listLoading: false,
      count: 0,
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
      this.listLoading = false
      this.inlineData = {}
      this.errors = null

      const url = this.method.url.replace("{id}", this.id)
      getList({
        url: url,
        method: this.method.methodHttp,
        pageInfo: this.pageInfo,
        filter_info: this.filterInfo,
      }).then(response => {
        this.inlineData = response
        this.count = this.inlineData.count

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
      if (!this.pageData) return 0
      return parseInt((this.pageData.count || 0) / this.pageInfo.limit)
    },
    changePagination() {
      let settings = getSettings()
      settings.page_size = this.pageInfo.limit,
      setSettings(settings)

      this.getInlineData()
    },
  },
}
</script>
