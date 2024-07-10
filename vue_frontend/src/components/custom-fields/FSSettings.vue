<template>
  <div>
    <v-card
      class="fs-card"
      :loading="loadData"
    >
      <template v-if="Object.keys(freespinsInfo).length !== 0">
        <template v-for="(config_options, config_slug) in freespinsInfo">

          <div v-if="config_slug !== '_help_text'">
            <v-label>{{ formatTitle(config_slug) }}:</v-label>

            <template v-if="config_options === 'float' || (typeof config_options === 'number')">
              <v-number-input
                :model-value="data[config_slug]"
                :clearable="true"
                @update:modelValue="value => onChange(config_slug, value)"
              />
            </template>

            <template v-else-if="Array.isArray(config_options)">
              <v-select
                :model-value="data[config_slug]"
                :items="config_options"
                item-title="bet_id"
                item-value="amount"
                :return-object="true"
                :clearable="true"
                @update:modelValue="value => onChange(config_slug, value)"
              >
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props">{{ item.raw }}</v-list-item>
                </template>
                <template v-slot:selection="{item}">
                  {{ item.raw }}
                </template>
              </v-select>
            </template>

            <template v-else>
              <v-text-field
                :model-value="data[config_slug]"
                :clearable="true"
                @update:modelValue="value => onChange(config_slug, value)"
              />
            </template>

            <div v-if="data[config_slug]" class="choice-button" @click="value => data[config_slug] = null">
              <i class="el-icon-delete"/>
            </div>
          </div>

        </template>

        <div class="fs-help-text" v-if="freespinsInfo._help_text">
          {{ freespinsInfo._help_text }}
        </div>

      </template>

      <template v-else-if="errorMessage">
        <div class="form-error">{{ errorMessage }}</div>
      </template>

      <template v-else>
        <div>---</div>
      </template>

      <v-label class="fs-help" v-if="field.help_text">{{ field.help_text }}</v-label>
    </v-card>

    <v-expansion-panels class="jsonforms-source-json">
      <v-expansion-panel>
        <v-expansion-panel-title><v-icon icon="mdi-cog-outline" size="x-small"/> <p>Source JSON</p></v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-label>{{ data }}</v-label>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<style>
 .fs-card {
     padding: 15px 5px;
 }
 .fs-help {
     margin-top: 10px;
 }
 .fs-help-text {
   color: #7e8286;
   font-size: 12px;
   display: block;
 }
</style>

<script>
import { VNumberInput } from 'vuetify/labs/VNumberInput'
import { defaultProps, validateProps } from '/src/utils/fields.js'
import request from '/src/utils/request'
import { config_dataset } from '/src/utils/settings'
import { toast } from "vue3-toastify"

export default {
  props: {
    ...defaultProps,
  },
  components: {
    VNumberInput,
  },
  emits: ['changed'],
  data() {
    return {
      hallGameInfo: null,
      bonusCurrency: null,
      freespinsInfo: {},
      loadData: false,
      errorMessage: null,
      data: {},
    }
  },
  created() {
    validateProps(this, [])
  },
  methods: {
    updateFormData(value) {
      // console.log('update', JSON.stringify(value))
      const hallGameInfo = value['hall_game_info']
      const bonusCurrency = value['bonus_currency']
      const freespin_config = value['freespin_config']
      const initValue = typeof freespin_config == 'string' ? JSON.parse(freespin_config) : freespin_config
      this.updateTrigger(hallGameInfo, bonusCurrency, initValue)
    },
    change(value) {
      // console.log('change', JSON.stringify(value))
      this.$emit('changed', this.data)
    },
    updateTrigger(hallGameInfo, bonusCurrency, initValue) {
      if (!hallGameInfo || !bonusCurrency) {
        this.freespinsInfo = {}
        this.data = initValue || {}
        this.change(initValue)
      }
      else if (hallGameInfo !== this.hallGameInfo || bonusCurrency != this.bonusCurrency) {
        this.getJackpotsInfo(hallGameInfo, bonusCurrency, initValue)
      }
      this.hallGameInfo = hallGameInfo
      this.bonusCurrency = bonusCurrency
    },
    formatTitle(value) {
      if (typeof value !== 'string') return value

      return (value.charAt(0).toUpperCase() + value.slice(1)).replace("_", " ")
    },
    getJackpotsInfo(hallGameInfo, bonusCurrency, initValue) {
      this.errorMessage = null
      const baseUrl = config_dataset.backend_prefix.replace("custom_admin/", "")
      const hallId = typeof hallGameInfo === "object" ? hallGameInfo.id : hallGameInfo

      const url = `${baseUrl}api/v1/nodes/freespins/${hallId}/bets/?bonus_currency=${bonusCurrency.id || bonusCurrency}`

      this.freespinsInfo = {}
      this.data = initValue || {}
      this.change(initValue)
      this.loadData = true
      request({
        url: url,
        method: 'get',
        headers: {
          'Accept': 'application/json',
        }
      }).then(response => {
        this.freespinsInfo = response.data
        this.loadData = false
      }).catch(error => {
        if (error.response && error.response.data && error.response.data.errors) {
          const errorObj = error.response.data.errors[0]
          if (errorObj.message) {
            this.errorMessage = errorObj.message
          } else {
            this.errorMessage = errorObj
          }
        }
        else {
          toast(error, {
            "limit": 3,
            "theme": "auto",
            "type": "error",
            "position": "top-center",
            "dangerouslyHTMLString": true
          })
        }
        this.loadData = false
      })
    },
    onChange(config_slug, value) {
      this.data[config_slug] = value
    },
  }
}
</script>
