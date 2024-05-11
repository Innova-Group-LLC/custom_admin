<template>
  <v-container fluid>
    <v-row>
      <v-col cols="4">
        <v-list-subheader>Prefix for dollar currency</v-list-subheader>
      </v-col>

      <v-col cols="8">
        <v-text-field
          label="Amount"
          model-value="10.00"
          prefix="$"
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="4">
        <v-list-subheader>Suffix for weight</v-list-subheader>
      </v-col>

      <v-col cols="8">
        <v-text-field
          label="Weight"
          model-value="28.00"
          suffix="lbs"
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="4">
        <v-list-subheader>Suffix for email domain</v-list-subheader>
      </v-col>

      <v-col cols="8">
        <v-text-field
          label="Email address"
          model-value="example"
          suffix="@gmail.com"
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="4">
        <v-list-subheader>Suffix for time zone</v-list-subheader>
      </v-col>

      <v-col cols="8">
        <v-text-field
          label="Label Text"
          model-value="12:30:00"
          suffix="PST"
          type="time"
        ></v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
  props: {
    apiInfo: {type: Object, required: true},
    formType: {
      type: String,
      required: true,
      validator: function (value) {
          return ['create', 'edit'].indexOf(value) !== -1
      }
    },

    // Required if no meta was provided
    viewname: {type: String, required: false},

    // Chema of this form, if not provided - it will be used from apiInfo
    meta: {
      type: Object,
      required: false,
      validator: function (value) {
        if (value.serializer == null) {
          console.error('fields-container meta must contain serializer')
          return false
        }
        return true
      },
      default(rawProps) {
        return rawProps.apiInfo[rawProps.viewname].meta
      }
    },

    relationNameFilter: {type: Object, required: false},
    filterId: {type: Object, required: false},
  },
  data() {
    return {
      formData: {},
      translationsTabs: {},
    }
  },
  watch: {
    formData: {
      handler: function(newValue) {
        if (newValue) {
          this.$emit('changed', newValue)
        }
      },
      deep: true
    }
  },
  methods: {
    getGroups() {
      if (this.meta.field_groups) return this.meta.field_groups
      return [{"title": ""}]
    },
    getTranslations() {
      return this.meta.translations || {}
    },
    isTranslation(field_slug) {
      for (const [slug, translations] of Object.entries(this.getTranslations())) {
        for (var i = 0; i < translations.length; i++) {
          if (translations[i].slug === field_slug) return true
        }
      }
      return false
    },
  },
}
</script>
