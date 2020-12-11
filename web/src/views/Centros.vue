<template v-slot:top>
  <v-container>
    <v-card class="mt-5" color="primary" elevation="5">
      <div class="pa-5" style="text-align: center">
        <v-icon color="white" size="50"> mdi-home-search </v-icon>
        <h1 class="text-h4" style="text-align: center; color: white">
          Listado de Centros
        </h1>
      </div>
    </v-card>
    <v-card class="mt-6 mb-10" elevation="5">
      <v-card-title>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" @click="resetear" v-bind="attrs" v-on="on">
              Centrar Mapa
              <v-icon> mdi-map </v-icon>
            </v-btn>
          </template>
          <span>Toque para volver a centrar el Mapa</span>
        </v-tooltip>

        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Buscá por cualquier campo..."
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table :headers="headers" :items="centrosList" :search="search">
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small class="mr-2" @click="verEnMapa(item)">
            mdi-map-marker
          </v-icon>
          <v-icon small @click="sacarTurno(item)"> mdi-calendar </v-icon>
        </template>
      </v-data-table>
    </v-card>
    <v-card class="mb-10" elevation="5">
      <l-map
        ref="map"
        :zoom="zoom"
        :bounds="bounds"
        :center="center"
        :options="mapOptions"
        style="height: 450px; width: 100%; z-index: 1"
        @update:center="centerUpdate"
        @update:zoom="zoomUpdate"
      >
        <l-tile-layer :url="url" :attribution="attribution" />
        <div id="button-wrapper">
          <input type="button" id="Btn1" value="Btn1" class="btnStyle span3" />
        </div>
        <l-marker
          :key="id"
          v-for="(centro, id) in centrosList"
          :lat-lng="centro.position"
        >
          <l-popup>
            <h3>{{ centro.nombre }}</h3>
            <p><b>Direccion:</b> {{ centro.direccion }},</p>
            <p>
              <b>Horario:</b> {{ centro.hora_apertura }} -
              {{ centro.hora_cierre }}
            </p>
            <p><b>Telefono:</b> {{ centro.telefono }}</p>
          </l-popup>
        </l-marker>
      </l-map>
    </v-card>
  </v-container>
</template>

<script>
import "leaflet/dist/leaflet.css";
import { latLngBounds, latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";

export default {
  name: "Centros",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  data() {
    return {
      zoom: 6,
      center: latLng(-37.3121792, -61.3996217),
      bounds: latLngBounds([-32.602, -65.237], [-41.673, -50.515]),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',

      mapOptions: {
        zoomSnap: 0.5,
      },

      search: "",
      headers: [
        {
          text: "Nombre",
          align: "start",
          sortable: true,
          value: "nombre",
        },
        {
          text: "Municipio",
          align: "start",
          sortable: true,
          value: "municipio",
        },
        {
          text: "Direccion",
          align: "start",
          sortable: true,
          value: "direccion",
        },
        {
          text: "Telefono",
          align: "start",
          sortable: true,
          value: "telefono",
        },
        {
          text: "Apertura",
          align: "start",
          sortable: true,
          value: "hora_apertura",
        },
        {
          text: "Cierre",
          align: "start",
          sortable: true,
          value: "hora_cierre",
        },
        { text: "Acciones", value: "actions", sortable: false },
      ],
      centrosList: [],
      items: [],
    };
  },

  /*  initial()
  {
    this.traerCentros();
  }, */

  mounted() {
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: "smooth",
    });
  },

  created() {
    this.traerCentros();
  },

  methods: {
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },
    showLongText() {
      this.showParagraph = !this.showParagraph;
    },

    seleccionado() {
      alert("hola");
    },
    traerCentros() {
      /* for (var pagina in [1,2,3])
      {
        alert(pagina)
      } */
      fetch(process.env.VUE_APP_RUTA_API + "centros")
        .then((res) => res.json())
        .then((data) => {
          /* alert(data.body.centros[1].nombre); */
          /* this.centrosList = data; */

          for (var centro in data.body.centros) {
            this.centrosList.push({
              id: data.body.centros[centro].id,
              nombre: data.body.centros[centro].nombre,
              position: {
                lng: data.body.centros[centro].longitud,
                lat: data.body.centros[centro].latitud,
              },
              municipio: data.body.centros[centro].municipio,
              direccion: data.body.centros[centro].direccion.replace(
                ", Provincia de Buenos Aires",
                ""
              ),
              hora_apertura: data.body.centros[centro].hora_apertura,
              hora_cierre: data.body.centros[centro].hora_cierre,
              telefono: data.body.centros[centro].telefono,
            });
          }
        });
    },

    /*  traerCentrosPrueba() {
      fetch("http://127.0.0.1:5000/api/centros", {
        method: "GET",
      })
        .then((res) => res.json())
        .then((data) => {
          alert(data.body.centros[1].nombre); 
          
        }
        );
        
    }, */
    verEnMapa(centro) {
      this.$refs.map.mapObject.flyTo(centro.position, 14, {
        pan: {
          animate: true,
          duration: 1.5,
        },
        zoom: {
          animate: true,
        },
      });
      window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth",
      });
    },

    resetear() {
      this.$refs.map.mapObject.flyTo([-37.3121792, -61.3996217], 6, {
        pan: {
          animate: true,
          duration: 1.5,
        },
        zoom: {
          animate: true,
        },
      });
    },

    sacarTurno(centro) {
      this.$router.push({
        path: "/v/turnos/solicitud",
        query: { id: centro.id },
      });
    },
  },
};
</script>
