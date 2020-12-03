<template>
  <div id="app">
    <l-map 
      :zoom="zoom"
      :center="center"
      style="height: 450px; width: 100%; z-index: 2">
      
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    </l-map>
    <h2>Hola</h2>
  </div>
  
</template>

<script>
import "leaflet/dist/leaflet.css";
import { latLng } from "leaflet";
import { LMap, LTileLayer } from "vue2-leaflet";
import { setInteractionMode } from "vee-validate";
 
setInteractionMode("aggressive");

export default {
  el: '#app',
  components: {
    LMap,
    LTileLayer,
  },
  data() {
    return {
      // Datos Leaflet
      zoom: 6,
      center: [-37.3121792, -61.3996217],
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      marker: latLng(0, 0),
      
    };
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
  }
};
