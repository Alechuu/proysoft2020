import App from "./App.vue";
import L from "leaflet";
import vuetify from "./plugins/vuetify";
import Vue from "vue";
import router from "./router";

import VeBar from "v-charts/lib/bar.common";
import VeLine from "v-charts/lib/line.common";

Vue.component(VeBar.name, VeBar);
Vue.component(VeLine.name, VeLine);

Vue.config.productionTip = false;

// Configuración de Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
