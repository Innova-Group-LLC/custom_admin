<template>
  <v-dialog max-width="500">
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn
        v-bind="activatorProps"
        class="create-button"
        size="small"
      >{{ $t('create') }}</v-btn>
  </template>

  <template v-slot:default="{ isActive }">
    <v-card title="Dialog">
      <v-card-text>

        <!-- Model form for create new record -->
        <ModelForm
          :api-info="apiInfo"
          :settings="settings"

          :viewname="viewname"
          :relation-name-filter="relationNameFilter"
          :filter-id="filterId"

          v-if="isActive.value"
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

export default {
  props: {
    apiInfo: {type: Object, required: true},
    settings: {type: Object, required: true},

    viewname: {type: String, required: false},
    relationNameFilter: {type: Object, required: false},
    filterId: {type: Object, required: false},
  },
  methods: {
  },
}
</script>
