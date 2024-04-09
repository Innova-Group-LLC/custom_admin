<template>
  <div class="filter-container">
    <el-tooltip class="item" effect="light" placement="bottom" v-if="searchFields">
      <div slot="content">{{ $t('search_by') }} {{ searchFields.join(', ') }}</div>
      <el-input
        v-model="filterInfo.search"
        :placeholder="$t('search')"
        class="filter-search filter-element"
        style="width: 200px;"
        @keyup.enter.native="applyFilter"
      />
    </el-tooltip>

    <template v-for="(filter, filter_name) in filtersetFields" v-if="filtersetFields">

      <template v-if="filter.choices">
        <el-select
          v-model="filterInfo.filters[filter_name]"
          :placeholder="filter.name"
          class="filter-element"
        >
          <el-option clear :value="null">---</el-option>
          <el-option
            v-for="choice in filter.choices"
            :key="choice[0]"
            :label="choice[1]"
            :value="choice[0]"
          >
          </el-option>
        </el-select>
      </template>

      <template v-else-if="types.number.indexOf(filter.type) >= 0">
        <el-input-number
          v-model="filterInfo.filters[filter_name]"
          :placeholder="filter.name"
          class="filter-element input-number"
          :precision="1"
        />
      </template>

      <template v-else-if="types.input.indexOf(filter.type) >= 0">
        <el-input
          v-model="filterInfo.filters[filter_name]"
          :placeholder="filter.name"
          class="filter-element"
        />
      </template>

      <template v-else-if="types.tagsfield.indexOf(filter.type) >= 0">
        <tagsfield
          :init-filter-values="filterInfo.filters[filter_name]"
          :model-name="filter.model"
          :app-label="filter.app_label"
          @changed="value => changeTags(value, filter_name)"
          type="many"
          :max-tags="20"
          :placeholder="filter.name"
          :settings="settings"
          class="filter-tag filter-element"
        />
      </template>

      <template v-else-if="types.choices.indexOf(filter.type) >= 0">
        <el-select
          v-model="filterInfo.filters[filter_name]"
          :placeholder="filter.name"
          class="filter-element"
        >
          <el-option clear :value="null">---</el-option>
          <el-option :key="true" :label="filter.name + ': ' + $t('yes')" :value="'true'"/>
          <el-option :key="false" :label="filter.name + ': ' + $t('no')" :value="'false'"/>
          </el-option>
        </el-select>
      </template>

      <template v-else-if="types.time.indexOf(filter.type) >= 0">
        <el-time-picker
          v-model="filterInfo.filters[filter_name]"
          :placeholder="filter.name"
          value-format="hh:mm:ss"
          class="filter-element"
        />
      </template>

      <template v-else-if="types.date.indexOf(filter.type) >= 0">
        <el-date-picker
          v-model="filterInfo.filters[filter_name]"
          type="datetime"
          :placeholder="filter.name"
          value-format="yyyy-MM-ddTHH:mm:ss"
          class="filter-element"
        />
      </template>

      <template v-else-if="types.daterange.indexOf(filter.type) >= 0">
        <div class="filter-daterange filter-element">
          <date-picker
            v-model="temp[filter_name]"
            type="date"
            format="YYYY-MM-DD"
            :range="true"
            :clearable="true"
            :lang="localeDateData"
            :auto-apply="true"
            :placeholder="filter.name"
            range-separator=" - "
            @change="value => updateDateRange(value, filter_name)"
            @clear="value => updateDateRange(null, filter_name)"
          />
        </div>
      </template>

      <template v-else>
        {{ filter_name }}{{ filter }}
      </template>
    </template>

    <el-button
      v-waves
      class="filter-item filter-button"
      type="primary"
      icon="el-icon-search"
      @click="applyFilter"
    >
      {{ $t('apply') }}
    </el-button>
  </div>
</template>

<script>
import waves from '@/directive/waves'
import TagsField from '@/components/fields/tags-field'
import moment from 'moment';

import DatePicker from 'vue2-datepicker';

export default {
  name: 'filters',
  components: {
    "tagsfield": TagsField,
    DatePicker,
  },
  props: {
    settings: {type: Object, required: true},

    filterInfoInit: {type: [Object, Array], required: false},
    filtersetFields: {type: [Object, Array], required: false},
    searchFields: {type: Array, required: false},
  },
  directives: { waves },
  data() {
    return {
      types: {
        daterange: ['DateTimeField', 'DateFromToRangeFilter'],
        date: ['DateTimeFilter'],
        time: ['TimeField', 'TimeFilter'],
        number: ['NumberFilter'],
        choices: ['BooleanField'],
        tagsfield: [
          'ForeignKey',
          'ModelChoiceFilter',
          'ManyToManyField',
          'OneToOneField',
          'ManyToManyRel',
          'ModelMultipleChoiceFilter',
          'ManyRelatedField',
          'AdminManyRelatedField',
        ],
        input: ['GenericIPAddressField', 'TextField', 'UUIDField', 'CharFilter'],
      },
      sectionData: null,
      filterInfo: {
        search: null,
        filters: {},
      },
      temp: {},
      localeDateData: {
        firstDayOfWeek: 0,
        yearFormat: 'YYYY',
        monthFormat: 'MMM',
      },
    }
  },
  created() {
    if (this.filterInfoInit) {
      this.filterInfo = this.filterInfoInit
    }
    for (const [filter_name, filter] of Object.entries(this.filtersetFields)) {
      if (this.types.daterange.indexOf(filter.type) >= 0) {
        this.setDefaultDateRange(filter_name)
      }
    }
  },
  methods: {
    applyFilter() {
      this.$emit('filtered', this.filterInfo)
    },
    setDefaultDateRange(filter_name) {
      const afterStr = this.filterInfo.filters[`${filter_name}_after`]
      const beforeStr = this.filterInfo.filters[`${filter_name}_before`]
      if (afterStr && beforeStr) {
        const dates = [
          moment(afterStr).toDate(),
          moment(beforeStr).toDate()
        ]
        this.$set(this.temp, filter_name, dates)
      }
    },
    updateDateRange(value, filter_name) {
      if (!value) {
        delete this.filterInfo.filters[`${filter_name}_before`]
        delete this.filterInfo.filters[`${filter_name}_after`]
        return
      }
      const after = moment(value[0]).format('YYYY-MM-DD')
      const before = moment(value[1]).format('YYYY-MM-DD')
      this.filterInfo.filters[`${filter_name}_after`] = after
      this.filterInfo.filters[`${filter_name}_before`] = before
    },
    changeTags(value, filter_name) {
      let newTags = []
      if (value !== null && value !== undefined) {
        for (const tag of value) {
          newTags.push(tag.id)
        }
      }
      this.filterInfo.filters[filter_name] = newTags
      this.$emit('filtered', this.filterInfo)
    }
  }
}
</script>
