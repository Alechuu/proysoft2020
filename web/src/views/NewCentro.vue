<template>
  <validation-observer ref="observer" v-slot="{ invalid }">
    <v-card class="pa-8 ma-5">
      <form id="test_form" @submit.prevent="submit">
        <validation-provider
          v-slot="{ errors }"
          name="Nombre"
          rules="required|max:50"
        >
          <v-text-field
            v-model="name"
            :counter="50"
            :error-messages="errors"
            label="Nombre"
            prepend-icon="mdi-text"
            required
          ></v-text-field>
        </validation-provider>
        <validation-provider
          v-slot="{ errors }"
          name="teléfono"
          rules="required|numeric"
        >
          <v-text-field
            v-model="telefono"
            :error-messages="errors"
            label="Teléfono"
            prepend-icon="mdi-phone"
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
            <v-text-field
              v-model="time_apertura"
              label="Hora de Apertura"
              prepend-icon="mdi-clock-time-four-outline"
              readonly
              v-bind="attrs"
              v-on="on"
              required
            ></v-text-field>
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
            <v-text-field
              v-model="time_cierre"
              label="Hora de Cierre"
              prepend-icon="mdi-clock-time-four-outline"
              readonly
              v-bind="attrs"
              v-on="on"
              required
            ></v-text-field>
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
            :error-messages="errors"
            label="Municipio"
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
            prepend-icon="mdi-map-marker"
            required
          ></v-text-field>
        </validation-provider>

        <v-file-input
          accept="application/pdf"
          label="PDF Visita"
        ></v-file-input>

        <v-btn class="mr-4" type="submit" :disabled="invalid" color="primary">
          enviar
        </v-btn>
        <v-btn @click="clear" color="warning"> limpiar formulario </v-btn>
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
    name: "",
    telefono: "",
    direccion: "",
    email: "",
    select: null,
    time_apertura: null,
    time_cierre: null,
    menu_apertura: false,
    menu_cierre: false,
    items: ["Item 1", "Item 2", "Item 3", "Item 4"],
    checkbox: null,
  }),

  methods: {
    submit() {
      this.$refs.observer.validate();
    },
    clear() {
      this.name = "";
      this.email = "";
      this.select = null;
      this.checkbox = null;
      this.$refs.observer.reset();
    },
    allowedStep: (m) => m % 30 === 0,
  },
};
</script>