<template>

  <v-dialog max-width="500">
    <template v-slot:activator="{ props: activatorProps }">
      <v-text-field
        :label="field.label"
        :model-value="value"
        :messages="field.help_text || []"
        :disabled="field.read_only"
        append-inner-icon="mdi-calendar-range"
      />
    </template>

    <template v-slot:default="{ isActive }">
      <v-card title="Dialog">
        <v-card-text>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            text="Close Dialog"
            @click="isActive.value = false"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>

</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'

const requiredFields = [
]

export default {
  props: {
    ...defaultProps,
  },
  data(props) {
    return {
      value: null,
    }
  },
  created() {
    validateProps(this, requiredFields)
    this.value = this.field.initial
  },
  methods: {
    updateFormData(initFormData) {
      this.value = initFormData[this.fieldSlug]
    },
  },
}
</script>
