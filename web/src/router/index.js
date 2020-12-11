const Centros = () => import("../views/Centros.vue");
const EstadoCentro = () => import("../views/EstadoCentro.vue");
const Home = () => import("../views/Home.vue");
const MisTurnos = () => import("../views/MisTurnos.vue");
const NewCentro = () => import("../views/NewCentro.vue");
const Turnos = () => import("../views/Turnos.vue");
const EstadisticasTurnos = () => import("../views/EstadisticasTurnos.vue");
import Vue from "vue";
import VueRouter from "vue-router";

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
  {
    path: "/v/estadisticas/turnos",
    name: "EstadisticasTurnos",
    component: EstadisticasTurnos,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
