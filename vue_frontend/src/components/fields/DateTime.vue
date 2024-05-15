<template>

  <v-dialog max-width="500">
    <template v-slot:activator="{ props: activatorProps }">
      <v-text-field
        v-bind="activatorProps"
        :label="field.label"
        :model-value="displayValue"
        :messages="field.help_text || []"
        :disabled="field.read_only"
        append-inner-icon="mdi-calendar-range"
      />
    </template>

    <template v-slot:default="{ isActive }">
      <v-card>
        <v-card-text>
          {{ getFormattedValue() }}
          <Datepicker
            v-model="date"
            inline
            auto-apply
            @update:model-value="updateDateTime"
          />
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
import Datepicker from '@vuepic/vue-datepicker';

const requiredFields = [
]

export default {
  components: {
    Datepicker,
  },
  props: {
    ...defaultProps,
  },
  data(props) {
    return {
      value: null,
      date: null,
      displayValue: null,
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
    getFormattedValue() {
      return moment(this.value).format('YYYY-MM-DD HH:mm')
    },
    updateDateTime(value) {
      this.value()
    }
  },
}
</script>
