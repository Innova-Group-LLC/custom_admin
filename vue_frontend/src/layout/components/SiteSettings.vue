<template>
  <div class="settings-icon">
    <i class="el-icon-s-tools" @click="dialogVisible = true"/>

    <el-dialog :visible.sync="dialogVisible" width="30%">
      <div class="header-form" v-if="dialogVisible">
        <h2 class="form-title">{{ $t('settings') }}</h2>
        <i class="el-icon-close icon-close" @click="dialogVisible = false"></i>
      </div>

      <el-form
        ref="form"
        class="data-form"
        :model="formData"
        label-width="120px"
        label-position="left"
        size="mini"
      >
        <el-form-item
          :label="$t('wysiwygSkin')"
          prop="field_slug"
          label-width="150px"
        >
          <el-select v-model="formData.wysiwygSkin">
            <el-option
              v-for="(title, slug) in getWysiwygTypes()"
              :key="slug"
              :label="title"
              :value="slug">
            </el-option>
          </el-select>

        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">{{ $t('close') }}</el-button>
        <el-button type="primary" @click="saveSettings">{{ $t('save') }}</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { wysiwygTypes, setSettings } from '/src/utils/settings'

export default {
  props: {
    settings: {type: Object, required: true},
  },
  data() {
    return {
      dialogVisible: false,
      formData: null,
    }
  },
  created() {
    this.formData = this.settings
  },
  methods: {
    getWysiwygTypes() {
      return wysiwygTypes
    },
    saveSettings() {
      setSettings(this.formData)
      document.location.reload()
    },
  }
}
</script>
