<template>
<div>
    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            Menú Principal
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list
        dense
        nav
      >
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
          :to="item.link"
        >
          <v-list-item-icon>
            <v-icon color="primary">{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>          

    </v-navigation-drawer>

    <v-app-bar app dark color="primary">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
        <div class="d-flex align-center">
            <v-img
            alt="Logo Centros"
            class="shrink mr-2"
            contain
            src="@/assets/logonew.jpg"
            transition="scale-transition"
            width="55"
            />
        </div>
        <v-toolbar-title>Centros Buenos Aires</v-toolbar-title>
        <v-spacer></v-spacer>   
    </v-app-bar> 
</div>  
</template>



<script>
  export default {
    name: 'AppBar',
    data () {
      return {
        items: [
          {title: 'Inicio', icon:'mdi-home',link:'/'},
          {title: 'Centros', icon: 'mdi-home-heart',link:'/centros'},
          {title: 'Turnos', icon: 'mdi-ticket-account',link:'/turnos'}
        ],
        drawer: false
      } 
    }
  }
</script>