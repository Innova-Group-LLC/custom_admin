<template>
  <div>
    <el-form-item
      :label="field.label"
      :prop="fieldSlug"
      label-width="230px"
      :class="{'is-required': field.required}"
      v-loading="loadData"
    >
      <template v-if="Object.keys(freespinsInfo).length !== 0">
        <template v-for="(config_options, config_slug) in freespinsInfo">

          <div v-if="config_slug !== '_help_text'">
            {{ formatTitle(config_slug) }}:

            <template v-if="config_options === 'float' || (typeof config_options === 'number')">
              <el-input-number v-model="data[config_slug]"/>
            </template>

            <template v-else-if="Array.isArray(config_options)">
              <el-select v-model="data[config_slug]">
                <el-option
                  v-for="option in config_options"
                  :key="JSON.stringify(option)"
                  :label="JSON.stringify(option)"
                  :value="JSON.stringify(option)"
                />
              </el-select>
            </template>

            <template v-else>
              <el-input v-model="data[config_slug]" class="string"/>
            </template>

            <div v-if="data[config_slug]" class="choice-button" @click="value => data[config_slug] = null">
              <i class="el-icon-delete"/>
            </div>

            <div class="el-form-item-delimiter"/>
          </div>

        </template>

        <span class="freespin-setting-help-text" v-if="freespinsInfo._help_text">{{ freespinsInfo._help_text }}</span>

      </template>

      <template v-else-if="errorMessage">
        <span class="error-text">{{ errorMessage }}</span>
      </template>

      <template v-else>
        ---
      </template>
      <span class="help-text" v-if="field.help_text">{{ field.help_text }}</span>

      <div class="errors" v-if="error">
        <span class="error-text" v-for="(errorText, field_slug) in error">{{ errorText }}</span>
      </div>

    </el-form-item>
    <div class="el-form-item-delimiter"/>
  </div>
</template>

<style>
 .freespin-setting-help-text {
   color: #7e8286;
   font-size: 12px;
   display: block;
 }
</style>

<script>
import request from '@/utils/request'
import { Message } from 'element-ui'
import { config_dataset } from '@/utils/settings'

export default {
  name: 'freespinssettings',
  props: ['field', 'fieldSlug', 'error'],
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
          Message({ message: error, type: 'error', duration: 5 * 1000 })
        }
        this.loadData = false
      })
    }
  }
}
</script>
