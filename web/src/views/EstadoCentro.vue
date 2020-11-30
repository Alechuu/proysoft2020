<template>
  <v-container>
    <v-card class="mt-5" color="primary" elevation="5">
      <div class="pa-5" style="text-align: center">
        <v-icon color="white" size="50"> mdi-home-edit </v-icon>
        <h1 class="text-h4" style="text-align: center; color: white">
          Estado de la Solicitud de un Centro
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
          Acá podés revisar el estado de la solicitud de un nuevo Centro
        </h3>
        <h4 class="text-subtitle-1 pb-3" style="text-align: center">
          Ingresá el número de solicitud y hacé click en <b>Ver Solicitud</b>
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

<script>
import { required, numeric } from "vee-validate/dist/rules";
import {
  extend,
  ValidationObserver,
  ValidationProvider,
  setInteractionMode,
} from "vee-validate";

setInteractionMode("aggressive");

extend("required", {
  ...required,
  message: "El campo {_field_} no puede estar vacío",
});

extend("numeric", {
  ...numeric,
  message: "El campo {_field_} solo puede contener números",
});

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  data() {
    return {
      panelSolicitud: [],
      cargandoSolicitud: false,
      idSolicitud: "",
      items: 1,
      alert_type: "error",
      alert: false,
      alert_body: "",
      alert_solicitud_type: "success",
      alert_solicitud_body: "",
      nombre_centro: "",
      municipio_centro: "",
      dir_centro: "",
      email_centro: "",
    };
  },

  mounted() {
    console.log(this.$route.query.id);
    if (this.$route.query.id !== undefined) {
      this.idSolicitud = this.$route.query.id;
      this.buscarSolicitud();
      this.alert_type = "warning";
      this.alert_body =
        "Tu número de solicitud es: " +
        this.$route.query.id +
        ". Anotalo para poder volver a consultar la solicitud en un futuro.";
      this.alert = true;
    }
  },

  methods: {
    buscarSolicitud() {
      this.cargandoSolicitud = true;
      this.panelSolicitud = [];
      this.alert = false;
      fetch("http://127.0.0.1:5000/api/centros/id=" + this.idSolicitud, {
        method: "GET",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.status === 200) {
            this.nombre_centro = data.atributos.nombre;
            this.municipio_centro = data.atributos.municipio;
            this.dir_centro = data.atributos.direccion;
            this.email_centro = data.atributos.email;
            if (data.atributos.solicitud === "ACEPTADO") {
              this.alert_solicitud_type = "success";
              this.alert_solicitud_body = "APROBADO";
            } else {
              if (data.atributos.solicitud === "RECHAZADO") {
                this.alert_solicitud_type = "error";
                this.alert_solicitud_body = "RECHAZADO";
              } else {
                this.alert_solicitud_type = "info";
                this.alert_solicitud_body = "EN REVISIÓN";
              }
            }
            this.panelSolicitud = [0];
            this.cargandoSolicitud = false;
            setTimeout(() => {
              window.scrollTo({
                top: document.body.scrollHeight,
                behavior: "smooth",
              });
            }, 450);
          } else {
            if (data.status === 404) {
              this.cargandoSolicitud = false;
              this.alert_type = "error";
              this.alert_body =
                "El número de solicitud que ingresaste es inválido.";
              this.panelSolicitud = [];
              this.alert = true;
            } else {
              this.cargandoSolicitud = false;
              this.alert_type = "error";
              this.alert_body =
                "Hubo un error buscando esa solicitud. Intentá de nuevo más tarde.";
              this.panelSolicitud = [];
              this.alert = true;
            }
          }
        });
    },
  },
};
</script>