<template>
  <v-dialog
    max-width="1200"
    content-class="dialog-top-position"
    persistent
  >
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn
        v-bind="activatorProps"
        class="create-button"
        size="small"
      >{{ $t('create') }}</v-btn>
    </template>

    <template v-slot:default="{ isActive }">
      <v-card v-if="isActive.value">

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
          formType="create"
          :api-info="apiInfo"
          :viewname="viewname"

          :relation-name-filter="relationNameFilter"
          :filter-id="filterId"
        />

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            :text="$t('close')"
            @click="isActive.value = false"
          ></v-btn>
      </v-card-actions>
    </v-card>
  </template>
</v-dialog>
</template>

<script>
// A component for displaying a button that causes a form to be opened to create a model.

import FieldsContainer from '/src/components/FieldsContainer.vue'

export default {
  props: {
    apiInfo: {type: Object, required: true},

    viewname: {type: String, required: false},
    relationNameFilter: {type: Object, required: false},
    filterId: {type: Object, required: false},
  },
  methods: {
    getTitle() {
      return this.apiInfo[this.viewname].title
    },
  },
}
</script>
