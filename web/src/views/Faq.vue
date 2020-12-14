<template>
  <v-container>
    <v-card class="mt-5" color="primary" elevation="5">
      <div class="pa-5" style="text-align: center">
        <v-icon color="white" size="50"> mdi-information </v-icon>
        <h1 class="text-h4" style="text-align: center; color: white">
          Preguntas Frecuentes
        </h1>
      </div>
    </v-card>
    <v-expansion-panels class="mt-5">
      <v-expansion-panel v-for="item in preguntas" :key="item">
        <v-expansion-panel-header color="primary"
          ><span style="color:white;">{{
            item.pregunta
          }}</span></v-expansion-panel-header
        >
        <v-expansion-panel-content>
          <p class="mt-5" style="text-align:left;white-space: pre-line">
            {{ item.respuesta }}
          </p>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<script>
export default {
  name: "PreguntasFrecuentes",
  data() {
    return {
      preguntas: [
        {
          pregunta: "¿Cuál es el propósito de este sitio web?",
          respuesta:
            "Debido a la situación que se enfrenta hoy en día en el mundo entero, " +
            "decidimos crear una forma fácil y rápida de poder conectar a personas \n" +
            " que quieran donar o necesiten una mano, junto con los mismos Centros de " +
            "donación. \n " +
            "La idea principal es que puedas encontrar tu Centro más cercano y sacar un Turno para que puedas acercarte al mismo. \n" +
            "Todo esto de una forma rápida y 100% virtual. \n" +
            "Nota: Este sitio web abarca Centros ubicados únicamente en la Provincia de Buenos Aires.",
        },
        {
          pregunta: "¿Cómo encuentro mi Centro más cercano?",
          respuesta:
            "En el menú de la izquierda, desplegá la solapa 'Centros' y clickeá la opción 'Listado'. \n" +
            "Una vez estando ahí, vas a poder visualizar una tabla con todos los Centros y abajo, un mapa " +
            "mostrando la ubicación de los mismos. \n" +
            "En la Tabla podés buscar por cualquier dato del Centro, por ejemplo, " +
            "si sos de Quilmes, podés buscar 'Quilmes' y automáticamente te van a " +
            "aparecer todos los Centros ubicados en Quilmes. \n" +
            "Para ver donde está ubicado un Centro podés tocar en el ícono de <ubicacion>.",
        },
        {
          pregunta: "¿Cómo solicito un Turno para un ir a un Centro?",
          respuesta: "",
        },
        {
          pregunta: "¡Saqué un Turno pero no pude descargarlo! ¿Qué hago?",
          respuesta: "",
        },
        {
          pregunta:
            "Conozco un Centro que no está acá, ¿Cómo puedo solicitar para agregarlo?",
          respuesta: "",
        },
        {
          pregunta:
            "Solicité un Centro nuevo, ¿Puedo saber el estado de la solicitud?",
          respuesta: "",
        },
      ],
    };
  },
};
</script>
