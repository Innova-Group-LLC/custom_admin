<template>
  <div class="tag-block">
    <div
      v-if="add && canBeAdded() && !disabled"
      class="add-model-icon"
      @click="addModelTag"
    >
      <i class="el-icon-circle-plus-outline"/>
    </div>
    <div class="tags-container" ref="tagsContainer">
      <vue-tags-input
        v-model="inputValue"
        :tags="tags"
        :autocomplete-items="autocompleteItems"
        :allow-edit-tags="false"
        :autocomplete-min-length="0"
        :max-tags="maxTags"
        :placeholder="placeholder"
        :add-only-from-autocomplete="true"
        :disabled="disabled"
        @tags-changed="tagsChanged"
        v-loading="loading"
        :class="{ disabled: disabled }"
        v-view="viewHandlerTag"
      />
    </div>

    <el-dialog
      title="sub-create-dialog"
      :visible.sync="subCreateDialogVisible"
      width="90%"
      top="2vh"
      custom-class="sub-create-dialog"
      :destroy-on-close="true"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <modelform
        :form-info="formInfo"
        :api-info="apiInfo"
        :settings="settings"
        @close="createClose"
      />
    </el-dialog>

  </div>
</template>

<script>
import { VueTagsInput } from '@vojtechlanka/vue-tags-input';
import { getAutocomplete } from '@/api/getAutocomplete'
import { Message } from 'element-ui'
import { getMethods } from '@/api/scheme'

export default {
  name: 'tagsinput',
  props: [
    // View info
    'modelName', 'appLabel', 'viewname', 'fieldSlug', 'initFormData', 'settings',

    // For related fields
    'instanceId', 'relationNameFilter', 'filterId',

    'type',
    'maxTags',
    'disabled',
    'placeholder',
    'apiInfo',
    'add',

    // For filter
    'initFilterValues',
  ],
  components: {
    VueTagsInput,
    "modelform": () => import('@/components/model-form')
  },
  data() {
    return {
      inputValue: '',
      tags: [],
      autocompleteItems: [],
      loading: false,
      formInfo: null,
      subCreateDialogVisible: false,
    }
  },
  watch: {
    inputValue: function(newValue) {
      this.getChoicesUpdate(newValue);
    },
  },
  async created() {

    if (this.relationNameFilter && this.relationNameFilter == this.fieldSlug) {
      // Read only
      this.tags = [{id: this.filterId, text: `${this.relationNameFilter} #${this.filterId}`, classes: 'disabled'}]
      this.emit(this.tags)
    }

    if (this.initFilterValues !== null && this.initFilterValues !== undefined) {
      // Set init filters values
      let init = this.initFilterValues
      if (!Array.isArray(init))
        init = [init]
      for (const initId of init) {
        this.tags.push({id: Number(initId), text: `#${initId} ${this.modelName}`})
      }
    }

    if (!this.disabled)
      this.search(null)

    if (this.initFormData != null) {
        this.updateFormData(this.initFormData)
    }
  },
  methods: {
    updateExistedChoices() {
      // When filter inits, this.initFilterValues contains ids,
      // but we need readable values

      loopTags:
      for (let index = 0; index < this.tags.length; ++index) {
        const tag = this.tags[index]

        for (const autocompleteItem of this.autocompleteItems) {
          if (tag.id === autocompleteItem.id) {
            this.tags[index].text = autocompleteItem.text
            this.$set(this.tags[index], 'classes', '')
            continue loopTags
          }
        }
        this.$set(this.tags[index], 'classes', 'tag-not-found')
      }
    },
    updateFormData(initFormData) {

      this.formData = initFormData

      const init = initFormData[this.fieldSlug]
      if (init !== null && init !== undefined) {
        this.tags = init
        // Make to list
        if (!Array.isArray(init))
          this.tags = [init]
      }

      if (!this.disabled) {
        this.search(null)
      }
    },
    tagsChanged(newTags) {
      this.tags = newTags
      this.emit(this.tags)
    },
    addModelTag() {
      this.formInfo = {
        formType: 'create',
        recordId: null,
        viewname: this.modelName.toLowerCase(),
        showTitle: true,

        relationNameFilter: this.relationNameFilter,
        filterId: this.filterId,
      }
      this.subCreateDialogVisible = true
    },
    createClose(response) {
      if (response) {
        const name = this.modelName.toLowerCase()
        this.tags.push({id: response.id, text: `${name} ${response.id}`})
        this.tagsChanged(this.tags)
      }
      this.subCreateDialogVisible = false
    },
    canBeAdded() {
      if (!this.modelName || !this.appLabel) return false
      if ((this.modelName.toLowerCase() in this.apiInfo)) {
        const methods = getMethods(this.modelName.toLowerCase(), this.apiInfo)
        if ('create' in methods) {

          if (this.tags.length >= this.maxTags) return false
          return true
        }
      }
      return false
    },
    async getChoicesUpdate(searchString) {
      if (this.disabled) return

      if (this.maxTags && this.tags.length >= this.maxTags) return
      this.autocompleteItems = []
      this.loading = true

      this.search(searchString)
    },
    search(searchString) {
      if (!this.modelName || !this.appLabel) {
        console.error(`modelName:${this.modelName} or appLabel:${this.appLabel} is not set (viewname:${this.viewname} fieldSlug:${this.fieldSlug})`)
        return
      }

      getAutocomplete(
        this.modelName,
        this.appLabel,
        searchString,
        30,
        this.viewname,
        this.fieldSlug,
        this.formData,
        this.tags,
      ).then(response => {

        this.autocompleteItems = response
        this.updateExistedChoices()
        this.loading = false
      }).catch(error => {

        this.loading = false
        let error_message = `Get model autocomplete for model ${this.modelName}.${this.viewname} searchString:"${searchString}" error:"${error}"`
        console.error(error_message)
        Message({ message: error_message, type: 'error', duration: 5 * 1000 })
      })
    },
    viewHandlerTag(e) {
      let classList = this.$refs.tagsContainer.classList
      e.percentTop > 0.5 ? classList.add('below-center') : classList.remove('below-center')
    },
    emit(tags) {
      if (tags.length === 0) {
        this.$emit('changed', null)
      }
      else {
        if (this.type === 'primary') {
          this.$emit('changed', tags[0])
        }
        else {
          this.$emit('changed', tags)
        }
      }
    },
  }
}
</script>
