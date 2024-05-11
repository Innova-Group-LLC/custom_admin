<template>
  model form
</template>

<script>

export default {
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},

    viewname: {type: String, required: false},
    relationNameFilter: {type: Object, required: false},
    filterId: {type: Object, required: false},
  },
  methods: {
  },
}
</script>
