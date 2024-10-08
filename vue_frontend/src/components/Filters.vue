<template>

  <div class="filters-container">

    <div class="filter-element" v-if="searchFields">
      <v-text-field
        density="compact"
        variant="solo"
        prepend-inner-icon="mdi-magnify"

        v-model="filterInfo.search"
        :clearable="true"
        :label="$t('search')"
        @keydown.enter.prevent="applyFilter"
      />
    </div>

    <div
      v-for="(filter, filter_name) in filtersetFields" v-if="filtersetFields"
      class="filter-element"
    >
      <component
        v-if="getFieldComponent(filter)"
        :is="getFieldComponent(filter)"

        density="compact"
        variant="solo"
        :viewname="viewname"
        :field="filter"
        :field-slug="filter_name"
        :loading="false"
        :is-filter="true"

        @changed="value => _updateValue(value, filter_name)"
        @keydown.enter.prevent="applyFilter"
      />
      <template v-else>
        {{ filter }}
      </template>
    </div>

    <!--
    <div class="filter-button">
      <v-btn
        variant="outlined"
        density="compact"
        class="button-icon"
        @click="applyFilter"
        color="secondary"
        icon="mdi-cog-outline"
      />
    </div>
    -->

    <div class="filter-button">
      <v-btn
        @click="applyFilter"
        color="secondary"
        prepend-icon="mdi-magnify"
        :disabled="loading"
      >{{ $t('apply') }}</v-btn>
    </div>
  </div>

</template>

<script>
import BooleanFilter from '/src/components/fields/BooleanFilter.vue'
import StringField from '/src/components/fields/String.vue'
import NumberField from '/src/components/fields/Number.vue'
import ChoiceField from '/src/components/fields/Choice.vue'
import RelatedField from '/src/components/fields/Related.vue'
import DateTimeField from '/src/components/fields/DateTime.vue'

export default {
  props: {
    settings: {type: Object, required: true},
    searchFields: {type: Object, required: false},
    filtersetFields: {type: Object, required: true},
    filterInfoInit: {type: Object, required: false},
    viewname: {type: String, required: false},
    loading: {type: Boolean, required: false},
  },
  emits: ["filtered"],
  data() {
    return {
      filterInfo: {},
    }
  },
  created() {
    if (this.filterInfoInit) {
      this.filterInfo = this.filterInfoInit
    }
  },
  methods: {
    getFieldComponent(filter) {
      const related = [
        'ForeignKey',
        'ModelChoiceFilter',
        'ManyToManyField',
        'OneToOneField',
        'ManyToManyRel',
        'ModelMultipleChoiceFilter',
        'ManyRelatedField',
        'AdminManyRelatedField',
        'AdminPrimaryKeyRelatedField',
      ]
      const datetime = [
        'DateTimeField',
        'DateFromToRangeFilter',
        'AdminDateFromToRangeFilter',
        'DateTimeFilter',
        'TimeField',
        'TimeFilter',
      ]

      if (['ChoiceFilter'].indexOf(filter.type) !== -1 || filter.choices) return ChoiceField

      const str = [
        'GenericIPAddressField',
        'TextField',
        'UUIDField',
        'CharFilter',
        'CharField',
      ]
      if (datetime.indexOf(filter.type) !== -1) return DateTimeField
      if (related.indexOf(filter.type) !== -1) return RelatedField
      if (str.indexOf(filter.type) !== -1) return StringField

      if (['NumberFilter'].indexOf(filter.type) !== -1) return NumberField
      if (['BooleanField', 'BooleanFilter'].indexOf(filter.type) !== -1) return BooleanFilter
    },
    _updateValue(value, filter_name) {
      this.filterInfo.filters[filter_name] = value
    },
    applyFilter() {
      if (this.loading) return
      this.$emit('filtered', this.filterInfo)
    },
  },
}
</script>
