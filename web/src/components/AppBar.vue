<template>
  <div>
    <v-navigation-drawer v-model="drawer" app>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title"> Menú Principal </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list>
        <v-list-item link to="/">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>

          <v-list-item-title>Inicio</v-list-item-title>
        </v-list-item>

        <!-- Opciones de los Centros -->

        <v-list-group
          group="/centros"
          :value="false"
          prepend-icon="mdi-home-heart"
        >
          <template v-slot:activator>
            <v-list-item-title>Centros</v-list-item-title>
          </template>

          <v-list-item
            class="ml-10"
            v-for="([title, icon, link], i) in centros"
            :key="i"
            link
            :to="link"
          >
            <v-list-item-title v-text="title"></v-list-item-title>

            <v-list-item-icon>
              <v-icon v-text="icon"></v-icon>
            </v-list-item-icon>
          </v-list-item>
        </v-list-group>

        <!-- /Opciones de los Centros -->

        <!-- Opciones de los Turnos -->

        <v-list-group
          group="/turnos"
          :value="false"
          prepend-icon="mdi-ticket-account"
        >
          <template v-slot:activator>
            <v-list-item-title>Turnos</v-list-item-title>
          </template>

          <v-list-item
            class="ml-10"
            v-for="([title, icon, link], i) in turnos"
            :key="i"
            link
            :to="link"
          >
            <v-list-item-title v-text="title"></v-list-item-title>

            <v-list-item-icon>
              <v-icon v-text="icon"></v-icon>
            </v-list-item-icon>
          </v-list-item>
        </v-list-group>

        <!-- /Opciones de los Turnos -->
      </v-list>
      <v-list-item @click="darkMode">
        <v-list-item-icon>
          <v-icon>mdi-theme-light-dark</v-icon>
        </v-list-item-icon>

        <v-list-item-title>Claro/Oscuro</v-list-item-title>
      </v-list-item>
    </v-navigation-drawer>

    <v-app-bar app dark color="primary">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <div class="d-flex align-center">
        <v-img
          alt="Logo Centros"
          class="shrink mr-2"
          contain
          src="@/assets/logonew.png"
          transition="scale-transition"
          width="38"
        />
      </div>
      <v-toolbar-title>Centros Buenos Aires</v-toolbar-title>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  name: "AppBar",
  data() {
    return {
      centros: [
        ["Listado", "mdi-home-search", "/centros/buscar"],
        ["Nuevo Centro", "mdi-home-plus", "/centros/crear"],
      ],
      turnos: [
        ["Opcion 1", "mdi-plus-circle", "/turnos/opcion1"],
        ["Opcion 2", "mdi-card-search-outline", "/turnos/opcion2"],
      ],
      drawer: false,
    };
  },

  created() {
    // Configuracion Tema
    if (localStorage.getItem("settings") === null) {
      var localDataNotSet = {
        settings: {
          dark_theme: this.$vuetify.theme.dark,
        },
      };
      localStorage.setItem("settings", JSON.stringify(localDataNotSet));
    } else {
      var localData = JSON.parse(localStorage.getItem("settings"));
      this.$vuetify.theme.dark = localData.settings.dark_theme;
    }
  },
  methods: {
    darkMode() {
      var localData = JSON.parse(localStorage.getItem("settings"));
      localData.settings.dark_theme = !this.$vuetify.theme.dark;
      localStorage.setItem("settings", JSON.stringify(localData));
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    },
  },
};
</script>
