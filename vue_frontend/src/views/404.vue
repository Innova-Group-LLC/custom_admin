<template>

  <v-app>
    <v-main>
      <v-container fluid class="fill-height gradient-bg">

        <v-row>
          <v-col class="d-flex justify-center">

            <div class="page-404">
              <router-link to="/dashboard" v-if="getLogo()">
                <v-img
                  class="project-logo"
                  :src="getLogo()"
                  max-width="400"
                  :eager="true"
                />
              </router-link>

              <p class="text-h4 text-center">{{ $t('notFoundPageHeadline') }}</p>
              <p class="text-center text-subtitle-2">{{ $t('notFoundPageTitle') }}</p>
              <router-link to="/dashboard"><p class="dashboard-link text-center">{{ $t('notFoundPageGoBack') }}</p></router-link>
            </div>

          </v-col>
        </v-row>

      </v-container>

    </v-main>
  </v-app>

</template>

<script>
import { config_dataset } from '/src/utils/settings'

export default {
  props: {
    apiInfo: {type: Object, required: true},
  },
  methods: {
    getLogo() {
      return config_dataset.logo_image
    },
  }
}
</script>
