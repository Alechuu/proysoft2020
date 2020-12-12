import Vue from "vue";
import Vuetify from "vuetify/lib";
import es from "vuetify/es5/locale/es";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    options: {
      customProperties: true,
    },
    themes: {
      light: {
        primary: "#00aec1",
        secondary: "#f5f5f5 ",
        accent: "#82B1FF",
        error: "#FF5252",
        info: "#2196F3",
        success: "#4CAF50",
        warning: "#fd8c04",
      },
      dark: {
        primary: "#3282b8",
        success: "#16a596",
        warning: "#db6400",
        error: "#af2d2d",
        info: "#0f4c75",
      },
    },
  },
  lang: {
    locales: { es },
    current: "es",
  },
});
