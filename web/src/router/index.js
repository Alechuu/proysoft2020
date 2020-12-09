import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Turnos from "../views/Turnos.vue";
import NewCentro from "../views/NewCentro.vue";
import Centros from "../views/Centros.vue";
import EstadoCentro from "../views/EstadoCentro.vue";
import MisTurnos from "../views/MisTurnos.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/v/centros/buscar",
    name: "Centros",
    component: Centros,
  },
  {
    path: "/v/centros/crear",
    name: "Nuevo Centro",
    component: NewCentro,
  },
  {
    path: "/v/centros/estado",
    name: "Estado Solicitud",
    component: EstadoCentro,
  },
  {
    path: "/v/turnos/solicitud",
    name: "Turnos",
    component: Turnos,
  },
  {
    path: "/v/turnos/misturnos",
    name: "MisTurnos",
    component: MisTurnos,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
