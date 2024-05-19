<template>

  FILTERS

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
