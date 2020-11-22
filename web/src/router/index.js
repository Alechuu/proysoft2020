import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Turnos from '../views/Turnos.vue'
import NewCentro from '../views/NewCentro.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/centros',
    name: 'Centros',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Centros.vue')
  },
  {
    path: '/turnos',
    name: 'Turnos',
    component: Turnos
  },
  {
    path: '/centros/crear',
    name: 'Nuevo Centro',
    component: NewCentro
  }
]

const router = new VueRouter({
  routes
})

export default router
