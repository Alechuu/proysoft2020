<template>
  <v-container>
    <v-card class="mt-5" color="primary" elevation="5">
      <div class="pa-5" style="text-align: center">
        <v-icon color="white" size="50"> mdi-chart-bar </v-icon>
        <h1 class="text-h4" style="text-align: center; color: white">
          Cantidad de Centros por municipio
        </h1>
      </div>
    </v-card>
    <v-card class="pa-8 mt-5 mb-5" elevation="5">
      <h5 class="font-weight-light pb-3" style="text-align: left">
        Seleccione un municipio para ver el cuadro estadístico.
      </h5>
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
      <ve-line :data="chartData" :settings="chartSettings"> </ve-line>
    </v-card>
  </v-container>
</template>

<script>
export default {
  //name: "Estadísticas Centro",
  data() {
    this.chartSettings = {
      labelMap: {
        a_fecha: 'fecha',
        cant_centros: 'cantidad centros'
      }
    }
    return {
      selectMunicipio: null,
      itemsMunicipios: [],     
      chartData: {
        columns: ["a_fecha", 'cant_centros'],
        rows: [],
      },
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
      fetch(process.env.VUE_APP_RUTA_API + "stats/centros?municipio="+this.selectMunicipio)
        .then((res) => res.json())
        .then((data) => {
          //borro los datos del grafico
          this.chartData["rows"] = [];
          var lista = data.lista;
          for (var i = 0; i < lista.length; i++) {
            this.chartData["rows"].push(lista[i]);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>