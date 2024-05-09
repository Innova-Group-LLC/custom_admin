<template>
  <div class="list-page">

    <v-data-table
      :items="pageData.data"
      :loading="listLoading"
    >
    </v-data-table>

  </div>
</template>

<script>
import { getMethods } from '/src/api/scheme'
import { getList } from '/src/api/getList'

export default {
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
      deserts: [
        {
          name: 'Frozen Yogurt',
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          iron: '1',
        },
        {
          name: 'Jelly bean',
          calories: 375,
          fat: 0.0,
          carbs: 94,
          protein: 0.0,
          iron: '0',
        },
      ],
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
      limit: 25,
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
  }
}
</script>
