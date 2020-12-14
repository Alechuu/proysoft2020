<template>
  <v-container>
    <v-card class="mt-5" color="primary" elevation="5">
      <div class="pa-5" style="text-align: center">
        <v-icon color="white" size="50"> mdi-help-circle </v-icon>
        <h1 class="text-h4" style="text-align: center; color: white">
          Preguntas Frecuentes
        </h1>
      </div>
    </v-card>
    <v-expansion-panels class="mt-5">
      <v-expansion-panel>
        <v-expansion-panel-header color="primary"
          ><span style="color:white;">
            ¿Cuál es el propósito de este sitio web?
          </span></v-expansion-panel-header
        >
        <v-expansion-panel-content>
          <p class="mt-5" style="text-align:left;white-space: pre-line">
            Debido a la situación que se enfrenta hoy en día en el mundo entero,
            decidimos crear una forma fácil y rápida de poder conectar a
            personas <br />
            que quieran donar o necesiten una mano, junto con los mismos Centros
            de donación. <br />
            La idea principal es que puedas encontrar tu Centro más cercano y
            sacar un Turno para que puedas acercarte al mismo. <br />
            Todo esto de una forma rápida y 100% virtual. <br />
            <b>Nota:</b> Este sitio web abarca Centros ubicados
            <b>únicamente</b> en la Provincia de Buenos Aires.
          </p>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header color="primary"
          ><span style="color:white;">
            ¿Cómo encuentro mi Centro más cercano?
          </span></v-expansion-panel-header
        >
        <v-expansion-panel-content>
          <p class="mt-5" style="text-align:left;white-space: pre-line">
            En el menú de la izquierda, desplegá la solapa <i>Centros</i> y
            clickeá la opción <i>Listado</i>. <br />
            Una vez estando ahí, vas a poder visualizar una tabla con todos los
            Centros y abajo, un mapa mostrando la ubicación de los mismos.
            <br />
            En la Tabla podés buscar por cualquier dato del Centro, por ejemplo,
            si sos de Quilmes, podés buscar <i>Quilmes</i> y automáticamente te
            van a aparecer todos los Centros ubicados en Quilmes. <br />
            Para ver donde está ubicado un Centro podés tocar en el ícono de
            <v-icon small>mdi-map-marker</v-icon>
          </p>
          <v-btn to="/v/centros/buscar" color="primary">Ir al listado</v-btn>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header color="primary"
          ><span style="color:white;">
            ¿Cómo solicito un Turno para un ir a un Centro?
          </span></v-expansion-panel-header
        >
        <v-expansion-panel-content>
          <p class="mt-5" style="text-align:left;white-space: pre-line">
            En el menú de la izquierda, desplegá la solapa <i>Centros</i> y
            clickeá la opción <i>Listado</i>. <br />
            Una vez estando ahí, vas a poder visualizar una tabla con todos los
            Centros. En esa misma tabla buscá el Centro al que quieras ir
            (también podés buscar un Centro desde el mapa que está debajo de la
            tabla), una vez que lo encuentres, tocá en el ícono de
            <v-icon small>mdi-calendar</v-icon> <br />
            Eso te va a redirigir automáticamente a un formulario para que
            llenes unos datos personales y elijas el día y horario del turno.
            <br />
            Una vez hecho eso vas a poder descargar tu Turno en formato PDF.
          </p>
          <v-btn to="/v/centros/buscar" color="primary">Ir al listado</v-btn>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header color="primary"
          ><span style="color:white;">
            ¡Saqué un Turno pero no pude descargarlo! ¿Qué hago?
          </span></v-expansion-panel-header
        >
        <v-expansion-panel-content>
          <p class="mt-5" style="text-align:left;white-space: pre-line">
            No te preocupes, si por algún motivo no pudiste descargar el PDF de
            tu Turno, podés ir al menú de la izquierda y en la solapa
            <i>Turnos</i> hacé click en la opción <i>Mis Turnos</i>. <br />
            Una vez estando ahí, seleccioná una fecha, completa tu e-mail y vas
            a poder visualizar todos los turnos que solicitaste para esa
            determinada fecha.
          </p>
          <v-btn to="/v/turnos/misturnos" color="primary"
            >Ir a Mis Turnos</v-btn
          >
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header color="primary"
          ><span style="color:white;">
            Conozco un Centro que no está acá, ¿Cómo puedo solicitar para
            agregarlo?
          </span></v-expansion-panel-header
        >
        <v-expansion-panel-content>
          <p class="mt-5" style="text-align:left;white-space: pre-line">
            ¡Sí! Si conoces un Centro de donación y lo querés agregar podés
            llenar un formulario con los datos del mismo para que quede
            pendiente de aprobación. <br />
            Para hacer esto, andá al menú de la izquierda, desplegá la solapa
            <i>Centros</i> y hacé click en <i>Nuevo Centro</i>. <br />
            Una vez hayas llenado los datos requeridos y hayas enviado la
            solicitud, vas a poder ver el estado de la solicitud haciendo click
            en <i>Ver Solicitud</i>. <br />
            <b>Nota:</b> Cuando veas la solicitud, se te va a informar de tu
            <b>número de solicitud</b>, por favor anotalo para poder consultar
            la solicitud en un futuro.
          </p>
          <v-btn to="/v/centros/crear" color="primary">Ir a Nuevo Centro</v-btn>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header color="primary"
          ><span style="color:white;">
            Solicité un Centro nuevo, ¿Puedo saber el estado de la solicitud?
          </span></v-expansion-panel-header
        >
        <v-expansion-panel-content>
          <p class="mt-5" style="text-align:left;white-space: pre-line">
            Si solicitaste un nuevo Centro y anotaste tu
            <b>número de solicitud</b> podés consultar el estado de la solicitud
            yendo al menú de la izquierda, desplegando la solapa
            <i>Centros</i> y haciendo click en <i>Estado Solicitud</i>. <br />
            Una vez estando allí, ingresá el <b>número de tu solicitud</b> y
            hacé click en
            <i>Ver Solicitud</i> <br>
            La solicitud puede tener 3 estados:
            <ul>
                <li><b>EN REVISIÓN</b></li>
                <li><b>ACEPTADO</b></li>
                <li><b>RECHAZADO</b></li>
            </ul>
          </p>
          <v-btn to="/v/centros/estado" color="primary">Ir a Estado Solicitud</v-btn>
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
