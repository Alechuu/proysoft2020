<template>
  <v-container>
    <v-card class="mt-5" color="primary" elevation="5">
      <div class="pa-5" style="text-align: center">
        <v-icon color="white" size="50"> mdi-home-calendar-search </v-icon>
        <h1 class="text-h4" style="text-align: center; color: white">
          Mis Turnos
        </h1>
      </div>
    </v-card>
    <v-card class="pa-8 mt-5 mb-5" elevation="5">
      <div style="text-align: center">
        <v-icon size="45" color="primary">mdi-clipboard-text</v-icon>
        <h3
          class="text-h6 pb-5"
          style="text-align: center; color: primary; font-family: Noto Sans SC"
        >
          Acá podés revisar todos tus turnos solicitados
        </h3>
        <h4 class="text-subtitle-1 pb-3" style="text-align: center">
          Ingresá una fecha y hacé click en <b>Ver Turnos</b>
        </h4>
      </div>
      <div class="d-flex flex-column">
        <v-divider></v-divider>
        <validation-observer ref="observer" v-slot="{ invalid }">
          <v-row>
            <v-col md="12" cols="12">
              <validation-provider
                v-slot="{ errors }"
                name="número de solicitud"
                rules="required|numeric"
              >
                <v-text-field
                  v-model="idSolicitud"
                  :error-messages="errors"
                  name="idSolicitud"
                  label="Número de Solicitud"
                  prepend-icon="mdi-numeric"
                  data-vv-validate-on="change"
                >
                </v-text-field>
              </validation-provider>
            </v-col>
            <v-col md="12" cols="12">
              <v-btn
                @click="buscarSolicitud"
                :loading="cargandoSolicitud"
                :disabled="invalid"
                color="primary"
                >Ver Solicitud</v-btn
              >
            </v-col>
          </v-row>
        </validation-observer>

        <v-alert
          border="bottom"
          class="mt-5"
          v-model="alert"
          :type="alert_type"
          dismissible
          transition="scale-transition"
        >
          {{ alert_body }}
        </v-alert>
        <v-expansion-panels
          :readonly="true"
          multiple
          class="mt-5"
          v-model="panelSolicitud"
        >
          <v-expansion-panel v-for="i in items" :key="i">
            <v-expansion-panel-header color="primary">
              <div style="color: white" class="text-body-1">Solicitud</div>
            </v-expansion-panel-header>
            <v-expansion-panel-content color="secondary">
              <div class="mt-5 text-h6">Datos del Centro</div>
              <v-divider></v-divider>
              <v-row>
                <ul>
                  <v-col md="12" cols="12">
                    <li>
                      <div class="text-body-1">
                        Nombre: <b>{{ nombre_centro }}</b>
                      </div>
                    </li>
                    <li>
                      <div class="text-body-1">
                        Municipio: <b>{{ municipio_centro }}</b>
                      </div>
                    </li>
                    <li>
                      <div class="text-body-1">
                        Dirección: <b>{{ dir_centro }}</b>
                      </div>
                    </li>
                    <li>
                      <div class="text-body-1">
                        E-Mail: <b>{{ email_centro }}</b>
                      </div>
                    </li>
                  </v-col>
                </ul>
              </v-row>
              <div class="mt-5 text-h6">Estado de la Solicitud</div>
              <v-divider></v-divider>
              <v-alert
                border="bottom"
                class="mt-5"
                dense
                :type="alert_solicitud_type"
                >{{ alert_solicitud_body }}</v-alert
              >
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        <span id="testing" type="hidden" ref="solicitud" />
      </div>
    </v-card>
  </v-container>
</template>