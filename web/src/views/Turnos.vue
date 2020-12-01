<template>
  <validation-observer ref="observer" v-slot="{ invalid }">
    <v-overlay :value="overlay">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
    <v-container>
      <v-card class="mt-5" color="primary" elevation="5">
        <div class="pa-5" style="text-align: center">
          <v-icon color="white" size="50"> mdi-calendar-month </v-icon>
          <h1 class="text-h4" style="text-align: center; color: white">
            Solicitud de turno
          </h1>
        </div>
      </v-card>
      <v-card class="mt-5" color="primary" elevation="5">
        <div class="pa-5" style="text-align: center">
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
        <form id="test_form" @submit.prevent="submit">
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
                  name="telefono"
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
                  name="email"
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
              <validation-provider
                v-slot="{ errors }"
                name="centro"
                rules="required"
              >
                <v-select
                  v-model="selectCentro"
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
                  @input="menuFecha = false"
                ></v-date-picker>
              </v-menu>
            </v-col>
            <v-col md="6" cols="12">
              <v-select
                v-model="valueHorarios"
                :items="itemsHorarios"
                attach
                chips
                label="Horarios"
                multiple
                prepend-icon="mdi-clock-time-three"
              ></v-select>
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
    // Datos formulario
    telefono: "",
    email: "",
    errors: null,
    selectCentro: null,
    itemsCentro: [],
    dialog: false,
    overlay: false,
    date: new Date().toISOString().substr(0, 10),
    dateFormatted: vm.formatDate(new Date().toISOString().substr(0, 10)),
    menuFecha: false,
    valueHorarios: "",
    itemsHorarios:[],
  }),
  computed: {
    computedDateFormatted() {
      return this.formatDate(this.date);
    },
  },
  created() {
    this.fetchCentros();
  },
  mounted() {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: "smooth",
    });
  },
  methods: {
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
            });
          }
        });
    },
      changeCentro() {
      if (this.selectCentro != null) {
        var headers = new Headers();
        headers.append("fecha", this.date);
        var request = new Request(
          "/api/centros/" + this.selectCentro.toString() + "/turnos_disponibles",
          {
            headers: headers,
          }
        );
        return fetch(request)
          .then((res) => res.json())
          .then((data) => {
            var turnos = data.turnos;
            for (var i = 0; i < turnos.length; i++) {
            this.itemsHorarios.push({
              hora_inicio: turnos[i].hora_inicio,              
            });
          }           
          });
      }      
    },

    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split("-");
      return `${day}/${month}/${year}`;
    },
    disablePastDates(val) {
      return val >= new Date().toISOString().substr(0, 10);
    },
    // Esto limpia el formulario si la solicitud fue exitosa
    limpiarFormulario() {
      //this.nombre = "";
      this.telefono = "";
      this.email = "";
      this.selectCentro = null;
      this.$refs.observer.reset();
    },
  },
};
</script>
