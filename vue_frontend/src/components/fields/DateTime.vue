<template>

  <v-dialog width="auto">
    <template v-slot:activator="{ props: activatorProps }">
      <v-text-field
        v-bind="activatorProps"
        :label="field.label"
        :model-value="displayValue"
        :messages="field.help_text || []"
        :disabled="field.read_only"
      >
        <template v-slot:append-inner>
          <v-icon :icon="icon" v-for="icon in getIcons()"/>
        </template>
      </v-text-field>
    </template>

    <template v-slot:default="{ isActive }">
      <v-card>
        <v-text-field
          :model-value="displayValue"
          @update:modelValue="updateDisplayValue"
        />
        <Datepicker
          v-model="value"
          inline
          auto-apply
          time-picker-inline

          :enable-time-picker="['datetime', 'time'].indexOf(field.type) !== -1"
          :time-picker="field.type === 'time'"

          @update:model-value="updateDateTime"
        />
      </v-card>
    </template>
  </v-dialog>

</template>

<script>
import { defaultProps, validateProps } from '/src/utils/fields.js'
import moment from 'moment'
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
      displayValue: '',
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
      if (!this.value) return ''
      return moment(this.value).format(this.getFormat())
    },
    getFormat() {
      if (this.field.type === 'datetime') return 'YYYY-MM-DD HH:mm'
      if (this.field.type === 'date') return 'YYYY-MM-DD'
      if (this.field.type === 'time') return 'HH:mm'
      console.error('DateTime bad type:', field.type)
    },
    getIcons() {
      if (this.field.type === 'datetime') return ['mdi-calendar-range', 'mdi-clock-time-eight-outline']
      if (this.field.type === 'date') return ['mdi-calendar-range']
      if (this.field.type === 'time') return ['mdi-clock-time-eight-outline']
      console.error('DateTime bad type:', field.type)
    },
    updateDateTime(value) {
      this.value = value
      this.displayValue = this.getFormattedValue()
    },
    updateDisplayValue(value) {
      this.value = new Date(moment(value))
    },
  },
}
</script>
