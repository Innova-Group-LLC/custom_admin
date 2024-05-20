<template>

  <template v-for="(filter, filter_name) in filtersetFields" v-if="filtersetFields">
    {{ filter.type }}|
  </template>

</template>

<script>

export default {
  props: {
    settings: {type: Object, required: true},
    filtersetFields: {type: Object, required: true},
    filterInfoInit: {type: Object, required: false},
  },
  emits: ["filtered"],
  methods: {
  },
}
</script>
