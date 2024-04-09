<template>
  <div>
    <el-form-item
      :label="field.label"
      :prop="fieldSlug"
      label-width="230px"
      :class="{'is-required': field.required}"
    >
      <!-- Код для изменения data -->

      <span class="help-text" v-if="field.help_text">{{ field.help_text }}</span>

      <div class="errors" v-if="error">
        <span class="error-text" v-for="(errorText, field_slug) in error">
          {{ errorText }}
        </span>
      </div>

    </el-form-item>
    <div class="el-form-item-delimiter"></div>
  </div>
</template>

<script>

// Для добавления поля, тебуется испортировать его в:
// src/components/custom-fields/index.js

export default {
  name: 'example',
  props: ['field', 'fieldSlug', 'error'],
  emits: ['changed'],
  data() {
    return {
      data: {},
    }
  },
  watch: {
    data: {
      immediate: true,
      deep: true,
      handler (newVal, oldVal) {
        // Отправление данных в форму при изменения data
        this.$emit('changed', newVal)
      }
    }
  },
  async created() {
  },
  methods: {
    updateFormData(formData) {
      // Сюда приходят данные формы, в т.ч.  при её обновлении остальными полями
    },
  }
}
</script>
