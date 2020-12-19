<template>
  <v-container>
    <v-card class="mt-5" color="primary" elevation="5">
      <div class="pa-5" style="text-align: center">
        <v-icon color="white" size="50"> mdi-chart-bar </v-icon>
        <h1 class="text-h4" style="text-align: center; color: white">
          Franjas Horarias mas concurridas
        </h1>
      </div>
    </v-card>

    <v-card class="mt-5">
      <v-card-title class="headline primary">
        <span style="color: white">Turnos por Franjas Horarias</span>
      </v-card-title>
      <v-card-text class="mt-5">
        Acá podes comparar la cantidad de <b>Turnos</b> totales por cada
        <b>Centro</b>
        registrado.
      </v-card-text>
      
    </v-card>


    <!--  <div class="container">
    <line-chart
      :chartdata="chartdata"
      
      :options="options"/>
    </div> -->
    <transition name="fade">
      <v-card >
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
  name: "EstadisticasHorarios",
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
        columns: ["horario", "turnos"],
        rows: [],
      },
    };
  },

  async mounted () {
    this.loaded = false
    try {
      await fetch(process.env.VUE_APP_RUTA_API + "stats/horarios")
      .then((res) => res.json())
        .then((res) => {
          const { count, entries } = res;
          this.count = count;
          this.entries = entries;
          this.chartData['rows']= this.entries
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => (this.isLoading = false));

    
    } catch (e) {
      console.error(e)
    }
  },
  
}


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