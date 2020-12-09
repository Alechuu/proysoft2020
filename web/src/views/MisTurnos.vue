<template>
  <v-container>
    <v-card class="mt-5" color="primary" elevation="5">
      <div class="pa-5" style="text-align: center">
        <v-icon color="white" size="50"> mdi-calendar-search </v-icon>
        <h1 class="text-h4" style="text-align: center; color: white">
          Mis Turnos
        </h1>
      </div>
    </v-card>
    <v-card class="pa-8 mt-5 mb-5" elevation="5">
      <div style="text-align: center">
        <v-icon size="45" color="primary">mdi-calendar-multiple-check</v-icon>
        <h3
          class="text-h6 pb-5"
          style="text-align: center; color: primary; font-family: Noto Sans SC"
        >
          Acá podés revisar todos tus turnos solicitados
        </h3>
        <h4 class="text-subtitle-1 pb-3" style="text-align: center">
          Completá los datos y hacé click en <b>Ver Turnos</b>
        </h4>
      </div>
      <div class="d-flex flex-column">
        <v-divider></v-divider>
        <validation-observer ref="observer" v-slot="{ invalid }">
          <v-row>
            <v-col md="6" cols="12">
              <v-menu
                v-model="menuFecha"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <validation-provider
                    v-slot="{ errors }"
                    name="fecha"
                    rules="required"
                  >
                    <v-text-field
                      v-model="computedDateFormatted"
                      :error-messages="errors"
                      label="Fecha a consultar"
                      name="fecha"
                      id="fecha"
                      persistent-hint
                      prepend-icon="mdi-calendar"
                      elevation="15"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                    ></v-text-field>
                  </validation-provider>
                </template>
                <v-date-picker
                  v-model="date"
                  :allowed-dates="disablePastDates"
                  @input="changeFecha"
                ></v-date-picker>
              </v-menu>
            </v-col>
            <v-col md="6" cols="12">
              <validation-provider
                v-slot="{ errors }"
                name="e-mail"
                rules="required|email"
              >
                <v-text-field
                  v-model="emailSolicitante"
                  :error-messages="errors"
                  name="emailSolicitante"
                  id="emailSolicitante"
                  label="Tu E-mail"
                  prepend-icon="mdi-at"
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
                >Ver Turnos</v-btn
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
              <div style="color: white" class="text-body-1">Turnos</div>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-divider></v-divider>
              <v-data-table
                dense
                :headers="headers"
                :items="turnos"
                item-key="name"
                class="mt-5 elevation-3"
                hide-default-footer
              >
                <template v-slot:[`item.actions`]="{ item }">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon
                        v-bind="attrs"
                        v-on="on"
                        class="mr-2"
                        @click="convertirPDF(item)"
                      >
                        mdi-file-pdf
                      </v-icon>
                    </template>
                    <span>Descargar Turno en formato PDF</span>
                  </v-tooltip>
                </template></v-data-table
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
import { jsPDF } from "jspdf";
import { required, numeric, email } from "vee-validate/dist/rules";
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

extend("email", {
  ...email,
  message: "El campo {_field_} debe ser un e-mail válido",
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
      emailSolicitante: "",
      date: new Date().toISOString().substr(0, 10),
      panelSolicitud: [],
      cargandoSolicitud: false,
      items: 1,
      alert_type: "error",
      alert: false,
      alert_body: "",
      menuFecha: false,
      headers: [
        {
          text: "Fecha",
          sortable: false,
          value: "fecha",
        },
        {
          text: "Hora Inicio",
          align: "start",
          value: "hora_inicio",
        },
        { text: "Hora Fin", value: "hora_fin" },
        { text: "Centro", value: "centro" },
        { text: "PDF", sortable: false, value: "actions" },
      ],
      turnos: [],
    };
  },

  computed: {
    computedDateFormatted() {
      return this.formatDate(this.date);
    },
  },

  methods: {
    buscarSolicitud() {
      this.cargandoSolicitud = true;
      this.panelSolicitud = [];
      this.alert = false;
      var email = document.getElementById("emailSolicitante").value;
      function formatDateISO(date) {
        const [day, month, year] = date.split("/");
        return `${year}-${month}-${day}`;
      }
      var fecha = formatDateISO(document.getElementById("fecha").value);
      console.log(email, fecha);
      fetch(
        process.env.VUE_APP_RUTA_API +
          "turnos?fecha=" +
          fecha +
          "&" +
          "email=" +
          email,
        {
          method: "GET",
        }
      )
        .then((res) => res.json())
        .then((data) => {
          if (data.status === 200) {
            this.turnos = [];
            for (var turno in data.body) {
              this.turnos.push({
                fecha: data.body[turno]["turno"]["datos"].fecha,
                hora_inicio: data.body[turno]["turno"]["datos"].hora_inicio,
                hora_fin: data.body[turno]["turno"]["datos"].hora_fin,
                centro: data.body[turno]["turno"]["centro"].nombre,
                municipio: data.body[turno]["turno"]["centro"].municipio,
                direccion: data.body[turno]["turno"]["centro"].direccion,
                email_visitante:
                  data.body[turno]["turno"]["datos"].email_visitante,
                telefono_visitante:
                  data.body[turno]["turno"]["datos"].telefono_visitante,
              });
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
                "No se encontraron Turnos para los parámetros solicitados.";
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
    disablePastDates(val) {
      return val >= new Date().toISOString().substr(0, 10);
    },
    changeFecha() {
      this.menuFecha = false;
    },
    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split("-");
      return `${day}/${month}/${year}`;
    },
    formatTime(time) {
      if (!time) return null;
      const [horas, minutos] = time.split(":");
      return `${horas}:${minutos}`;
    },
    convertirPDF(turno) {
      console.log(turno.municipio);
      const doc = new jsPDF();
      //Titulo centrado
      doc.setFontSize(22);
      doc.text("Resumen del Turno", 105, 10, null, null, "center");
      doc.setLineWidth(1);
      doc.line(0, 15, 300, 15);
      doc.text("Datos Personales", 105, 22.5, null, null, "center");
      doc.setLineWidth(1);
      doc.line(0, 25, 300, 25);
      doc.setFontSize(16);
      doc.text("Correo: " + turno.email_visitante, 10, 35);
      doc.text("Teléfono: " + turno.telefono_visitante, 10, 45);
      doc.setLineWidth(1);
      doc.line(0, 50, 300, 50);
      doc.setFontSize(22);
      //doc.text("-----------------------", 105, 10, null, null, "center");
      doc.text("Datos del Centro", 105, 60, null, null, "center");
      //doc.text("-----------------------", 105, 10, null, null, "center");
      doc.setLineWidth(1);
      doc.line(0, 65, 300, 65);
      doc.setFontSize(16);
      doc.text("Nombre: " + turno.centro, 10, 75);
      doc.text("Municipio: " + turno.municipio, 10, 85);
      //doc.text("Dirección: " + turno.direccion, 10, 30);
      doc.setFontSize(22);
      doc.setLineWidth(1);
      doc.line(0, 90, 300, 90);
      //doc.text("-----------------------", 105, 10, null, null, "center");
      doc.text("Datos del Turno", 105, 100, null, null, "center");
      //doc.text("-----------------------", 105, 10, null, null, "center");
      doc.setLineWidth(1);
      doc.line(0, 105, 300, 105);
      doc.setFontSize(16);
      doc.text("Fecha: " + this.formatDate(turno.fecha), 10, 115);
      doc.text(
        "Hora de Inicio: " + this.formatTime(turno.hora_inicio),
        10,
        125
      );
      doc.text("Hora de Fin: " + this.formatTime(turno.hora_fin), 10, 135);
      doc.save("Turno.pdf");
    },
  },
};
</script>