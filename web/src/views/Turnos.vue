<template>
  <validation-observer ref="observer" v-slot="{ invalid }">
    <v-overlay :value="overlay">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
    <v-container>
      <v-alert
        v-model="resetAlert"
        :type="alert_type"
        :value="alert"
        :dismissible="alert_cerrar"
        border="bottom"
        transition="scale-transition"
        prominent
      >
        <v-row align="center">
          <v-col class="grow">
            {{ alert_body }}
          </v-col>
          <v-col class="shrink">
            <v-btn outlined v-if="mostrarBotonAlert" @click="descargarPDFResumenTurno"
              >Descargar PDF</v-btn
            >
          </v-col>
        </v-row>
      </v-alert>
      <v-card class="mt-5" color="primary" elevation="5">
        <div class="pa-5" style="text-align: center">
          <v-icon color="white" size="50"> mdi-calendar-month </v-icon>
          <h1 class="text-h4" style="text-align: center; color: white">
            Solicitud de turno
          </h1>
          <h6 class="text-h6 pb-5" style="text-align: left; color: white">
            Para concurrir a nuestros centros, necesitas previamente solicitar
            un turno, que te permitirá acercarte a nosotros en los horarios
            habituales de atención.
          </h6>
        </div>
      </v-card>
      <v-card class="pa-8 mt-5 mb-5" elevation="5">
        <div class="d-flex flex-column">
          <v-icon size="45" color="primary">mdi-clipboard-edit</v-icon>
          <h3 class="text-h6 pb-5" style="text-align: center; color: primary">
            Por favor, completá los siguientes datos
          </h3>
          <h5 class="font-weight-light pb-3" style="text-align: center">
            Los campos requeridos están marcados con un *
          </h5>
        </div>

        <v-divider class="mb-10"></v-divider>
        <form id="form_turnos" @submit.prevent="submit">
          <h3 class="text-h6 pb-5" style="text-align: center; color: primary">
            Datos Personales
          </h3>
          <v-row>
            <v-col md="6" cols="12">
              <validation-provider
                v-slot="{ errors }"
                name="teléfono"
                rules="required|numeric"
              >
                <v-text-field
                  v-model="telefono"
                  :error-messages="errors"
                  label="Teléfono *"
                  name="telefono_visitante"
                  prepend-icon="mdi-phone"
                  required
                ></v-text-field>
              </validation-provider>
            </v-col>
            <v-col md="6" cols="12">
              <validation-provider
                v-slot="{ errors }"
                name="email"
                rules="required|email"
              >
                <v-text-field
                  v-model="email"
                  :error-messages="errors"
                  label="E-mail *"
                  name="email_visitante"
                  prepend-icon="mdi-at"
                  required
                ></v-text-field>
              </validation-provider>
            </v-col>
          </v-row>
          <h3 class="text-h6 pb-5" style="text-align: center; color: primary">
            Centro de Ayuda
          </h3>
          <v-row>
            <v-col md="6" cols="12">
              <v-select
                v-model="selectMunicipio"
                :items="itemsMunicipios"
                item-text="mun_nombre"
                item-value="mun_nombre"
                :error-messages="errors"
                label="Municipio"
                name="municipio"
                id="municipio"
                prepend-icon="mdi-map"
                clearable="true"
                v-on:change="changeMunicipio"
              ></v-select>
            </v-col>
            <v-col md="6" cols="12">
              <validation-provider
                v-slot="{ errors }"
                name="centro"
                rules="required"
              >
                <v-select
                  v-model="selectCentro.centro_id"
                  :items="itemsCentro"
                  item-text="centro_nombre"
                  item-value="centro_id"
                  :error-messages="errors"
                  label="Centro Ayuda *"
                  name="centro"
                  id="centro"
                  data-vv-name="select"
                  prepend-icon="mdi-map"
                  required
                  v-on:change="changeCentro"
                ></v-select>
              </validation-provider>
            </v-col>
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
                  <v-text-field
                    v-model="computedDateFormatted"
                    label="Fecha del turno"
                    name="fecha"
                    id="fecha"
                    persistent-hint
                    prepend-icon="mdi-calendar"
                    elevation="15"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
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
                name="hora"
                rules="required"
              >
                <v-select
                  v-model="selectHorarios"
                  :items="itemsHorarios"
                  item-text="hora_inicio"
                  item-value="hora_inicio"
                  name="hora_inicio"
                  return-object
                  attach
                  chips
                  label="Horarios"
                  prepend-icon="mdi-clock-time-three"
                  :error-messages="errors"
                  required
                ></v-select>
              </validation-provider>
            </v-col>
          </v-row>

          <v-btn
            class="mr-4 mt-10"
            x-large
            style="width: 100%"
            type="submit"
            :disabled="invalid"
            color="success"
          >
            enviar
          </v-btn>
        </form>
      </v-card>
    </v-container>
  </validation-observer>
</template>

<script>
import { jsPDF } from "jspdf";
import { required, email, max, numeric } from "vee-validate/dist/rules";
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

extend("max", {
  ...max,
  message: "El campo {_field_} no puede tener más de {length} caracteres",
});

extend("email", {
  ...email,
  message: "Email inválido",
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
  data: (vm) => ({
    // Datos Alerta
    resetAlert: false,
    alert: false,
    alert_type: "success",
    alert_body: "",
    alert_cerrar: false,
    mostrarBotonAlert: true,
    // Datos formulario
    telefono: "",
    email: "",
    errors: null,
    selectMunicipio: null,
    itemsMunicipios: [],
    selectCentro: { centro_id: null },
    itemsCentro: [],
    itemsCentroAuxiliar: [],
    dialog: false,
    overlay: false,
    date: new Date().toISOString().substr(0, 10),
    dateFormatted: vm.formatDate(new Date().toISOString().substr(0, 10)),
    menuFecha: false,
    selectHorarios: null,
    itemsHorarios: [],
    //Datos PDF
    PDF_centro_ayuda: null,
    PDF_municipio: null,
    PDF_email_donante:null,
    PDF_telefono_donante: null,
    PDF_hora_inicio: null,
    PDF_hora_fin: null,
    PDF_fecha: null,
  }),
  computed: {
    computedDateFormatted() {
      return this.formatDate(this.date);
    },
  },
  created() {
    this.fetchMunicipios();
    this.fetchCentros();
    if (this.$route.query.id !== undefined) {
      this.selectCentro.centro_id = this.$route.query.id;
      this.changeCentro();
    }
  },
  mounted() {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: "smooth",
    });
  },
  methods: {
    //Campo de ayuda para filtrar los centros
    fetchMunicipios() {
      fetch(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135"
      )
        .then((res) => res.json())
        .then((data) => {
          for (var municipio in data.data.Town) {
            this.itemsMunicipios.push({
              mun_nombre: data.data.Town[municipio].name,
            });
          }
        });
    },
    // Función que trae los centros para llenar el Select
    fetchCentros() {
      fetch("http://127.0.0.1:5000/api/centros?pagina=1")
        .then((res) => res.json())
        .then((data) => {
          var centros = data.body.centros;
          for (var i = 0; i < centros.length; i++) {
            this.itemsCentro.push({
              centro_id: centros[i].id,
              centro_nombre: centros[i].nombre,
              centro_municipio: centros[i].municipio,
            });
            this.itemsCentroAuxiliar.push({
              centro_id: centros[i].id,
              centro_nombre: centros[i].nombre,
              centro_municipio: centros[i].municipio,
            });
          }
        });
    },
    changeMunicipio() {
      if (this.selectMunicipio != null) {
        var centrosFiltrados = [];
        for (var i = 0; i < this.itemsCentroAuxiliar.length; i++) {
          if (
            this.itemsCentroAuxiliar[i].centro_municipio == this.selectMunicipio
          ) {
            centrosFiltrados.push(this.itemsCentroAuxiliar[i]);
          }
        }
        this.itemsCentro = centrosFiltrados;
        this.selectCentro.centro_id = null;
        //borro los horarios por si hay seteados
        this.selectHorarios = null;
        this.itemsHorarios = [];
      } else {
        this.itemsCentro = this.itemsCentroAuxiliar;
      }
    },
    changeCentro() {
      if (this.selectCentro.centro_id != null) {
        fetch(
          "http://127.0.0.1:5000/api/centros/" +
            this.selectCentro.centro_id +
            "/turnos_disponibles?fecha=" +
            this.date
        )
          .then((res) => res.json())
          .then((data) => {
            var turnos = data.turnos;
            this.selectHorarios = null;
            this.itemsHorarios = [];
            for (var i = 0; i < turnos.length; i++) {
              this.itemsHorarios.push({
                hora_inicio: turnos[i].hora_inicio,
                hora_fin: turnos[i].hora_fin,
              });
            }
          });
      }
    },
    changeFecha() {
      this.menuFecha = false;
      this.selectHorarios = null;
      this.changeCentro();
    },
    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split("-");
      return `${day}/${month}/${year}`;
    },
    disablePastDates(val) {
      return val >= new Date().toISOString().substr(0, 10);
    },
    submit() {
      this.$refs.observer.validate();
      this.overlay = true;
      const form_data = new FormData(document.getElementById("form_turnos"));
      function formatDateISO(date) {
        const [day, month, year] = date.split("/");
        return `${year}-${month}-${day}`;
      }

      var fecha = formatDateISO(form_data.get("fecha"));
      form_data.set("fecha", fecha);
      form_data.set("hora_inicio", this.selectHorarios.hora_inicio);
      form_data.set("hora_fin", this.selectHorarios.hora_fin);
      fetch(
        "http://127.0.0.1:5000/api/centros/" +
          this.selectCentro.centro_id +
          "/reserva",
        {
          method: "POST",
          body: form_data,
        }
      )
        .then((res) => res.json())
        .then((data) => {
          if (data.status === "201 Created") {
            // Para descarga del PDF con los datos del turno
            this.PDF_centro_ayuda = this.selectCentro.centro_nombre;
            this.PDF_municipio = this.selectMunicipio;
            this.PDF_email_donante = data.body.atributos.email_donante;
            this.PDF_telefono_donante = data.body.atributos.telefono_donante;
            this.PDF_hora_inicio = data.body.atributos.hora_inicio;
            this.PDF_hora_fin = data.body.atributos.hora_fin;
            this.PDF_fecha = data.body.atributos.fecha;
            //Fin datos PDF
            this.limpiarFormulario();
            this.alert_type = "success";
            this.alert_body = data.details;
            this.mostrarBotonAlert = true;
          } else if (data.status === "400") {
            this.alert_type = "error";
            this.alert_body = data.details;
            this.mostrarBotonAlert = false;
          } else {
            this.alert_type = "error";
            this.alert_body =
              "Hubo un error procesando tu solicitud. Por favor, intentá de nuevo.";
            this.mostrarBotonAlert = false;
          }
          this.alert_cerrar = true;
          this.overlay = false;
          this.resetAlert = true;
          this.alert = true;
          window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth",
          });
        });
    },

    // Esto limpia el formulario si la solicitud fue exitosa
    limpiarFormulario() {
      this.telefono = "";
      this.email = "";
      this.fecha = "";
      this.selectCentro.centro_id = null;
      this.selectHorarios = null;
      this.$refs.observer.reset();
    },
    descargarPDFResumenTurno() {            
      const doc = new jsPDF();     
      //Titulo centrado
      doc.text("Resumen del Turno", 105, 10, null, null, "center");
      //Datos a izquierda
      doc.text("Nombre del centro de ayuda:" + this.PDF_centro_ayuda, 10, 20);

      doc.save("Reserva.pdf");
    },
  },
};
</script>