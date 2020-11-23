<template>
  <validation-observer ref="observer" v-slot="{ invalid }">
    <v-overlay :value="overlay">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
    <v-alert
      class="ma-5"
      :value="alert"
      border="bottom"
      :type="alert_type"
      transition="scale-transition"
      >{{ alert_body }}
    </v-alert>
    <v-card class="pa-8 ma-5" color="primary" elevation="5">
      <div class="d-flex flex-column">
        <v-icon color="white" size="50"> mdi-home-heart </v-icon>
        <h1 style="text-align: center; color: white">
          Agregar un nuevo Centro
        </h1>
      </div>
    </v-card>
    <v-card class="pa-8 ma-5" elevation="5">
      <div class="d-flex flex-column">
        <v-icon size="45" color="primary">mdi-clipboard-edit</v-icon>
        <h3 class="pb-5" style="text-align: center; color: primary">
          Por favor, completá los siguientes datos
        </h3>
      </div>

      <v-divider class="mb-10"></v-divider>
      <form id="test_form" @submit.prevent="submit">
        <validation-provider
          v-slot="{ errors }"
          name="nombre"
          rules="required|max:50"
        >
          <v-text-field
            v-model="nombre"
            :counter="50"
            :error-messages="errors"
            label="Nombre"
            name="nombre"
            prepend-icon="mdi-text"
            required
          ></v-text-field>
        </validation-provider>
        <v-text-field
          v-model="web"
          :error-messages="errors"
          label="Sitio Web"
          name="sitio_web"
          prepend-icon="mdi-web"
          required
        ></v-text-field>
        <validation-provider
          v-slot="{ errors }"
          name="teléfono"
          rules="required|numeric"
        >
          <v-text-field
            v-model="telefono"
            :error-messages="errors"
            label="Teléfono"
            name="telefono"
            prepend-icon="mdi-phone"
            required
          ></v-text-field>
        </validation-provider>
        <validation-provider v-slot="{ errors }" name="tipo" rules="required">
          <v-text-field
            v-model="tipo"
            :error-messages="errors"
            label="Tipo"
            name="tipo"
            prepend-icon="mdi-text-box"
            required
          ></v-text-field>
        </validation-provider>
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
                label="Hora de Apertura"
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
                label="Hora de Cierre"
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
        <validation-provider
          v-slot="{ errors }"
          name="email"
          rules="required|email"
        >
          <v-text-field
            v-model="email"
            :error-messages="errors"
            label="E-mail"
            name="email"
            prepend-icon="mdi-at"
            required
          ></v-text-field>
        </validation-provider>
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
            label="Municipio"
            name="municipio"
            data-vv-name="select"
            prepend-icon="mdi-home-map-marker"
            required
          ></v-select>
        </validation-provider>
        <validation-provider
          v-slot="{ errors }"
          name="direccion"
          rules="required"
        >
          <v-text-field
            v-model="direccion"
            :error-messages="errors"
            label="Dirección"
            name="direccion"
            prepend-icon="mdi-map-marker"
            required
          ></v-text-field>
        </validation-provider>

        <v-file-input
          accept="application/pdf"
          label="PDF Visita"
          name="path_pdf"
        ></v-file-input>

        <v-btn class="mr-4" type="submit" :disabled="invalid" color="primary">
          enviar
        </v-btn>
      </form>
    </v-card>
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

setInteractionMode("eager");

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
  data: () => ({
    alert: false,
    alert_type: "success",
    alert_body: "",
    overlay: false,
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
    errors: null,
    items: [],
    checkbox: null,
  }),
  created() {
    this.fetchMunicipios();
  },
  methods: {
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
            this.overlay = false;
            this.alert_type = "success";
            this.alert_body =
              "Solicitud de Centro aceptada exitosamente. Estará pendiente de aprobación";
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
              "Hubo un error procesando tu solicitud, por favor, intentá de nuevo";
            this.alert = true;
            console.log(data);
            console.log("Hubo un error");
          }
        });
    },
    allowedStep: (m) => m % 30 === 0,
  },
};
</script>