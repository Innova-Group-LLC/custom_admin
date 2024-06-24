<template>
  <v-app>
    <v-main>

      <v-container fluid class="fill-height gradient-bg">

        <v-row>
          <v-col class="d-flex justify-center">

            <v-card
              :loading="loading"
              width="400"
              class="login-header"
            >
              <template v-slot:title>
                <v-row justify="center" no-gutters>
                  <v-img
                    class="project-logo"
                    :alt="getTitle()"
                    :src="getLogo()"
                    v-if="getLogo()"
                    max-width="250"
                    :eager="true"
                  />
                  <span class="font-weight-black" v-else>{{ getTitle() }}</span>
                </v-row>
              </template>

              <v-card-text class="bg-surface-light pt-4">
                <form>
                  <v-text-field
                    density="default"
                    :hideDetails="false"

                    v-model="username"
                    :rules="[rules.required, rules.min]"
                    label="Username"
                    required
                    @keydown.enter.prevent="login"
                  ></v-text-field>
                  <v-text-field
                    density="default"
                    :hideDetails="false"

                    v-model="password"
                    :rules="[rules.required, rules.min]"
                    label="Password"
                    :type="show ? 'text' : 'password'"
                    :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                    required
                    @click:append="show = !show"
                    @keydown.enter.prevent="login"
                  ></v-text-field>

                  <v-row justify="end" no-gutters>
                    <v-btn @click="login">Login</v-btn>
                  </v-row>

                </form>

              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

      </v-container>

    </v-main>
  </v-app>
</template>

<script>
import { toast } from "vue3-toastify";
import { config_dataset } from '/src/utils/settings'

import { login } from '/src/api/user'

export default {
  data () {
    return {
      rules: {
        required: value => !!value || 'Required.',
      },
      username: '',
      password: '',
      show: false,
      loading: false,
    }
  },
  watch: {
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = `${this.$t('login')} | ${config_dataset.title}`
      }
    },
  },
  methods: {
    async validate () {
      const { valid } = await this.$refs.form.validate()

      if (valid) alert('Form is valid')
    },
    getLogo() {
      return config_dataset.logo_image
    },
    getTitle() {
      return config_dataset.title
    },
    login() {
      this.loading = true
      login(this.username, this.password).then(() => {
        this.$router.push('/')
        this.loading = false
      }).catch(error => {
        this.loading = false
        let error_message = error.message
        if (error.response) {
          const data = error.response.data

          if (data && data['non_field_errors']) {
            error_message = data['non_field_errors'][0]
          }
        }
        toast(error_message, {
          "limit": 3,
          "theme": "auto",
          "type": "error",
          "position": "top-center",
          "dangerouslyHTMLString": true
        })
      })
    },
  },
}
</script>
