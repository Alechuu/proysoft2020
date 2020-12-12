<template>
  <v-app id="inspire">
    <AppBar />
    <v-main>
      <transition name="slide-fade" mode="out-in">
        <router-view></router-view>
      </transition>
    </v-main>
    <v-footer relative class="font-weight-medium" color="primary" dark>
      <v-col class="text-center" cols="12">
        <strong>Grupo 33 Proyecto de Software</strong> -
        {{ new Date().getFullYear() }}
      </v-col>
    </v-footer>
  </v-app>
</template>



<script>
import AppBar from "@/components/AppBar.vue";
export default {
  components: {
    AppBar,
  },
};
</script>

<style>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}
.slide-fade-enter,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-30%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>