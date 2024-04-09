<template>
  <div>
  </div>
</template>

<script>
export default {
  name: 'examplefield',
  props: [
    'field', 'fieldSlug',
  ],
  data(props) {
    return {
    }
  },
  created() {
  },
  methods: {
    updateFormData(initFormData) {
      const init = initFormData[this.fieldSlug]
    },
    changed(value) {
      this.$emit('changed', value)
    },
  },
}
</script>
