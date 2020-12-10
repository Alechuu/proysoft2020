<template>
  <v-container>
    <v-card class="mt-5" color="primary" elevation="5">
      <div class="pa-5" style="text-align: center">
        <v-icon color="white" size="50"> mdi-chart-bar </v-icon>
        <h1 class="text-h4" style="text-align: center; color: white">
          Cantidad de Turnos por Centro
        </h1>
      </div>
    </v-card>
    <v-card class="mt-5">
      <v-card-title class="headline primary">
        <span style="color:white;">Buscá un Centro para compararlo</span>
      </v-card-title>
      <v-card-text class="mt-5">
        Acá podes comparar la cantidad de <b>Turnos</b> totales por cada
        <b>Centro</b>
        registrado.
      </v-card-text>
      <v-card-text>
        <v-autocomplete
          v-model="model"
          :items="items"
          :loading="isLoading"
          :search-input.sync="search"
          hide-no-data
          hide-selected
          item-text="Description"
          item-value="API"
          label="Centros Registrados"
          placeholder="Empezá a escribir para Buscar..."
          prepend-icon="mdi-home-search"
          return-object
        ></v-autocomplete>
      </v-card-text>
      <v-divider></v-divider>
      <v-expand-transition>
        <v-list v-if="model">
          <v-list-item v-for="(field, i) in fields" :key="i">
            <v-list-item-content>
              <v-list-item-title v-text="field.value"></v-list-item-title>
              <v-list-item-subtitle v-text="field.key"></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-expand-transition>
    </v-card>
    <v-card class="mt-5 pa-5" elevation="5">
      <ve-bar :data="chartData"></ve-bar>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      chartData: {
        columns: ["centro", "turnos"],
        rows: [
          { centro: "Centro 1", turnos: 123 },
          { centro: "Centro 2", turnos: 1223 },
          { centro: "Centro 3", turnos: 2123 },
          { centro: "Centro 4", turnos: 4123 },
          { centro: "Centro 5", turnos: 3123 },
          { centro: "Centro 6", turnos: 200 },
        ],
      },
    };
  },
};
</script>
