<template>
  <v-container>
    <v-card class="mt-5" color="primary" elevation="5">
      <div class="pa-5" style="text-align: center">
        <v-icon color="white" size="50"> mdi-chart-bar </v-icon>
        <h1 class="text-h4" style="text-align: center; color: white">
          Cantidad de Centros por Municipio
        </h1>
      </div>
    </v-card>
    <v-card class="mt-5 mb-5" elevation="5">
      <v-card-title class="headline primary">
        <span style="color: white">Turnos y Centros por Municipio</span>
      </v-card-title>
      <v-col md="6" cols="12">
        <v-select
          v-model="selectMunicipio"
          :items="itemsMunicipios"
          item-text="mun_nombre"
          item-value="mun_nombre"
          label="Municipio"
          name="municipio"
          id="municipio"
          prepend-icon="mdi-map"
          v-on:change="changeMunicipio"
        ></v-select>
      </v-col>
    </v-card>
    <v-card class="mt-5" elevation="5">
      <v-overlay :absolute="true" :value="isLoadingChart">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
      <ve-line class="pa-5" :data="chartData" :settings="chartSettings">
      </ve-line>
    </v-card>
  </v-container>
</template>

<script>
export default {
  //name: "Estadísticas Centro",
  data() {
    this.chartSettings = {
      labelMap: {
        a_fecha: "fecha",
        cant_centros: "cantidad de centros",
        cant_turnos: "cantidad de turnos",
      },
    };
    return {
      selectMunicipio: null,
      itemsMunicipios: [],
      chartData: {
        columns: ["a_fecha", "cant_centros", "cant_turnos"],
        rows: [],
      },
      isLoadingChart: false,
    };
  },
  mounted() {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: "smooth",
    });
  },
  created() {
    this.fetchMunicipios();
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
    changeMunicipio() {
      this.isLoadingChart = true;
      fetch(
        process.env.VUE_APP_RUTA_API +
          "stats/centros?municipio=" +
          this.selectMunicipio
      )
        .then((res) => res.json())
        .then((data) => {
          //borro los datos del grafico
          this.chartData["rows"] = [];
          var lista = data.lista;
          for (var i = 0; i < lista.length; i++) {
            this.chartData["rows"].push(lista[i]);
          }
          this.isLoadingChart = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
