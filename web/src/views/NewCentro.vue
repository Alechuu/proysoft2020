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
            <v-btn outlined v-if="mostrarBotonAlert" @click="verSolicitud"
              >Ver Solicitud</v-btn
            >
          </v-col>
        </v-row>
      </v-alert>
      <v-card class="mt-5" color="primary" elevation="5">
        <div class="pa-5" style="text-align: center">
          <v-icon color="white" size="50"> mdi-home-heart </v-icon>
          <h1 class="text-h4" style="text-align: center; color: white">
            Agregar un nuevo Centro
          </h1>
        </div>
      </v-card>
      <v-card class="pa-8 mt-5 mb-5" elevation="5">
        <div style="text-align: center">
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
          <v-row>
            <v-col md="6" cols="12">
              <validation-provider
                v-slot="{ errors }"
                name="nombre"
                rules="required|max:50"
              >
                <v-text-field
                  v-model="nombre"
                  :counter="50"
                  :error-messages="errors"
                  label="Nombre *"
                  name="nombre"
                  prepend-icon="mdi-text"
                  required
                ></v-text-field>
              </validation-provider>
            </v-col>
            <v-col md="6" cols="12">
              <v-text-field
                v-model="web"
                :error-messages="errors"
                label="Sitio Web"
                name="sitio_web"
                prepend-icon="mdi-web"
              ></v-text-field>
            </v-col>
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
                name="tipo"
                rules="required"
              >
                <v-text-field
                  v-model="tipo"
                  :error-messages="errors"
                  label="Tipo (Ropa, Alimentos, Sangre, etc) *"
                  name="tipo"
                  prepend-icon="mdi-text-box"
                  required
                ></v-text-field>
              </validation-provider>
            </v-col>
            <v-col md="6" cols="12">
              <v-menu
                ref="menu_apertura"
                v-model="menu_apertura"
                :close-on-content-click="false"
                :nudge-right="40"
                :return-value.sync="time_apertura"
                transition="scale-transition"
                offset-y
                max-width="290px"
                min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <validation-provider
                    v-slot="{ errors }"
                    name="Hora de Apertura"
                    rules="required"
                  >
                    <v-text-field
                      v-model="time_apertura"
                      label="Hora de Apertura *"
                      name="hora_apertura"
                      prepend-icon="mdi-clock-time-four-outline"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      required
                      :error-messages="errors"
                    ></v-text-field>
                  </validation-provider>
                </template>
                <v-time-picker
                  v-if="menu_apertura"
                  v-model="time_apertura"
                  format="24hr"
                  :allowed-minutes="allowedStep"
                  min="9:00"
                  :max="time_cierre"
                  full-width
                  @click:minute="$refs.menu_apertura.save(time_apertura)"
                ></v-time-picker>
              </v-menu>
            </v-col>
            <v-col md="6" cols="12">
              <v-menu
                ref="menu_cierre"
                v-model="menu_cierre"
                :close-on-content-click="false"
                :nudge-right="40"
                :return-value.sync="time_cierre"
                transition="scale-transition"
                offset-y
                max-width="290px"
                min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <validation-provider
                    v-slot="{ errors }"
                    name="Hora de Cierre"
                    rules="required"
                  >
                    <v-text-field
                      v-model="time_cierre"
                      label="Hora de Cierre *"
                      name="hora_cierre"
                      prepend-icon="mdi-clock-time-four-outline"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      required
                      :error-messages="errors"
                    ></v-text-field>
                  </validation-provider>
                </template>
                <v-time-picker
                  v-if="menu_cierre"
                  v-model="time_cierre"
                  format="24hr"
                  :allowed-minutes="allowedStep"
                  :min="time_apertura"
                  max="16:00"
                  full-width
                  @click:minute="$refs.menu_cierre.save(time_cierre)"
                ></v-time-picker>
              </v-menu>
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
            <v-col md="6" cols="12">
              <validation-provider
                v-slot="{ errors }"
                name="PDF"
                rules="required"
              >
                <v-file-input
                  v-model="pdf_visita"
                  :error-messages="errors"
                  @click:append="mostrarAyuda"
                  append-icon="mdi-help-circle"
                  accept="application/pdf"
                  label="PDF Visita *"
                  name="path_pdf"
                ></v-file-input>
              </validation-provider>
            </v-col>
            <v-col md="6" cols="12">
              <validation-provider
                v-slot="{ errors }"
                name="municipio"
                rules="required"
              >
                <v-select
                  v-model="select"
                  :items="items"
                  item-text="mun_nombre"
                  item-value="mun_nombre"
                  :error-messages="errors"
                  label="Municipio *"
                  name="municipio"
                  id="municipio"
                  data-vv-name="select"
                  prepend-icon="mdi-map"
                  required
                ></v-select>
              </validation-provider>
            </v-col>
            <v-col md="6" cols="12">
              <validation-provider
                v-slot="{ errors }"
                name="direccion"
                rules="required"
              >
                <v-text-field
                  v-model="direccion"
                  :error-messages="errors"
                  label="Dirección *"
                  name="direccion"
                  prepend-icon="mdi-map-marker"
                  required
                ></v-text-field>
              </validation-provider>
            </v-col>
          </v-row>
          <div class="d-flex flex-column ml-10">
            <v-alert type="info" dense border="bottom">
              Elegí un <b>municipio</b>, ingresá una <b>dirección</b> y hacé
              click en
              <b>Ver en Mapa</b>
            </v-alert>
            <v-btn class="mb-5" color="primary" @click="verEnMapa">
              Ver en Mapa
            </v-btn>
          </div>

          <v-alert
            v-model="resetAlertMapa"
            :value="alertMapa"
            class="ml-10"
            style="width: 50%"
            type="warning"
            transition="scale-transition"
            dismissible
            dense
            border="bottom"
          >
            Ups, no encontramos esa dirección. Revisala e intentá de nuevo.
          </v-alert>
          <v-card class="ml-10">
            <div>
              <l-map
                @click="agregarMarker"
                :zoom="zoom"
                :minZoom="minZoom"
                :bounds="bounds"
                :max-bounds="maxBounds"
                :center="center"
                ref="mapaCentro"
                style="height: 450px; width: 100%; z-index: 1"
              >
                <l-tile-layer :url="url" :attribution="attribution" />
                <l-marker :lat-lng="marker">
                  <l-tooltip
                    v-html="pin_help"
                    :options="{ permanent: true, interactive: true }"
                  >
                    <div>
                      {{ pin_help }}
                    </div>
                  </l-tooltip>
                </l-marker>
              </l-map>
              <v-overlay :absolute="true" :value="overlayMapa">
                <v-progress-circular
                  indeterminate
                  size="64"
                ></v-progress-circular>
              </v-overlay>
            </div>
          </v-card>
          <div class="text-center">
            <v-dialog v-model="dialog" width="500">
              <v-card>
                <v-card-title class="headline primary">
                  <h4 style="color: white">PDF con información de visita</h4>
                </v-card-title>

                <v-card-text class="mt-5">
                  Te solicitamos que subas un PDF especificando el protocolo de
                  visita que se debe respetar para poder ir al Centro. <br />
                  Por ejemplo, como se manejan con los turnos, indicar que se
                  tiene que llevar barbijo, respetar la distancia social, entre
                  otros. <br />
                  Esto quedará disponible para las personas que vayan a visitar
                  el Centro.
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" text @click="dialog = false">
                    Entendí
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>

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
          <!-- Hidden inputs para coordenadas  -->
          <input
            type="hidden"
            name="latitud"
            id="latitud"
            :value="latitudInput"
          />
          <input
            type="hidden"
            name="longitud"
            id="longitud"
            :value="longitudInput"
          />
        </form>
      </v-card>
    </v-container>
  </validation-observer>
</template>


<script>
import "leaflet/dist/leaflet.css";
import { latLngBounds, latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LTooltip } from "vue2-leaflet";
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
  name: "CrearCentro",
  components: {
    ValidationProvider,
    ValidationObserver,
    LMap,
    LTileLayer,
    LMarker,
    LTooltip,
  },
  data() {
    return {
      // Datos Leaflet
      minZoom: 6,
      zoom: 6,
      center: [-37.3121792, -61.3996217],
      bounds: latLngBounds([-33.275, -63.402], [-41.071, -56.415]),
      maxBounds: latLngBounds([-32.602, -65.237], [-41.673, -50.515]),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      marker: latLng(0, 0),
      pin_help:
        "Esta sería la ubicación del Centro.<br />" +
        "Si es errónea, simplemente<br />" +
        "hacé click en la ubicación correcta<br />" +
        "y se guardará.",

      // Datos Alerta
      resetAlert: false,
      alert: false,
      alert_type: "success",
      alert_body: "",
      alert_cerrar: false,
      mostrarBotonAlert: true,
      resetAlertMapa: false,
      alertMapa: false,

      // Loading animacion
      overlay: false,
      overlayMapa: false,

      // Datos formulario
      nombre: "",
      telefono: "",
      direccion: "",
      email: "",
      web: "",
      tipo: "",
      select: null,
      time_apertura: null,
      time_cierre: null,
      menu_apertura: false,
      menu_cierre: false,
      pdf_visita: null,
      errors: null,
      items: [],
      checkbox: null,
      dialog: false,
      latitudInput: "",
      longitudInput: "",
      idCentroSolicitud: null,
    };
  },

  created() {
    this.fetchMunicipios();
  },
  mounted() {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: "smooth",
    });
  },
  methods: {
    // Función que trae los municipios para llenar el Select
    fetchMunicipios() {
      fetch(
        "https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135"
      )
        .then((res) => res.json())
        .then((data) => {
          for (var municipio in data.data.Town) {
            this.items.push({
              mun_id: data.data.Town[municipio].id,
              mun_nombre: data.data.Town[municipio].name,
            });
          }
        });
    },

    // Submit del formulario junto a sus chequeos + Alertas
    submit() {
      this.$refs.observer.validate();
      this.overlay = true;
      const form_data = new FormData(document.getElementById("test_form"));
      fetch("http://127.0.0.1:5000/api/centros", {
        method: "POST",
        body: form_data,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.status === "201 Created") {
            this.limpiarFormulario();
            this.idCentroSolicitud = data.body.atributos.id;
            this.overlay = false;
            this.alert_type = "success";
            this.alert_body =
              "Solicitud de Centro aceptada exitosamente. Estará pendiente de aprobación";
            this.resetAlert = true;
            this.alert_cerrar = false;
            this.mostrarBotonAlert = true;
            this.alert = true;
            window.scrollTo({
              top: 0,
              left: 0,
              behavior: "smooth",
            });
          } else {
            this.overlay = false;
            window.scrollTo({
              top: 0,
              left: 0,
              behavior: "smooth",
            });
            this.alert_type = "error";
            this.alert_body =
              "Hubo un error procesando tu solicitud. Por favor, intentá de nuevo.";
            this.resetAlert = true;
            this.mostrarBotonAlert = false;
            this.alert_cerrar = true;
            this.alert = true;
          }
        });
    },

    // Esto limpia el formulario si la solicitud fue exitosa
    limpiarFormulario() {
      this.nombre = "";
      this.telefono = "";
      this.direccion = "";
      this.email = "";
      this.web = "";
      this.tipo = "";
      this.select = null;
      this.time_apertura = null;
      this.time_cierre = null;
      this.menu_apertura = false;
      this.menu_cierre = false;
      this.pdf_visita = null;
      this.$refs.observer.reset();
    },

    // Esto controla que el horario sea de 30 a 30 minutos
    allowedStep: (m) => m % 30 === 0,

    // Esto abre el popup de ayuda

    mostrarAyuda() {
      this.dialog = true;
    },

    // Funciones de Leaflet

    agregarMarker(event) {
      if (this.bounds.contains(latLng(event.latlng.lat, event.latlng.lng))) {
        this.pin_help = "¡Ubicación guardada!";
        this.marker = latLng(event.latlng.lat, event.latlng.lng);
        this.latitudInput = event.latlng.lat;
        this.longitudInput = event.latlng.lng;
      }
    },

    verEnMapa() {
      this.overlayMapa = true;
      var dataDir = encodeURI(
        this.direccion +
          ", Municipio " +
          this.select +
          ", Provincia de Buenos Aires, Argentina"
      );
      fetch(
        "https://geocode.search.hereapi.com/v1/geocode?apikey=s0gvC3NKNulSUn6DSTyhf4jCcwVL5TN7C5oBELvwf3I&q=" +
          dataDir
      )
        .then((response) => response.json())
        .then((data) => {
          if (data["items"][0] === undefined) {
            this.resetAlertMapa = true;
            this.alertMapa = true;
            this.overlayMapa = false;
          }
          var lat = data["items"][0]["position"]["lat"];
          var lng = data["items"][0]["position"]["lng"];
          this.pin_help =
            "Esta sería la ubicación del Centro.<br />" +
            "Si es errónea, simplemente<br />" +
            "hacé click en la ubicación correcta<br />" +
            "y se guardará.";
          this.marker = latLng(lat, lng);
          this.overlayMapa = false;
          this.$refs.mapaCentro.mapObject.setView([lat, lng], 18);
        });
    },

    // Redirigie para ver la solcitud
    verSolicitud() {
      this.$router.push({
        path: "/v/centros/estado",
        query: { id: this.idCentroSolicitud },
      });
    },
  },
};
</script>
