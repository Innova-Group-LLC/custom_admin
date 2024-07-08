<template>
  <v-dialog
    max-width="1200"
    content-class="dialog-top-position"
    persistent
    v-model="open"
    class="create-dialog"
  >
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn
        v-bind="activatorProps"
        color="primary"
        @click="open = true"
        icon="mdi-plus"
        class="button-icon"
      ></v-btn>
    </template>

    <template v-slot:default="{ isActive }">
      <v-card v-if="open">

        <v-card-title class="d-flex justify-space-between align-center">
          <span>{{ getTitle() }}: {{ $t('creation') }}</span>

          <v-btn
            icon="mdi-close"
            variant="text"
            density="compact"
            @click="isActive.value = false"
          ></v-btn>
        </v-card-title>

        <!-- Form for create new model record -->
        <FieldsContainer
          ref="fieldscontainer"
          form-type="create"
          :api-info="apiInfo"
          :viewname="viewname"

          :relation-name-filter="relationNameFilter"
          :filter-id="filterId"
          :loading="loading"

          @changed="value => formData = value"
        />

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            :text="$t('close')"
            @click="open = false"
          />
          <v-btn
            :text="$t('create')"
            variant="elevated"
            color="primary"
            @click="createModel"
          />
      </v-card-actions>
    </v-card>
  </template>
</v-dialog>
</template>

<script>
// A component for displaying a button that causes a form to be opened to create a model.

import { getMethods } from '/src/api/scheme'
import { sendData } from '/src/api/sendData'
import { toast } from "vue3-toastify"

import FieldsContainer from '/src/components/FieldsContainer.vue'

export default {
  props: {
    apiInfo: {type: Object, required: true},

    viewname: {type: String, required: false},
    relationNameFilter: {type: String, required: false},
    filterId: {type: String, required: false},
  },
  emits: ["created"],
  data() {
    return {
      open: false,
      formData: {},
      loading: false,
    }
  },
  async created() {
    this.apiMethods = getMethods(this.viewname, this.apiInfo)
  },
  methods: {
    getTitle() {
      return this.apiInfo[this.viewname].title
    },
    createModel() {
      let method = this.apiMethods['create']
      if (!method) {
        console.error(`create method is not found in the list of available methods`)
        return
      }

      this.loading = true
      this.$refs.fieldscontainer.updateErrors({})
      sendData(
        method.url.replace("{id}", this.id),
        method.methodHttp,
        this.formData,
      ).then(response => {
        this.loading = false
        if (response) {
          let message = this.$t('modelCreated').replace('{id}', response.id)
          toast(message, {"theme": "auto", "type": "success", "position": "top-center"})
        }
        this.open = false
        this.$emit('created')
      }).catch(error => {
        this.loading = false
        if (error.response) {
          if (error.response.status === 400) {
            this.$refs.fieldscontainer.updateErrors(error.response.data)
            console.error('Validation errors', error.response.data)
            toast(this.$t('fixErrors'), {"theme": "auto", "type": "error", "position": "top-center" })
            return
          }
          toast(`Error: ${error.response.data}`, {"theme": "auto", "type": "error", "position": "top-center"})
          return
        }
        console.error(error)
        toast(error, {"theme": "auto", "type": "error", "position": "top-center"})
      })
    },
  },
}
</script>
