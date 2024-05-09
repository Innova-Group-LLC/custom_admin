<template>
  <div class="list-page">

    <v-data-table-server
      v-model:items-per-page="itemsPerPage"
      :headers="headers"
      :items="serverItems"
      :items-length="totalItems"
      :loading="loading"
      :search="search"
      item-value="name"
      @update:options="loadItems"
    ></v-data-table-server>

  </div>
</template>

<script>

export default {
  props: {
    apiInfo: {type: Object, required: true},
  },
  data() {
    return {
      listLoading: false,
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
