<template v-slot:top>
  <v-container>
    <v-card>
      <!-- <p>
          First marker is placed at {{ withPopup.lat }}, {{ withPopup.lng }}
        </p>
        <p>
          Center is at {{ currentCenter }} and the zoom is: {{ currentZoom }}
        </p>
        <button @click="showLongText">
          Toggle long popup
        </button>
        <button @click="showMap = !showMap">
          Toggle map
        </button> -->

      <v-card>
        <v-card-title>
          Centros de Ayuda
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers" :items="centrosList" :search="search">
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="verEnMapa(item)">
              mdi-map-marker
            </v-icon>
            <v-icon small @click="sacarTurno(item)">
              mdi-calendar
            </v-icon>
          </template>
        </v-data-table>
      </v-card>

      <l-map
        v-if="showMap"
        :zoom="zoom"
        :center="center"
        :options="mapOptions"
        style="height: 450px; width: 100%; z-index: 1"
        @update:center="centerUpdate"
        @update:zoom="zoomUpdate"
      >
        <l-tile-layer :url="url" :attribution="attribution" />

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
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";

export default {
  name: "Example",
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

      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      withPopup: latLng(47.41322, -1.219482),
      withTooltip: latLng(47.41422, -1.250482),
      currentZoom: 11.5,
      currentCenter: latLng(47.41322, -1.219482),
      showParagraph: false,
      mapOptions: {
        zoomSnap: 0.5,
      },
      showMap: true,
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

  created() {
    this.fetchMunicipios();
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
      fetch("http://127.0.0.1:5000/api/centros")
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
              direccion: data.body.centros[centro].direccion,
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
       return this.setView(centro.position, 12)
    },

    sacarTurno(centro) {
      alert(centro.nombre)
      /*  this.$router.push({
        path: "/v/centros/estado",
        query: { id: this.idCentroSolicitud },
      }); */
    },

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
  },
};
</script>
