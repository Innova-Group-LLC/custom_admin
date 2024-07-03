<template>

  <v-select
    :density="density"
    :variant="variant"
    :clearable="true"
    :label="field.label"
    :model-value="value"
    :messages="field.help_text || []"
    :disabled="readOnly"
    :loading="loading"

    :items="choices"
    item-title="display_name"
    item-value="value"
    :return-object="false"

    @update:modelValue="onChange"
  />

</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'

export default {
  props: {
    ...defaultProps,
  },
  emits: ["changed"],
  data(props) {
    return {
      value: null,
      choices: [
        { value: true, display_name: this.$t('yes') },
        { value: false, display_name: this.$t('no') },
      ],
    }
  },
  created() {
    validateProps(this)
    this.value = this.field.initial
  },
  methods: {
    updateFormData(initFormData) {
      this.value = initFormData[this.fieldSlug]
    },
    onChange(newValue) {
      this.value = newValue
      this.$emit('changed', this.value)
    },
  },
}
</script>
