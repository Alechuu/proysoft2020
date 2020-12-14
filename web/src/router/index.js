const Centros = () => import("../views/Centros/Centros.vue");
const EstadoCentro = () => import("../views/Centros/EstadoCentro.vue");
const Home = () => import("../views/Home.vue");
const MisTurnos = () => import("../views/Turnos/MisTurnos.vue");
const NewCentro = () => import("../views/Centros/NewCentro.vue");
const Turnos = () => import("../views/Turnos/Turnos.vue");
const EstadisticasTurnos = () =>
  import("../views/Estadisticas/EstadisticasTurnos.vue");
const EstadisticasHorarios = () =>
  import("../views/Estadisticas/EstadisticasHorarios.vue");
const EstadisticasCentros = () =>
  import("../views/Estadisticas/EstadisticasCentros.vue");
const FAQ = () => import("../views/Faq.vue");
const NotFound = () => import("../views/NotFound.vue");
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
  {
    path: "/v/estadisticas/horarios",
    name: "EstadisticasHorarios",
    component: EstadisticasHorarios,
  },
  {
    path: "/v/estadisticas/centros",
    name: "EstadisticasCentros",
    component: EstadisticasCentros,
  },
  {
    path: "/v/faq",
    name: "PreguntasFrecuentes",
    component: FAQ,
  },
  { path: "/404", component: NotFound },
  { path: "*", redirect: "/404" },
];

const router = new VueRouter({
  routes,
});

export default router;
