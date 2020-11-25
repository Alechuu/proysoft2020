<template>
  <div class="home">
    <v-parallax
      dark
      src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg"
      height="400"
    >
      <v-row
        align="center"
        justify="center"
      >
        <v-col
          class="text-center"
          cols="12"
        >
          
          <h1 class="display-2 font-weight-black mb-4">
            Centros de donación de la Provincia de Buenos Aires
          </h1>
          <h3 class="font-italic">
            Cientos de centros de ropa, alimentos, donaciones de sangre, plasma y ¡muchos más!
          </h3>
        </v-col>
      </v-row>
    </v-parallax>
    <div class="d-flex flex-column justify-center">
      <v-card
        v-for="slide in slides"
        :key="slide.title"
        class="d-flex justify-center pa-15"
        outlined
        tile
      >
        <div style="text-align:center;">
          <v-icon 
          size="50"
          color="primary"
          > {{ slide.icon }} 
          </v-icon>          
          <h1>{{ slide.title }}</h1>
          <p 
          class="mt-2"
          style="font-family:Ruda;font-size:20px;max-width:600px"
          >{{slide.descripcion}}</p>
          <v-btn 
          color="primary" 
          v-if="slide.boton"
          :to="slide.link" >{{slide.botonContent}}</v-btn>
        </div>

      </v-card>
    </div>  
  </div>
</template>




<script>
export default {
  name: 'Home',
  data () {
    return {
      slides: [
        {
          title: 'Información General',
          icon: 'mdi-help-circle',
          descripcion: 'Acá vas a poder encontrar un montón de Centros ubicados en la Provincia de Buenos Aires. Podés buscar tu Centro más cercano para donar, recibir asistencia o incluso agregar un Centro nuevo. '
          
        },
        {
          title: 'Donaciones',
          icon: 'mdi-heart-plus',
          descripcion: 'Donar es muy fácil, hacé click abajo para buscar un Centro al cuál donar.',
          boton: true,
          botonContent: 'Donar',
          link:'/centros' 
        },
        {
          title: 'Necesito una mano',
          icon: 'mdi-hand-heart',
          descripcion: '¿Necesitás asistencia? Hacé click abajo y buscá el Centro más cercano para empezar.',
          boton: true,
          botonContent: 'Necesito una mano',
          link:'/centros'
        },
        {
          title: 'Nuevo Centro',
          icon: 'mdi-home-heart',
          descripcion: 'Si sabés de algún Centro que falte, hacé click abajo para llenar un formulario con los datos correspondientes.',
          boton: true,
          botonContent: 'Solicitar',
          link:'/centros/crear' 
        }        
    ]
    }
  }

}
</script>
