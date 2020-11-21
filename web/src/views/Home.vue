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
          <h1 class="display-2 font-weight-thin mb-4">
            Centros de donación de la Provincia de Buenos Aires
          </h1>
          <h4 class="subheading">
            Dándole una mano al que más lo necesita
          </h4>
        </v-col>
      </v-row>
    </v-parallax>
    <div class="d-flex flex-column justify-center">
      <v-card
        v-for="slide in slides"
        :key="slide.title"
        class="d-flex justify-center pa-2"
        outlined
        tile
      >
        <div style="text-align:center;">
          <h1>{{ slide.title }}</h1>
          <v-icon 
          size="50"
          color="primary"
          > {{ slide.icon }} </v-icon>
          <p 
          class="mt-2"
          style="font-family:Ruda;font-size:20px;max-width:600px"
          >{{slide.descripcion}}</p>
          <v-btn color="primary" v-if="slide.boton" >{{slide.botonContent}}</v-btn>
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
          title: '¿De qué trata este sitio web?',
          icon: 'mdi-help-circle',
          descripcion: 'Text some text '+'Some other text'
          
        },
        {
          title: '¿Cómo puedo donar?',
          icon: 'mdi-heart-plus',
          descripcion: 'Donar es muy fácil, hacé click abajo para empezar',
          boton: true,
          botonContent: 'Donar'
        },
        {
          title: 'Necesito una mano',
          icon: 'mdi-hand-heart',
          descripcion: 'Al igual que donar, hacé click abajo para empezar',
          boton: true,
          botonContent: 'Necesito una mano'
        }        
    ]
    }
  }

}
</script>
