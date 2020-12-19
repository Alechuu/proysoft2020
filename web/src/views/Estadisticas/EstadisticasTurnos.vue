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
        <span style="color: white;text-align:left;">Comparar Centros</span>
      </v-card-title>
      <v-card-text class="mt-5">
        Acá podes comparar la cantidad de <b>Turnos</b> totales por cada
        <b>Centro</b>
        registrado.
      </v-card-text>
      <v-card-text>
        <v-autocomplete
          chips
          deletable-chips
          multiple
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
    </v-card>
    <transition name="fade">
      <v-card v-if="!emptyArray">
        <ve-bar
          class="mt-5 pa-0"
          :settings="chartSettings"
          :data="chartData"
        ></ve-bar>
      </v-card>
    </transition>
  </v-container>
</template>

<script>
export default {
  name: "EstadisticasTurnos",
  data() {
    this.chartSettings = {
      dataOrder: {
        label: "turnos",
        order: "desc",
      },
    };
    return {
      emptyArray: true,
      descriptionLimit: 25,
      chartLimit: 10,
      entries: [],
      isLoading: false,
      model: null,
      search: null,
      chartData: {
        columns: ["centro", "turnos"],
        rows: [],
      },
    };
  },
  computed: {
    fields() {
      if (!this.model) return [];
      return Object.keys(this.model).map((key) => {
        return {
          key,
          value: this.model[key] || "n/a",
        };
      });
    },
    items() {
      return this.entries.map((entry) => {
        const Description =
          entry.centro.length > this.descriptionLimit
            ? entry.centro.slice(0, this.descriptionLimit) + "..."
            : entry.centro;
        entry.centro =
          entry.centro.length > this.chartLimit
            ? entry.centro.slice(0, this.chartLimit) + "..."
            : entry.centro;

        return Object.assign({}, entry, { Description });
      });
    },
  },
  watch: {
    search() {
      // Items have already been loaded
      if (this.items.length > 0) return;

      // Items have already been requested
      if (this.isLoading) return;

      this.isLoading = true;

      // Lazily load input items
      fetch(process.env.VUE_APP_RUTA_API + "stats/turnos")
        .then((res) => res.json())
        .then((res) => {
          const { count, entries } = res;
          this.count = count;
          this.entries = entries;
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => (this.isLoading = false));
    },
    model() {
      /*       this.chartData["rows"].push({
        centro: this.model[this.model.length - 1].centro,
        turnos: this.model[this.model.length - 1].turnos,
      }); */
      if (this.model.length != 0) {
        this.emptyArray = false;
      } else {
        this.emptyArray = true;
      }
      this.chartData["rows"] = this.model;
    },
  },
};
</script>

<style lang="scss">
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
