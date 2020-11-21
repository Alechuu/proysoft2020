<template>
  <v-app id="inspire">
    <AppBar/>
    <v-main>
      <router-view></router-view>
    </v-main>
    <v-footer
      relative
      class="font-weight-medium"
      color="primary"
      dark
    >
      <v-col
        class="text-center"
        cols="12"
      >
         <strong>Grupo 33 Proyecto de Software</strong> - {{ new Date().getFullYear() }}
      </v-col>
    </v-footer>    
  </v-app>
</template>



<script>
  import AppBar from '@/components/AppBar.vue'
  export default {
    components: {
      AppBar,
    }
  }
</script>